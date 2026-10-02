"""PCB-0021-A lipo-boost: single flat sheet (BQ24074 charger + TPS61023 boost).

Every pin number is from parts/C54313.json (BQ24074 RGT), parts/C919459.json
(TPS61023 DRL), parts/C45367187.json (MSXC61 SOT-23-3: 1 VOUT, 2 VSS, 3 VIN),
and the pulled lib symbols. Run with the hwde venv from skill scripts/:
    python <ws>/kicad/gen/lipo_boost.py
Writes kicad/PCB-0021-A_lipo-boost.kicad_sch + kicad/decoupling.json.
"""
from __future__ import annotations

import sys
from pathlib import Path

import kicad_sch_api as ksa

SKILL = Path(".claude/skills/hwde/scripts")
sys.path.insert(0, str(SKILL))
import schlib  # noqa: E402

BOARD = Path(__file__).resolve().parents[2]
ksa.get_symbol_cache().add_library_path(BOARD / "lib" / "aiee.kicad_sym")
NAME = "PCB-0021-A_lipo-boost"

s = schlib.Sheet(NAME, title="PCB-0021-A lipo-boost", paper="A3", pwr_base=100)

R = {  # value -> (lib symbol, lcsc)
    "10k": ("0603WAF1002T5E", "C25804"), "1k": ("0603WAF1001T5E", "C21190"),
    "1.2k": ("0603WAF1201T5E", "C22765"), "51k": ("0603WAF5102T5E", "C23196"),
    "470R": ("0603WAF4700T5E", "C23179"), "100k": ("0603WAF1003T5E", "C25803"),
    "732k": ("0603WAF7323T5E", "C23239"), "0R": ("0603WAF0000T5E", "C21189"),
}
C = {
    "4.7uF 25V X5R": ("CL21A475KAQNNNE", "C1779", "aiee:C0805"),
    "10uF 25V X5R": ("CL21A106KAYNNNE", "C15850", "aiee:C0805"),
    "22uF 25V X5R": ("CL21A226MAQNNNE", "C45783", "aiee:C0805"),
    "100nF 50V X7R": ("CC0603KRX7R9BB104", "C14663", "aiee:C0603"),
}
LCSC: dict[str, str] = {}


def cap(ref, v, rail, pin, **kw):
    sym, lcsc, fp = C[v]
    LCSC[ref] = lcsc
    d = {"cap": ref, "pin": pin, "rail": rail, "value": v,
         "lib_id": f"aiee:{sym}", "footprint": fp}
    d.update(kw)
    return d


def res(ref, v, x, y, p1, p2):
    sym, lcsc = R[v]
    LCSC[ref] = lcsc
    s.add_component(f"aiee:{sym}", ref, v, (x, y), footprint="aiee:R0603")
    s.wire_pins(ref, {"1": p1, "2": p2})


def part(ref, sym, value, lcsc, at, pins, fp=None, rot=0):
    LCSC[ref] = lcsc
    s.add_component(f"aiee:{sym}", ref, value, at, footprint=fp, rotation=rot)
    s.wire_pins(ref, pins)


# ---- U1 BQ24074 charger / power path ----
LCSC["U1"] = "C54313"
s.place_ic_with_decoupling(
    "U1", "aiee:BQ24074RGTR", "BQ24074RGTR", (127.0, 76.2),
    pins={"1": "TS", "2": "VBAT", "3": "VBAT", "4": "GND", "5": "+SYS",
          "6": "GND", "7": "PGOOD", "8": "GND", "9": "CHG", "10": "+SYS",
          "11": "+SYS", "12": "ILIM", "13": "VBUS", "14": "TMR",
          "15": "NC",  # ITERM open = default 10 % termination (datasheet)
          "16": "ISET", "17": "GND"},
    footprint="aiee:QFN-16_L3.0-W3.0-P0.50-TL-EP1.7",
    decoupling=[cap("C1", "4.7uF 25V X5R", "VBUS", "13"),
                cap("C4", "100nF 50V X7R", "VBUS", "13"),
                cap("C2", "10uF 25V X5R", "+SYS", "10"),
                cap("C3", "10uF 25V X5R", "VBAT", "2")],
    caps_at=(76.2, 127.0), caps_dx=25.4,
    expect={"1": "TS", "4": "CE", "5": "EN2", "6": "EN1", "7": "PGOOD",
            "9": "CHG", "12": "ILIM", "13": "IN", "14": "TMR", "15": "ITERM",
            "16": "ISET", "10": "OUT", "2": "BAT", "8": "VSS"})
res("R1", "10k", 177.8, 127.0, "TS", "GND")     # no NTC: fixed 10k
res("R2", "1.2k", 203.2, 127.0, "ILIM", "GND")   # ILIM mode input limit
res("R3", "1k", 228.6, 127.0, "ISET", "GND")     # fast charge ~0.89 A
res("R4", "51k", 254.0, 127.0, "TMR", "GND")     # safety timers

