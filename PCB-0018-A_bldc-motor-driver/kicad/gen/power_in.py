"""PCB-0018-A `power_in` sheet: reverse-polarity protected VM entry.

Refdes block 100 (architecture/sheets.md): TP101/TP102 (bare pads), Q101,
U101, D101, C101-C104, #PWR100+. Build output: kicad/power_in.kicad_sch.

Ground truth: parts/C5219210.json (LM74500-Q1, TI SNVSAJ1) and
`schlib.py --pins aiee:LM74500QDDFRQ1` / `aiee:NTMFS5C628NLT1G`.

Topology (LM74500-Q1 reverse-polarity-protection controller driving an
external NMOS, non-blocking so BLDC regen current can flow back out to the
supply - parts.json role text for U101: an ideal-diode/blocking part would
pump VBUS on regen and is explicitly wrong here):
  * Q101 SOURCE = raw input (VM_IN, from TP101); Q101 DRAIN = protected VM.
    Body diode conducts VM_IN -> VM when polarity is correct; a reversed
    input leaves the body diode reverse-biased (blocked). Because the
    controller holds the FET fully enhanced (not just diode-ORing per half
    cycle), the CHANNEL also conducts VM -> VM_IN, so motor regen current
    is never blocked - only reversed input polarity is.
  * U101 SOURCE (5) = VM_IN (datasheet: "connect to the source of the
    external N-channel MOSFET"); GATE (6) -> Q101 gate; EN (1) tied to
    SOURCE for always-ON operation (datasheet note on EN, no MCU enable
    signal exists on this sheet); GND (2) -> GND; N.C (3,7,8) -> no-connect
    ("No connection" in the datasheet pin table).
  * C102 = VCAP-to-SOURCE charge-pump cap, 0.1uF, per the datasheet's
    recommended operating condition (NOT to GND - the pump needs SOURCE as
    its return, per "decoupling" pins ["VCAP","SOURCE"]).
  * C103 = SOURCE-to-GND bypass, >22nF recommended when the supply is more
    than a few inches away; reuses the same 100nF/50V part as C102 as the
    other MLCC named in the P4 brief ("C102/C103 MLCC").
  * D101 SMCJ28A: TVS on VM (task brief: "SMCJ28A TVS D101 on VM"), paired
    with C101 (bulk electrolytic, "at VM entry" = the VM net, 63V rating
    gives margin over the 45.4V clamp voltage per parts.json). Together
    they absorb the load-dump/regen energy the TVS clamps, downstream of
    Q101 so a raw-input surge never has to cross the FET first.
  * TP101/TP102 are bare copper pads (board features, no LCSC), same
    exclude-from-BOM pattern as stereo-class-d-amp's J1-J4/TP1.
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

# kicad-sch-api reads KICAD_SYMBOL_DIR, not the KICAD10_SYMBOL_DIR hwde exports.
if not os.environ.get("KICAD_SYMBOL_DIR"):
    for _cand in (os.environ.get("KICAD10_SYMBOL_DIR"),
                  str(Path.home() / ".local/kicad10/usr/share/kicad/symbols")):
        if _cand and Path(_cand).is_dir():
            os.environ["KICAD_SYMBOL_DIR"] = _cand
            break

import kicad_sch_api as ksa  # noqa: E402

ksa.get_symbol_cache().add_library_path(BOARD / "lib" / "aiee.kicad_sym")

from power_stage import _wire_all_drains  # noqa: E402  (same FET symbol)
import schlib  # noqa: E402

NAME = "power_in"
FP = "aiee"
R0603 = f"{FP}:R0603"
C0603 = f"{FP}:C0603"
TESTPAD = "Connector:TestPoint"
# 4.0 mm pad / 2.0 mm drill, same as the phase pads: these carry the whole
# bus (13 A continuous, ~25 A peak), so a 2.0 mm test pad is too small.
TESTPAD_FP = "TestPoint:TestPoint_THTPad_4.0x4.0mm_Drill2.0mm"
FET = f"{FP}:NTMFS5C628NLT1G"
FET_FP = f"{FP}:DFN-5_L4.9-W5.9-P1.27-LS6.2-BL"
FET_EXPECT = {"1": "S", "2": "S", "3": "S", "4": "G", "5": "D"}

LCSC = {
    "U101": "C5219210",   # LM74500QDDFRQ1
    "D101": "C2943858",   # SMCJ28A
    "C101": "C106675",    # 470uF 63V electrolytic
    "C104": "C106675",    # second 470uF 63V, shares the bus ripple current
    "C102": "C14663",     # 100nF 50V X7R (VCAP-SOURCE charge-pump cap)
    "C103": "C14663",     # 100nF 50V X7R (SOURCE-GND bypass)
    "Q101": "C145537",    # NTMFS5C628NLT1G
}
BARE_PADS = ("TP101", "TP102")


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME, title="PCB-0018 REV A power_in: reverse-polarity protected VM entry",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=100)

    # ---- input pads
    sh.add_component(TESTPAD, "TP101", "VM_IN", at=(25.4, 38.1),
                     footprint=TESTPAD_FP)
    sh.wire_pins("TP101", {"1": "VM_IN"})
    sh.add_component(TESTPAD, "TP102", "GND", at=(25.4, 63.5),
                     footprint=TESTPAD_FP)
    sh.wire_pins("TP102", {"1": "GND"})

    # ---- U101 LM74500-Q1 reverse-polarity controller
    sh.place_ic_with_decoupling(
        "U101", f"{FP}:LM74500QDDFRQ1", "LM74500-Q1", at=(76.2, 63.5),
        footprint=f"{FP}:SOT-23-8_L3.0-W1.7-P0.65-LS2.8-BR",
        pins={"1": "VM_IN",      # EN tied to SOURCE: always-ON, no MCU enable here
              "2": "GND",
              "3": "NC",         # datasheet: "No connection"
              "4": "VCAP",       # charge-pump output, cap to SOURCE (C102)
              "5": "VM_IN",      # SOURCE = raw input, same node as Q101 source
              "6": "Q_GATE",     # gate drive to Q101
              "7": "NC",
              "8": "NC"},
        expect={"1": "EN", "2": "GND", "3": "N.C", "4": "VCAP", "5": "SOURCE",
                "6": "GATE", "7": "N.C", "8": "N.C"},
        decoupling=[
            {"cap": "C102", "pin": "4", "rail": "VCAP", "value": "100nF 50V X7R",
             "lib_id": f"{FP}:CC0603KRX7R9BB104", "footprint": C0603,
             "gnd": "VM_IN"},   # VCAP-to-SOURCE, not to GND (datasheet)
        ],
        caps_at=(76.2, 101.6))
    # SOURCE bypass (>22nF recommended): separate cap, SOURCE(VM_IN) to GND.
    sh.add_component(f"{FP}:CC0603KRX7R9BB104", "C103", "100nF 50V X7R",
                     at=(101.6, 101.6), footprint=C0603)
    sh.wire_pins("C103", {"1": "VM_IN", "2": "GND"})

    # ---- Q101 reverse-polarity NMOS (SO-8FL/DFN-5: pins 1-3 S, 4 G, 5 D
    # - the 4 drain tabs share symbol pin number "5", per power_stage.py's
    # same-part precedent)
    sh.add_component(FET, "Q101", "NTMFS5C628NL", at=(139.7, 63.5),
                     footprint=FET_FP, expect=FET_EXPECT)
    sh.wire_pins("Q101", {"1": "VM_IN", "2": "VM_IN", "3": "VM_IN",
                          "4": "Q_GATE", "5": "VM"})
    _wire_all_drains(sh, "Q101", "VM")

    # ---- D101 TVS + C101 bulk on VM (post-FET, protected rail)
    sh.add_component(f"{FP}:SMCJ28A_C2943858", "D101", "SMCJ28A",
                     at=(190.5, 50.8), footprint=f"{FP}:SMC_L6.9-W5.8-LS7.9-RD",
                     expect={"1": "C", "2": "A"})
    sh.wire_pins("D101", {"1": "VM", "2": "GND"})
    sh.add_component(f"{FP}:ERS1JM471K20OT", "C101", "470uF 63V",
                     at=(215.9, 63.5), footprint=f"{FP}:CAP-TH_BD13.0-P5.00-D1.2-FD")
    sh.wire_pins("C101", {"1": "VM", "2": "GND"})
    # C104: a second bulk cap. Bus-cap RMS ripple of a 3-phase inverter is
    # ~0.5-0.6x phase RMS (5-6 A at 10 A/phase); at 20 kHz the 9x10uF MLCC
    # bank (~40 uF derated, ~0.2 ohm) leaves most of it to the electrolytics,
    # and one 13x20 mm can is rated ~1-2 A. Two halve it; the rest is a
    # continuous-current derating recorded in requirements.md.
    sh.add_component(f"{FP}:ERS1JM471K20OT", "C104", "470uF 63V",
                     at=(241.3, 63.5), footprint=f"{FP}:CAP-TH_BD13.0-P5.00-D1.2-FD")
    sh.wire_pins("C104", {"1": "VM", "2": "GND"})

    # ---- rails: this sheet OWNS VM and GND (the design's external entry
    # point - TP101/TP102 are the only truly external, passive-pin driven
    # nodes), so it carries the single PWR_FLAG for each across the whole
    # hierarchy. Every other sheet places these as flag=False consumers.
    sh.power_flag("VM", at=(38.1, 165.1), sym="power:VCC", flag=True)
    sh.power_flag("GND", at=(76.2, 165.1), sym="power:GND", flag=True)
    # VM_IN (raw input, pad-fed) drives U101 SOURCE, a power-input pin.
    sh.power_flag("VM_IN", at=(114.3, 165.1), flag=True)

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    for ref in BARE_PADS:
        sh.sch.components.get(ref).in_bom = False
    return sh


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else Path("/tmp/p18-power_in")
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
