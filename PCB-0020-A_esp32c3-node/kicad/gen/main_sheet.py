"""esp32c3-node `main` sheet: B4 ESP32-C3-MINI-1-N4 module (EN RC, RESET,
BOOT, straps, status LED, edge pads) + B5 BME280 and the Qwiic port.

SOURCE for kicad/main.kicad_sch (build output). Refdes ranges
(architecture/sheets.md): U1, U5-U9, J3-J9, D10-D19, R10-R19, C10-C19,
SW1-SW9; pwr_base=200. +3V3 / GND / VBUS / VBAT are global power symbols.
Cross-sheet signals arrive as hierarchical pins USB_DP, USB_DM, VBAT_SENSE.

Pin ground truth (schlib --pins + parts/C2838502.json, DS Table 3-1):
  U1 1,2,11,14,36-53 GND (49 = EPAD); 3 3V3; 8 EN; 5 IO2; 6 IO3; 12 IO0;
     13 IO1; 16 IO10; 18 IO4; 19 IO5; 20 IO6; 21 IO7; 22 IO8; 23 IO9;
     26 IO18 (USB D-); 27 IO19 (USB D+); 30 RXD0 (GPIO20); 31 TXD0 (GPIO21);
     4,7,9,10,15,17,24,25,28,29,32-35 NC (no-connect flags).
  U5 BME280 (C92489): 1 GND, 2 CSB, 3 SDI, 4 SCK, 5 SDO, 6 VDDIO, 7 GND,
     8 VDD. I2C: CSB tied to VDDIO (DS Fig 17 "direct connection"), SDO to
     GND -> address 0x76.
  SW1/SW2 TS-1187A: pins 1+2 one terminal, 3+4 the other.
  J3 SM04B-SRSS-TB Qwiic: 1 GND, 2 3V3, 3 SDA, 4 SCL; 5/6 mechanical tabs.
  J4/J5 0.1 in edge pads, footprint only (DNP): stock Conn_01x08 / Conn_01x04.

Straps (DS Sec 3.3, research/refdesign-esp32c3-module): IO9 high = SPI
boot (R11 10k + SW2 to GND for download), IO8 must be high for download
(R12 10k), IO2 high (R13 10k). EN: R10 10k / C12 1 uF RC + SW1 (DS p34).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BOARD = HERE.parents[2]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "hwde" / "scripts"))
sys.path.insert(0, str(HERE.parent))

import _libs  # noqa: E402

_libs.register(BOARD)

import schlib  # noqa: E402

FP = "aiee"
V_100N = "100nF 50V X7R"

U1_PINS = {
    "3": "+3V3", "8": "EN",
    "5": "IO2", "6": "VBAT_SENSE", "12": "IO0", "13": "IO1",
    "16": "LED", "18": "IO4", "19": "IO5", "20": "SDA", "21": "SCL",
    "22": "IO8", "23": "BOOT", "26": "USB_DM", "27": "USB_DP",
    "30": "IO20", "31": "IO21",
}
for _p in [1, 2, 11, 14] + list(range(36, 54)):
    U1_PINS[str(_p)] = "GND"
for _p in [4, 7, 9, 10, 15, 17, 24, 25, 28, 29, 32, 33, 34, 35]:
    U1_PINS[str(_p)] = "NC"   # module NC pads (DS Table 3-1)

LCSC = {
    "U1": "C2838502", "C10": "C15850", "C11": "C14663",
    "R10": "C25804", "C12": "C15849", "SW1": "C318884", "SW2": "C318884",
    "R11": "C25804", "R12": "C25804", "R13": "C25804",
    "D10": "C2297", "R16": "C21190",
    "U5": "C92489", "C13": "C14663", "C14": "C14663",
    "R14": "C23162", "R15": "C23162", "J3": "C160404",
}


def build() -> schlib.Sheet:
    sh = schlib.Sheet("main",
                      title="esp32c3-node: ESP32-C3-MINI-1 module, BME280, Qwiic, edge pads",
                      paper="A3", date="2026-10-01", company="ai-ee",
                      pwr_base=200)

    # ---- U1 module + 10 uF / 100 nF at 3V3 (DS Fig 9-1) ------------------
    sh.place_ic_with_decoupling(
        "U1", "aiee:ESP32-C3-MINI-1-N4", "ESP32-C3-MINI-1-N4",
        at=(203.20, 127.00), pins=U1_PINS,
        footprint=f"{FP}:WIFIM-SMD_ESP32-C3-MINI-1",
        expect={"3": "3V3", "8": "EN", "5": "IO2", "6": "IO3", "12": "IO0",
                "13": "IO1", "16": "IO10", "18": "IO4", "19": "IO5",
                "20": "IO6", "21": "IO7", "22": "IO8", "23": "IO9",
                "26": "IO18", "27": "IO19", "30": "RXD0", "31": "TXD0",
                "49": "GND"},
        decoupling=[
            {"cap": "C10", "pin": "3", "rail": "+3V3", "value": "10uF 25V X5R",
             "lib_id": "aiee:CL21A106KAYNNNE", "footprint": f"{FP}:C0805"},
            {"cap": "C11", "pin": "3", "rail": "+3V3", "value": V_100N,
             "lib_id": "aiee:CC0603KRX7R9BB104", "footprint": f"{FP}:C0603"},
        ],
        caps_at=(50.80, 241.30), caps_dx=20.32)

    # ---- EN: 10k / 1 uF RC + RESET button ---------------------------------
    sh.add_component("aiee:0603WAF1002T5E", "R10", "10k",
                     at=(50.80, 50.80), footprint=f"{FP}:R0603")
    sh.wire_pins("R10", {"1": "+3V3", "2": "EN"})
    sh.add_component("aiee:CL10A105KB8NNNC", "C12", "1uF 50V X7R",
                     at=(76.20, 50.80), footprint=f"{FP}:C0603")
    sh.wire_pins("C12", {"1": "EN", "2": "GND"})
    sh.add_component("aiee:TS-1187A-B-A-B", "SW1", "RESET",
                     at=(50.80, 76.20),
                     footprint=f"{FP}:SW-SMD_4P-L5.1-W5.1-P3.70-LS6.5-TL_H1.5",
                     expect={"1": "A", "2": "B", "3": "C", "4": "D"})
    sh.wire_pins("SW1", {"1": "EN", "2": "EN", "3": "GND", "4": "GND"})

    # ---- BOOT (IO9) + strap pull-ups ------------------------------------
    sh.add_component("aiee:TS-1187A-B-A-B", "SW2", "BOOT",
                     at=(50.80, 101.60),
                     footprint=f"{FP}:SW-SMD_4P-L5.1-W5.1-P3.70-LS6.5-TL_H1.5",
                     expect={"1": "A", "2": "B", "3": "C", "4": "D"})
    sh.wire_pins("SW2", {"1": "BOOT", "2": "BOOT", "3": "GND", "4": "GND"})
    sh.add_component("aiee:0603WAF1002T5E", "R11", "10k",
                     at=(50.80, 127.00), footprint=f"{FP}:R0603")
    sh.wire_pins("R11", {"1": "+3V3", "2": "BOOT"})
    sh.add_component("aiee:0603WAF1002T5E", "R12", "10k",
                     at=(50.80, 152.40), footprint=f"{FP}:R0603")
    sh.wire_pins("R12", {"1": "+3V3", "2": "IO8"})
    sh.add_component("aiee:0603WAF1002T5E", "R13", "10k",
                     at=(50.80, 177.80), footprint=f"{FP}:R0603")
    sh.wire_pins("R13", {"1": "+3V3", "2": "IO2"})

    # ---- status LED on IO10 (not a strap) ---------------------------------
    sh.add_component("aiee:0603WAF1001T5E", "R16", "1k",
                     at=(101.60, 203.20), footprint=f"{FP}:R0603")
    sh.wire_pins("R16", {"1": "LED", "2": "LED_A"})
    sh.add_component("aiee:0805G", "D10", "Green LED (status)",
                     at=(127.00, 203.20), footprint=f"{FP}:LED0805-R-RD",
                     expect={"1": "A", "2": "K"})
    sh.wire_pins("D10", {"1": "LED_A", "2": "GND"})

    # ---- U5 BME280 (I2C, 0x76) --------------------------------------------
    sh.place_ic_with_decoupling(
        "U5", "aiee:BME280", "BME280",
        at=(330.20, 76.20),
        pins={"1": "GND", "2": "+3V3", "3": "SDA", "4": "SCL", "5": "GND",
              "6": "+3V3", "7": "GND", "8": "+3V3"},
        footprint=f"{FP}:LGA-8_BME280_BL",
        expect={"1": "GND", "2": "CSB", "3": "SDI", "4": "SCK", "5": "SDO",
                "6": "VDDIO", "7": "GND", "8": "VDD"},
        decoupling=[
            {"cap": "C13", "pin": "8", "rail": "+3V3", "value": V_100N,
             "lib_id": "aiee:CC0603KRX7R9BB104", "footprint": f"{FP}:C0603"},
            {"cap": "C14", "pin": "6", "rail": "+3V3", "value": V_100N,
             "lib_id": "aiee:CC0603KRX7R9BB104", "footprint": f"{FP}:C0603"},
        ],
        caps_at=(317.50, 127.00), caps_dx=20.32)
    sh.add_component("aiee:0603WAF4701T5E", "R14", "4.7k",
                     at=(279.40, 50.80), footprint=f"{FP}:R0603")
    sh.wire_pins("R14", {"1": "+3V3", "2": "SDA"})
    sh.add_component("aiee:0603WAF4701T5E", "R15", "4.7k",
                     at=(279.40, 76.20), footprint=f"{FP}:R0603")
    sh.wire_pins("R15", {"1": "+3V3", "2": "SCL"})

    # ---- J3 Qwiic (fixed pin order: GND, 3V3, SDA, SCL) -------------------
    sh.add_component("aiee:SM04B-SRSS-TB", "J3", "Qwiic JST-SH 4P",
                     at=(368.30, 165.10),
                     footprint=f"{FP}:CONN-SMD_4P-P1.00_SM04B-SRSS-TB-LF-SN")
    sh.wire_pins("J3", {"1": "GND", "2": "+3V3", "3": "SDA", "4": "SCL",
                        "5": "NC", "6": "NC"})   # 5/6 mechanical tabs

    # ---- J4 GPIO edge pads, J5 power pads (footprint only, DNP) -----------
    sh.add_component("Connector_Generic:Conn_01x08", "J4", "GPIO edge pads",
                     at=(368.30, 215.90),
                     footprint=f"{FP}:PinHeader_1x08_P2.54mm_Vertical")
    sh.wire_pins("J4", {"1": "IO0", "2": "IO1", "3": "IO2", "4": "IO4",
                        "5": "IO5", "6": "IO8", "7": "IO20", "8": "IO21"})
    sh.add_component("Connector_Generic:Conn_01x04", "J5", "Power pads",
                     at=(368.30, 254.00),
                     footprint=f"{FP}:PinHeader_1x04_P2.54mm_Vertical")
    sh.wire_pins("J5", {"1": "VBUS", "2": "VBAT", "3": "+3V3", "4": "GND"})

    # ---- cross-sheet signals --------------------------------------------
    sh.hier_pin("USB_DP", shape="bidirectional", at=(101.60, 254.00))
    sh.hier_pin("USB_DM", shape="bidirectional", at=(101.60, 266.70))
    sh.hier_pin("VBAT_SENSE", shape="input", at=(101.60, 279.40))

    # ---- rails (flags live on the power sheet) ----------------------------
    sh.power_flag("+3V3", at=(165.10, 254.00), sym="power:+3V3", flag=False)
    sh.power_flag("GND", at=(165.10, 266.70), sym="power:GND", flag=False)
    sh.power_flag("VBUS", at=(228.60, 254.00), sym="power:VBUS", flag=False)
    sh.power_flag("VBAT", at=(228.60, 266.70), sym="power:VBUS", flag=False)

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    for ref in ("J4", "J5"):
        sh.mark_dnp(ref)
    return sh


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else HERE.parents[1]
    try:
        sh = build()
        sch = sh.save(out_dir, project=False)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"script": "gen.main_sheet", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({"script": "gen.main_sheet", "status": "pass",
                      "files": [str(sch)], "hier_pins": sorted(sh.hier_pins),
                      "decoupling_associations": len(sh.decoupling)}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
