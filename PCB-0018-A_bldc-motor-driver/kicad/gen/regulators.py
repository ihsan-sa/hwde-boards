"""PCB-0018-A `regulators` sheet: VM->+5V buck, +5V->+12V boost, +5V->+3V3
LDO, +3V3->VDDA ferrite.

Refdes block 200 (architecture/sheets.md): U201-U203, L201-L202, D201,
R201-R205, C201-C209, FB201, #PWR200+. Build output:
kicad/regulators.kicad_sch.

Ground truth: parts/C477928.json (LM5164), parts/C7722.json (TPS61040),
parts/C485517.json (TLV75733) and `schlib.py --pins aiee:<part>`.

Pin decisions:
  * U201 LM5164 EN/UVLO (3) tied directly to VIN (VM): abs max is the same
    100V VIN ceiling, and no programmable UVLO is required by the brief -
    "no MCU enable signal exists on this sheet" is the same call power_in
    made for the LM74500's EN.
  * U201 PGOOD (6) is open-drain output, unused -> explicit no-connect.
  * U201 RON (4): R201 31.6k to GND -> ~400kHz (Eq.15, power_tree.md).
  * U201 FB (5): R202 33.2k (top, VOUT) / R203 10k (bottom, GND).
  * U201 VIN decoupling: C203 100nF HF ceramic (role reg_input, <=1uF) +
    C204 10uF/50V bulk (role reg_input) - both required by the P4 brief
    ("reg_input HF ceramic <=1uF plus bulk"); C204 reuses the power_stage
    leg-bank 50V 1210 part since no VM-rated bulk cap exists in parts.json
    for this pin specifically.
  * U201 BST(7)-SW(8): C201 2.2nF CBST, wired directly (not via the
    decoupling-to-GND helper - this cap returns to SW, not GND).
  * U201 SW(8) -> local label BUCK_SW (constraints.json canonical name) ->
    L201 -> +5V; C202 22uF output cap, +5V to GND.
  * U201 EP(9) -> GND (datasheet: "no internal electrical connection...
    connect EP to GND pin").
  * U202 TPS61040 EN(4) tied to VIN(+5V): "must not be left floating";
    always-on boost, no MCU enable signal available here either.
  * U202 SW(1) -> local label BOOST_SW -> L202 -> +5V (inductor from VIN to
    switch node, standard boost) and D201 anode; D201 cathode -> +12V.
    D201 MBR0520L pin map from the aiee footprint's silkscreen diode glyph
    (triangle/cathode-bar): pin 1 = K, pin 2 = A (no named pins in the
    2-pin generic symbol body - confirmed against the SOD-123 footprint
    polarity graphic, no datasheet JSON exists for C5563735).
  * U202 FB(3): R204 86.6k (top, +12V) / R205 10k (bottom, GND).
  * U203 TLV75733 EN(3) tied to IN(+5V): active-high enable, "must not be
    left floating" equivalent guidance; always-on LDO.
  * U203 pin 4 (NC) -> true no-connect ("No internal connection", DBV pkg).
  * FB201 ferrite +3V3 -> VDDA, exposed as the sheet's one hier pin (output
    - this sheet drives VDDA). C209 100nF local bypass added after the
    ferrite as ordinary analog-supply practice; the MCU sheet may add its
    own pin-adjacent VDDA decoupling too (noted in OPEN).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BOARD = HERE.parents[2]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "hwde" / "scripts"))

if not os.environ.get("KICAD_SYMBOL_DIR"):
    for _cand in (os.environ.get("KICAD10_SYMBOL_DIR"),
                  str(Path.home() / ".local/kicad10/usr/share/kicad/symbols")):
        if _cand and Path(_cand).is_dir():
            os.environ["KICAD_SYMBOL_DIR"] = _cand
            break

import kicad_sch_api as ksa  # noqa: E402

ksa.get_symbol_cache().add_library_path(BOARD / "lib" / "aiee.kicad_sym")

import schlib  # noqa: E402

NAME = "regulators"
FP = "aiee"
R0603 = f"{FP}:R0603"
C0603 = f"{FP}:C0603"
C0805 = f"{FP}:C0805"
C1210 = f"{FP}:C1210"

LCSC = {
    "U201": "C477928", "L201": "C2849539",
    "R201": "C25967", "R202": "C23003", "R203": "C25804",
    "C201": "C1604", "C202": "C45783", "C203": "C14663", "C204": "C2918502",
    "U202": "C7722", "L202": "C135264", "D201": "C5563735",
    "R204": "C23121", "R205": "C25804",
    "C205": "C15850", "C206": "C28323",
    "U203": "C485517", "C207": "C28323", "C208": "C28323",
    "FB201": "C1002", "C209": "C14663", "C213": "C14663",
    "R206": "C25803", "C210": "C1604", "C211": "C14663", "C212": "C1588",
}


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME, title="PCB-0018 REV A regulators: VM->5V buck, 5V->12V boost, 5V->3V3 LDO",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=200)

    # ==================================================================
    # U201 LM5164: VM -> +5V synchronous buck, COT, 400kHz
    # ==================================================================
    sh.place_ic_with_decoupling(
        "U201", f"{FP}:LM5164DDAR", "LM5164", at=(76.2, 76.2),
        footprint=f"{FP}:SO-8_L4.9-W3.9-P1.27-LS6.0-BL-EP",
        pins={"1": "GND",
              "2": "VM",         # VIN
              "3": "VM",         # EN/UVLO tied to VIN: no MCU enable here
              "4": "RON5V",
              "5": "FB5V",
              "6": "NC",         # PGOOD unused
              "7": "BST5V",
              "8": "BUCK_SW",
              "9": "GND"},       # EP
        expect={"1": "GND", "2": "VIN", "3": "EN/UVLO", "4": "RON", "5": "FB",
                "6": "PGOOD", "7": "BST", "8": "SW", "9": "EP"},
        decoupling=[
            {"cap": "C203", "pin": "2", "rail": "VM", "value": "100nF 50V X7R",
             "lib_id": f"{FP}:CC0603KRX7R9BB104", "footprint": C0603,
             "role": "reg_input"},
            {"cap": "C204", "pin": "2", "rail": "VM", "value": "10uF 50V X7R",
             "lib_id": f"{FP}:CS3225X7R106K500NRL", "footprint": C1210,
             "role": "reg_input"},
        ],
        caps_at=(76.2, 114.3), caps_dx=25.4)
    sh.add_component(f"{FP}:0603WAF3162T5E", "R201", "31.6k 1%",
                     at=(114.3, 63.5), footprint=R0603)
    sh.wire_pins("R201", {"1": "RON5V", "2": "GND"})
    sh.add_component(f"{FP}:0603WAF3322T5E", "R202", "33.2k 1%",
                     at=(139.7, 50.8), footprint=R0603)
    sh.wire_pins("R202", {"1": "+5V", "2": "FB5V"})
    sh.add_component(f"{FP}:0603WAF1002T5E", "R203", "10k",
                     at=(139.7, 76.2), footprint=R0603)
    sh.wire_pins("R203", {"1": "FB5V", "2": "GND"})
    sh.add_component(f"{FP}:0603B222K500NT", "C201", "2.2nF 50V X7R",
                     at=(114.3, 88.9), footprint=C0603)
    sh.wire_pins("C201", {"1": "BST5V", "2": "BUCK_SW"})
    sh.add_component(f"{FP}:PNLS6045-220M22UH", "L201", "22uH shielded",
                     at=(165.1, 76.2), footprint=f"{FP}:IND-SMD_L6.0-W6.0")
    sh.wire_pins("L201", {"1": "BUCK_SW", "2": "+5V"})
    sh.add_component(f"{FP}:CL21A226MAQNNNE", "C202", "22uF 25V X5R",
                     at=(190.5, 88.9), footprint=C0805)
    sh.wire_pins("C202", {"1": "+5V", "2": "GND"})
    # Type-3 ripple injection (LM5164 DS 6.3.1: COT needs >=20 mV in-phase
    # ripple at FB; an all-ceramic output gives ~1-2 mV). RA/CA filter the
    # inductor voltage, CB couples it onto FB. tau = 100k * 2.2nF = 220 us:
    # (VIN-VOUT)*tON/tau = 28 mV at VM 10 V, 45 mV at 28 V, 49 mV at 45 V.
    sh.add_component(f"{FP}:0603WAF1003T5E", "R206", "100k",
                     at=(215.9, 50.8), footprint=R0603)
    sh.wire_pins("R206", {"1": "BUCK_SW", "2": "RIPPLE_INJ"})
    sh.add_component(f"{FP}:0603B222K500NT", "C210", "2.2nF 50V X7R",
                     at=(241.3, 50.8), footprint=C0603)
    sh.wire_pins("C210", {"1": "RIPPLE_INJ", "2": "+5V"})
    sh.add_component(f"{FP}:CC0603KRX7R9BB104", "C211", "100nF 50V X7R",
                     at=(266.7, 50.8), footprint=C0603)
    sh.wire_pins("C211", {"1": "RIPPLE_INJ", "2": "FB5V"})

    # ==================================================================
    # U202 TPS61040: +5V -> +12V boost (GVDD supply for the gate driver)
    # ==================================================================
    sh.place_ic_with_decoupling(
        "U202", f"{FP}:TPS61040DBVR", "TPS61040", at=(76.2, 165.1),
        footprint=f"{FP}:SOT-23-5_L2.9-W1.6-P0.95-LS2.8-BL",
        pins={"1": "BOOST_SW", "2": "GND", "3": "FB12V", "4": "+5V", "5": "+5V"},
        expect={"1": "SW", "2": "GND", "3": "FB", "4": "EN", "5": "VIN"},
        decoupling=[
            {"cap": "C205", "pin": "5", "rail": "+5V", "value": "10uF 25V X5R",
             "lib_id": f"{FP}:CL21A106KAYNNNE", "footprint": C0805,
             "role": "reg_input"},
        ],
        caps_at=(76.2, 190.5))
    # C213 added at verify (reg_input_no_hf): the TPS61040 switch current
    # needs an HF ceramic <= 1 uF at VIN, not only the C205 bulk.
    sh.add_component(f"{FP}:CC0603KRX7R9BB104", "C213", "100nF 50V X7R",
                     at=(50.8, 190.5), footprint=C0603)
    sh.wire_pins("C213", {"1": "+5V", "2": "GND"})
    sh.add_component(f"{FP}:SMNR4020-22UH", "L202", "22uH shielded",
                     at=(139.7, 152.4), footprint=f"{FP}:IND-SMD_L4.0-W4.0_LQH44PN2R2MP0L")
    sh.wire_pins("L202", {"1": "+5V", "2": "BOOST_SW"})
    sh.add_component(f"{FP}:MBR0520L_C5563735", "D201", "MBR0520L",
                     at=(165.1, 165.1), footprint=f"{FP}:SOD-123_L2.7-W1.6-LS3.7-RD-1")
    sh.wire_pins("D201", {"1": "+12V", "2": "BOOST_SW"})
    sh.add_component(f"{FP}:CL21B105KBFNNNE", "C206", "1uF 50V X7R",
                     at=(190.5, 177.8), footprint=C0805)
    sh.wire_pins("C206", {"1": "+12V", "2": "GND"})
    sh.add_component(f"{FP}:0603WAF8662T5E", "R204", "86.6k 1%",
                     at=(139.7, 190.5), footprint=R0603)
    sh.wire_pins("R204", {"1": "+12V", "2": "FB12V"})
    # CFF across R1 (datasheet eq. 6): CFF = 1/(2*pi*(fS/20)*R1). GVDD load
    # ~10 mA (6 gates x ~40 nC x 20 kHz + driver IQ) gives fS = 2*Iout*(Vout-
    # Vin+Vd)/(Ip^2*L) = 2*0.01*7.4/(0.4^2*22u) ~ 42 kHz -> CFF ~ 875 pF; 1 nF.
    sh.add_component(f"{FP}:CL10B102KB8NNNC", "C212", "1nF 50V X7R",
                     at=(165.1, 203.2), footprint=C0603)
    sh.wire_pins("C212", {"1": "+12V", "2": "FB12V"})
    sh.add_component(f"{FP}:0603WAF1002T5E", "R205", "10k",
                     at=(139.7, 215.9), footprint=R0603)
    sh.wire_pins("R205", {"1": "FB12V", "2": "GND"})

    # ==================================================================
    # U203 TLV75733: +5V -> +3V3 LDO
    # ==================================================================
    sh.place_ic_with_decoupling(
        "U203", f"{FP}:TLV75733PDBVR", "TLV75733", at=(76.2, 241.3),
        footprint=f"{FP}:SOT-23-5_L2.9-W1.6-P0.95-LS2.8-BL",
        pins={"1": "+5V", "2": "GND", "3": "+5V", "4": "NC", "5": "+3V3"},
        expect={"1": "IN", "2": "GND", "3": "EN", "4": "NC", "5": "OUT"},
        decoupling=[
            {"cap": "C207", "pin": "1", "rail": "+5V", "value": "1uF 50V X7R",
             "lib_id": f"{FP}:CL21B105KBFNNNE", "footprint": C0805,
             "role": "reg_input"},
        ],
        caps_at=(76.2, 266.7))
    sh.add_component(f"{FP}:CL21B105KBFNNNE", "C208", "1uF 50V X7R",
                     at=(139.7, 254.0), footprint=C0805)
    sh.wire_pins("C208", {"1": "+3V3", "2": "GND"})

    # ==================================================================
    # FB201: +3V3 -> VDDA ferrite filter (hier output to mcu)
    # ==================================================================
    sh.add_component(f"{FP}:GZ1608D601TF", "FB201", "600ohm@100MHz ferrite",
                     at=(76.2, 292.1), footprint=R0603)
    sh.wire_pins("FB201", {"1": "+3V3"})
    sh.hier_pin("VDDA", ref="FB201", pad="2", shape="output")
    sh.add_component(f"{FP}:CC0603KRX7R9BB104", "C209", "100nF 50V X7R",
                     at=(101.6, 304.8), footprint=C0603)
    sh.wire_pins("C209", {"1": "VDDA", "2": "GND"})

    # ---- rails: driven by this sheet's regulators (VOUT pins are actual
    # power-out-class connections downstream of the FET/inductor); VM is
    # consumed only, flag=False (power_in owns its PWR_FLAG).
    sh.power_flag("VM", at=(190.5, 292.1), sym="power:VCC", flag=False)
    sh.power_flag("+5V", at=(215.9, 292.1), sym="power:+5V", flag=True)
    sh.power_flag("+12V", at=(241.3, 292.1), sym="power:+12V", flag=True)
    sh.power_flag("+3V3", at=(266.7, 292.1), sym="power:+3V3", flag=False)
    sh.power_flag("GND", at=(292.1, 292.1), sym="power:GND", flag=False)
    # +5V (inductor-fed), +12V (diode-fed), VDDA (ferrite-fed) and BST5V
    # (bootstrap cap) have no power-output pin on them, so this sheet, which
    # sources each, carries their one PWR_FLAG.
    sh.power_flag("VDDA", at=(317.5, 292.1), flag=True)
    sh.power_flag("BST5V", at=(342.9, 292.1), flag=True)

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    return sh


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else Path("/tmp/p18-regulators")
    try:
        sh = build()
        sch = sh.save(out_dir, project=True)
        meta = sh.emit_decoupling(out_dir / "decoupling.json")
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"script": f"gen.{NAME}", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({"script": f"gen.{NAME}", "status": "pass",
                      "files": [str(sch), str(meta)],
                      "hier_pins": sorted(sh.hier_pins)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