# ---- U2 TPS61023 boost ----
LCSC["U2"] = "C919459"
s.place_ic_with_decoupling(
    "U2", "aiee:TPS61023DRLR", "TPS61023DRLR", (254.0, 76.2),
    pins={"1": "FB", "2": "EN", "3": "+SYS", "4": "GND", "5": "SW",
          "6": "+5V"},
    footprint="aiee:SOT-563_L1.6-W1.2-P0.50-LS1.6-BR",
    decoupling=[cap("C10", "10uF 25V X5R", "+SYS", "3", role="reg_input"),
                cap("C14", "100nF 50V X7R", "+SYS", "3", role="reg_input"),
                cap("C11", "22uF 25V X5R", "+5V", "6"),
                cap("C12", "22uF 25V X5R", "+5V", "6"),
                cap("C13", "100nF 50V X7R", "+5V", "6")],
    caps_at=(215.9, 165.1), caps_dx=25.4,
    expect={"1": "FB", "2": "EN", "3": "VIN", "4": "GND", "5": "SW",
            "6": "VOUT"})
part("L1", "FHD4020S-1R0MT", "1uH", "C602028", (215.9, 203.2),
     {"1": "+SYS", "2": "SW"}, fp="aiee:IND-SMD_L4.0-W4.0")
res("R9", "100k", 241.3, 203.2, "+SYS", "EN")    # EN pull-up
res("R10", "732k", 266.7, 203.2, "+5V", "FB")    # FB top
res("R11", "100k", 292.1, 203.2, "FB", "GND")    # FB bottom

# ---- U3 low-battery detector + LEDs + Q1 ----
part("U3", "MSXC61CN3302MR", "MSXC61CN3302MR", "C45367187", (76.2, 203.2),
     {"1": "LBO", "2": "GND", "3": "VBAT"},
     fp="aiee:SOT-23-3_L2.9-W1.6-P1.90-LS2.8-BR")
part("Q1", "2N7002", "2N7002", "C8545", (177.8, 203.2),
     {"1": "CHG", "2": "PGOOD", "3": "DONE_K"},
     fp="aiee:SOT-23-3_L2.9-W1.3-P1.90-LS2.4-BR")
res("R8", "100k", 127.0, 203.2, "+SYS", "CHG")   # Q1 gate pull-up
res("R5", "1k", 25.4, 165.1, "+SYS", "CHG_A")
part("D1", "ORH-R36A", "ORH-R36A orange", "C205445", (50.8, 165.1),
     {"1": "CHG", "2": "CHG_A"}, fp="aiee:LED0603-RD")       # pin1 K, pin2 A
res("R6", "470R", 76.2, 165.1, "+SYS", "DONE_A")
part("D2", "0603Green509-620mcd", "KT-0603G green", "C12624", (101.6, 165.1),
     {"1": "DONE_K", "2": "DONE_A"}, fp="aiee:LED0603-RD")   # pin1 K, pin2 A
res("R7", "1k", 127.0, 165.1, "+SYS", "LB_A")
part("D3", "KT-0603R", "KT-0603R red", "C2286", (152.4, 165.1),
     {"1": "LB_A", "2": "LBO"}, fp="aiee:LED-SMD_L1.6-W0.8-R-RD")  # 1 A, 2 K

# ---- connectors ----
part("J1", "MICROXNJ", "MicroXNJ", "C404969", (38.1, 50.8),
     {"1": "VBUS", "2": "NC", "3": "NC", "4": "NC", "5": "GND", "6": "GND",
      "7": "GND", "8": "GND", "9": "GND"},
     fp="aiee:MICRO-USB-SMD_MICROXNJ_1")
part("J2", "S2B-PH-SM4-TB", "S2B-PH-SM4-TB(LF)(SN)", "C295747",
     (38.1, 101.6), {"1": "VBAT", "2": "GND", "3": "NC", "4": "NC"},
     fp="aiee:CONN-SMD_P2.00_S2B-PH-SM4-TB-LF-SN")
part("J3", "HXPZ2.54-1X7PZZ", "HX PZ2.54-1x7P", "C32713273", (381.0, 76.2),
     {"1": "GND", "2": "VBAT", "3": "+SYS", "4": "+5V", "5": "LBO",
      "6": "EN", "7": "GND"}, fp="aiee:HDR-TH_7P-P2.54-V-M")
part("J4", "TYPE-A-AF90", "Type-A-AF90", "C53207796", (381.0, 152.4),
     {"1": "+5V", "2": "USB_DM", "3": "USB_DP", "4": "GND", "5": "GND",
      "6": "GND"}, fp="aiee:USB-A-TH_U-A-24DD-Y-13")
res("R12", "0R", 330.2, 228.6, "USB_DP", "USB_DM")   # R_DCP

# ---- rails (global power symbols; PWR_FLAG only where nothing drives) ----
s.power_flag("GND", (25.4, 254.0), "power:GND")
s.power_flag("VBUS", (63.5, 254.0), "power:VBUS")
s.power_flag("VBAT", (101.6, 254.0), "power:+BATT")
s.power_flag("+SYS", (139.7, 254.0), "power:+5V", flag=False)  # U1 OUT drives
s.power_flag("+5V", (177.8, 254.0), "power:+5V", flag=False)   # U2 VOUT drives

for ref, lcsc in LCSC.items():
    s.sch.components.get(ref).set_property("LCSC Part", lcsc)

out = BOARD / "kicad"
p = s.save(out)
s.emit_decoupling(out / "decoupling.json")
print("wrote", p)
