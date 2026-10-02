"""esp32c3-node `power` sheet: B1 USB-C sink + protection, B2 MCP73831 charger
with AN1149 load sharing, B3 RT9080-33 LDO, battery sense divider.

SOURCE for kicad/power.kicad_sch (build output). Refdes ranges
(architecture/sheets.md): J1-J2, U2-U4, Q1-Q9, D1-D9, R1-R9, C1-C9;
pwr_base=100. Rails VBUS / VBAT / VSYS / +3V3 / GND are global power
symbols (bare names). Cross-sheet signals USB_DP, USB_DM, VBAT_SENSE leave
through hierarchical pins and become root labels /USB_DP, /USB_DM,
/VBAT_SENSE.

Pin ground truth (schlib --pins on lib/aiee.kicad_sym + parts/<lcsc>.json):
  J1 TYPE-C-31-M-12 (C165948): A4B9/B4A9 = VBUS, A1B12/B1A12 = GND (ganged
     pads), A5 CC1, B5 CC2, A6/B6 DP1/DP2, A7/B7 DN1/DN2, A8/B8 SBU, 1-4 EH
     shell legs -> GND.
  D1 SMF5.0A_C284108: pin 1 = cathode, pin 2 = anode (settled on PCB-0015
     for the same pulled symbol + SOD-123_L2.8 footprint, cathode band on
     pad 1).
  U4 USBLC6-2SC6 (C7519): 1/6 = I/O1 (internally common), 3/4 = I/O2,
     2 = GND, 5 = VBUS.
  U2 MCP73831T-2ACI/OT (C424093): 1 STAT, 2 VSS, 3 VBAT, 4 VDD, 5 PROG.
  Q1 AO3401A: 1 G, 2 S, 3 D.   D3 B5819W: 1 "-" cathode, 2 "+" anode.
  U3 RT9080-33GJ5 (C841192): 1 VIN, 2 GND, 3 EN, 4 NC, 5 VOUT.
  J2 S2B-PH-SM4-TB: 1, 2 contacts (1 = +), 3, 4 mechanical tabs.

Circuit (architecture/blocks.md, research/refdesign-charger-loadshare):
- Independent 5.1k Rd per CC pin; SMF5.0A at J1; USBLC6 on both D+/D- rows.
- RPROG 5.1k -> ~196 mA. STAT LED: VBUS -> R4 1k -> D2 -> STAT (lit while
  charging, STAT low).
- Load sharing (AN1149): Q1 PMOS drain VBAT, source VSYS, gate VBUS with R5
  100k to GND; D3 Schottky VBUS -> VSYS.
- U3 EN tied to VSYS (EN must not float, DS Enable). C3/C4 1 uF ceramics.
- R6/R7 1M/1M + C5 100 nF: VBAT/2 into U1 IO3.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BOARD = HERE.parents[2]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "hwde" / "scripts"))

import kicad_sch_api as ksa  # noqa: E402

sys.path.insert(0, str(HERE.parent))
import _libs  # noqa: E402

_libs.register(BOARD)

import schlib  # noqa: E402

FP = "aiee"

LCSC = {
    "J1": "C165948", "R1": "C23186", "R2": "C23186", "D1": "C284108",
    "U4": "C7519", "C1": "C19666", "U2": "C424093", "C2": "C19666",
    "R3": "C23186", "D2": "C2286", "R4": "C21190", "J2": "C295747",
    "Q1": "C15127", "R5": "C25803", "D3": "C8598", "U3": "C841192",
    "C3": "C15849", "C4": "C15849", "R6": "C22935", "R7": "C22935",
    "C5": "C14663",
}


def build() -> schlib.Sheet:
    sh = schlib.Sheet("power",
                      title="esp32c3-node: USB-C in, LiPo charger, power path, 3V3 LDO",
                      paper="A3", date="2026-10-01", company="ai-ee",
                      pwr_base=100)

    # ---- J1 USB-C receptacle (USB 2.0 device, default-USB sink) ---------
    sh.add_component("aiee:TYPE-C-31-M-12", "J1", "TYPE-C-31-M-12",
                     at=(50.80, 101.60),
                     footprint=f"{FP}:USB-C_SMD-TYPE-C-31-M-12_1",
                     expect={"A4B9": "VBUS", "B4A9": "VBUS",
                             "A1B12": "GND", "B1A12": "GND",
                             "A5": "CC1", "B5": "CC2", "A6": "DP1",
                             "B6": "DP2", "A7": "DN1", "B7": "DN2",
                             "A8": "SBU1", "B8": "SBU2",
                             "1": "EH", "2": "EH", "3": "EH", "4": "EH"})
    sh.wire_pins("J1", {
        "A4B9": "VBUS", "B4A9": "VBUS", "A1B12": "GND", "B1A12": "GND",
        "1": "GND", "2": "GND", "3": "GND", "4": "GND",
        "A5": "CC1", "B5": "CC2",
        # both rows of the reversible plug joined (sheets.md contract)
        "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
        # SBU: no alternate mode on a USB 2.0 device
        "A8": "NC", "B8": "NC",
    })

    # ---- CC: one independent 5.1k Rd per pin ----------------------------
    sh.add_component("aiee:0603WAF5101T5E", "R1", "5.1k 1%",
                     at=(101.60, 63.50), footprint=f"{FP}:R0603")
    sh.wire_pins("R1", {"1": "CC1", "2": "GND"})
    sh.add_component("aiee:0603WAF5101T5E", "R2", "5.1k 1%",
                     at=(101.60, 76.20), footprint=f"{FP}:R0603")
    sh.wire_pins("R2", {"1": "CC2", "2": "GND"})

    # ---- VBUS TVS at the receptacle (pin 1 cathode -> VBUS) -------------
    sh.add_component("aiee:SMF5.0A_C284108", "D1", "SMF5.0A",
                     at=(101.60, 101.60),
                     footprint=f"{FP}:SOD-123_L2.8-W1.8-LS3.7-RD")
    sh.wire_pins("D1", {"1": "VBUS", "2": "GND"})

    # ---- U4 USBLC6-2SC6 on D+/D- (pass-through 1<->6, 3<->4) ------------
    sh.add_component("aiee:USBLC6-2SC6", "U4", "USBLC6-2SC6",
                     at=(101.60, 139.70),
                     footprint=f"{FP}:SOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL")
    sh.wire_pins("U4", {"1": "USB_DP", "6": "USB_DP",
                        "3": "USB_DM", "4": "USB_DM",
                        "2": "GND", "5": "VBUS"})

    # ---- U2 MCP73831 charger --------------------------------------------
    # C1 4.7u at VDD (also the receptacle bulk; total <= 10 uF at J1),
    # C2 4.7u at VBAT (DS: >= 4.7 uF output for stability without battery).
    sh.place_ic_with_decoupling(
        "U2", "aiee:MCP73831T-2ACI_OT", "MCP73831T-2ACI/OT",
        at=(165.10, 76.20),
        pins={"1": "CHG_STAT", "2": "GND", "3": "VBAT", "4": "VBUS",
              "5": "PROG"},
        footprint=f"{FP}:SOT-23-5_L3.0-W1.7-P0.95-LS2.8-BL",
        expect={"1": "STAT", "2": "VSS", "3": "VBAT", "4": "VDD",
                "5": "PROG"},
        decoupling=[
            {"cap": "C1", "pin": "4", "rail": "VBUS", "value": "4.7uF 16V X5R",
             "lib_id": "aiee:CL10A475KO8NNNC", "footprint": f"{FP}:C0603"},
            {"cap": "C2", "pin": "3", "rail": "VBAT", "value": "4.7uF 16V X5R",
             "lib_id": "aiee:CL10A475KO8NNNC", "footprint": f"{FP}:C0603"},
        ],
        caps_at=(152.40, 127.00), caps_dx=20.32)
    sh.add_component("aiee:0603WAF5101T5E", "R3", "5.1k 1% (RPROG)",
                     at=(215.90, 50.80), footprint=f"{FP}:R0603")
    sh.wire_pins("R3", {"1": "PROG", "2": "GND"})
    # STAT LED: VBUS -> R4 -> D2 anode, D2 cathode -> STAT (sinks to light)
    sh.add_component("aiee:0603WAF1001T5E", "R4", "1k",
                     at=(215.90, 76.20), footprint=f"{FP}:R0603")
    sh.wire_pins("R4", {"1": "VBUS", "2": "CHG_LED_A"})
    sh.add_component("aiee:KT-0603R", "D2", "Red LED (charging)",
                     at=(215.90, 101.60),
                     footprint=f"{FP}:LED-SMD_L1.6-W0.8-R-RD",
                     expect={"1": "A", "2": "K"})
    sh.wire_pins("D2", {"1": "CHG_LED_A", "2": "CHG_STAT"})

    # ---- J2 LiPo JST-PH 2-pin (pin 1 = +) -------------------------------
    sh.add_component("aiee:S2B-PH-SM4-TB", "J2", "JST-PH 2P LiPo",
                     at=(266.70, 50.80),
                     footprint=f"{FP}:CONN-SMD_P2.00_S2B-PH-SM4-TB-LF-SN")
    # 3/4 are the mechanical reinforcement tabs - no electrical function
    sh.wire_pins("J2", {"1": "VBAT", "2": "GND", "3": "NC", "4": "NC"})

    # ---- load sharing (AN1149) -----------------------------------------
    sh.add_component("aiee:AO3401A", "Q1", "AO3401A",
                     at=(266.70, 88.90),
                     footprint=f"{FP}:SOT-23_L2.9-W1.3-P1.90-LS2.4-BR",
                     expect={"1": "G", "2": "S", "3": "D"})
    sh.wire_pins("Q1", {"1": "VBUS", "2": "VSYS", "3": "VBAT"})
    sh.add_component("aiee:0603WAF1003T5E", "R5", "100k",
                     at=(266.70, 114.30), footprint=f"{FP}:R0603")
    sh.wire_pins("R5", {"1": "VBUS", "2": "GND"})
    sh.add_component("aiee:B5819W_C8598", "D3", "B5819W",
                     at=(266.70, 139.70),
                     footprint=f"{FP}:SOD-123_L2.7-W1.6-LS3.7-RD-1",
                     expect={"1": "-", "2": "+"})
    sh.wire_pins("D3", {"2": "VBUS", "1": "VSYS"})

    # ---- U3 RT9080-33 LDO ------------------------------------------------
    sh.place_ic_with_decoupling(
        "U3", "aiee:RT9080-33GJ5", "RT9080-33GJ5",
        at=(330.20, 76.20),
        pins={"1": "VSYS", "2": "GND", "3": "VSYS", "4": "NC",
              "5": "+3V3"},
        footprint=f"{FP}:TSOT-23-5_L2.9-W1.6-P0.95-LS2.8-BL",
        expect={"1": "VIN", "2": "GND", "3": "EN", "4": "NC", "5": "VOUT"},
        decoupling=[
            {"cap": "C3", "pin": "1", "rail": "VSYS", "value": "1uF 50V X7R",
             "lib_id": "aiee:CL10A105KB8NNNC", "footprint": f"{FP}:C0603"},
            {"cap": "C4", "pin": "5", "rail": "+3V3", "value": "1uF 50V X7R",
             "lib_id": "aiee:CL10A105KB8NNNC", "footprint": f"{FP}:C0603"},
        ],
        caps_at=(317.50, 127.00), caps_dx=20.32)

    # ---- battery sense divider -> U1 IO3 ---------------------------------
    sh.add_component("aiee:0603WAF1004T5E", "R6", "1M 1%",
                     at=(152.40, 177.80), footprint=f"{FP}:R0603")
    sh.wire_pins("R6", {"1": "VBAT", "2": "VBAT_SENSE"})
    sh.add_component("aiee:0603WAF1004T5E", "R7", "1M 1%",
                     at=(177.80, 177.80), footprint=f"{FP}:R0603")
    sh.wire_pins("R7", {"1": "VBAT_SENSE", "2": "GND"})
    sh.add_component("aiee:CC0603KRX7R9BB104", "C5", "100nF 50V X7R",
                     at=(203.20, 177.80), footprint=f"{FP}:C0603")
    sh.wire_pins("C5", {"1": "VBAT_SENSE", "2": "GND"})

    # ---- cross-sheet signals --------------------------------------------
    sh.hier_pin("USB_DP", shape="bidirectional", at=(50.80, 228.60))
    sh.hier_pin("USB_DM", shape="bidirectional", at=(50.80, 241.30))
    sh.hier_pin("VBAT_SENSE", shape="output", at=(50.80, 254.00))

    # ---- rails -----------------------------------------------------------
    # VBUS, VSYS, GND see only passive/power_in pins -> PWR_FLAG here.
    # VBAT is driven by U2 pin 3 and +3V3 by U3 pin 5 (power_out): no flag.
    sh.power_flag("VBUS", at=(127.00, 228.60), sym="power:VBUS", flag=True)
    sh.power_flag("VSYS", at=(127.00, 241.30), sym="power:VBUS", flag=True)
    sh.power_flag("GND", at=(127.00, 254.00), sym="power:GND", flag=True)
    sh.power_flag("VBAT", at=(190.50, 228.60), sym="power:VBUS", flag=False)
    sh.power_flag("+3V3", at=(190.50, 241.30), sym="power:+3V3", flag=False)

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    return sh


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else HERE.parents[1]
    try:
        sh = build()
        sch = sh.save(out_dir, project=False)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"script": "gen.power_sheet", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({"script": "gen.power_sheet", "status": "pass",
                      "files": [str(sch)], "hier_pins": sorted(sh.hier_pins),
                      "decoupling_associations": len(sh.decoupling)}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
