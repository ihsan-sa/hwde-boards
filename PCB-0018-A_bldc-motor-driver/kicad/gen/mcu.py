"""PCB-0018-A `mcu` sheet: STM32G431CBT6 (U601) + decoupling, SWD header
J601, reset/user switches SW601/SW602, status LEDs D601-D603.

Refdes range (architecture/sheets.md): base 600 -> U601, J601, SW601/SW602,
D601-D603, R6xx, C6xx, #PWR06xx via pwr_base=600.

GROUND TRUTH for every pin number/name below is
architecture/mcu_pinmap.md (P3 orchestrator pin assignment, itself grounded
in parts/C529355.json DS12589 Table 12) - never memory.

Net naming (sheets.md): power rails (+3V3, GND) are GLOBAL power symbols,
made global here via power_symbol_at_pin on U601's own supply pins (the
lumina-carrier mcu.py idiom: a plain same-name label on this sheet already
merges with those pins, so downstream connectors/caps just use the bare
"+3V3"/"GND" label). VDDA is NOT a rail: it is this sheet's own hier pin,
already filtered upstream by the regulators-sheet ferrite (see OPEN note on
the FB parts.json/sheets.md mismatch) and decoupled locally per mcu_pinmap.
Every other cross-sheet net is a hierarchical pin with the exact bare name
from sheets.md (no leading slash); this sheet exposes them with the
free-cluster hier_pin variant (local label merges with the already-wired
MCU pin by NAME on this sheet; hier label crosses to the root as "/NAME").

Rebuild standalone (root generator is authoritative for the whole project):
    ~/.local/hwde-venv/bin/python PCB-0018-A_bldc-motor-driver/kicad/gen/mcu.py
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

# KiCad 10 stock libraries (power:*, Device:*): kicad-sch-api discovers
# KICAD_SYMBOL_DIR / KICAD9_SYMBOL_DIR only, not the KICAD10_SYMBOL_DIR the
# hwde env exports - alias it before the cache is first built (see
# PCB-0017-A_astra-amp/kicad/gen/root.py).
if not os.environ.get("KICAD_SYMBOL_DIR"):
    for _cand in (os.environ.get("KICAD10_SYMBOL_DIR"),
                  str(Path.home() / ".local/kicad10/usr/share/kicad/symbols")):
        if _cand and Path(_cand).is_dir():
            os.environ["KICAD_SYMBOL_DIR"] = _cand
            break

import kicad_sch_api as ksa  # noqa: E402

ksa.get_symbol_cache().add_library_path(BOARD / "lib" / "aiee.kicad_sym")

import schlib  # noqa: E402

NAME = "mcu"
FP = "aiee"
C0603 = f"{FP}:C0603"
C0805 = f"{FP}:C0805"
R0603 = f"{FP}:R0603"
LED0603 = f"{FP}:LED-SMD_L1.6-W0.8-R-RD"

# parts/parts.json (P3, live-verified 2026-09-27), block "mcu" unless noted.
LCSC = {
    "U601": "C529355",           # STM32G431CBT6
    "C601": "C14663", "C602": "C14663", "C603": "C14663",   # 100nF VDD
    "C604": "C1779",             # 4.7uF bulk, CL21A475KAQNNNE
    "C605": "C28323",            # 1uF VDDA, CL21B105KBFNNNE
    "C606": "C57112",            # 10nF VDDA - see OPEN: not in parts.json
    "C607": "C28323",            # 1uF VREF+
    "C608": "C14663",            # 100nF VREF+
    "C609": "C14663",            # 100nF NRST
    "C610": "C14663",            # 100nF SW602 debounce
    "R601": "C25804",            # 10k BOOT0 pull-down, 0603WAF1002T5E
    "SW601": "C720477", "SW602": "C720477",   # TS-1088-AR02016 x2
    "J601": "C2935458",          # PZ127VS-12-10-H10-A38, 2x5 1.27mm SWD
    "R602": "C21190", "R603": "C21190", "R604": "C21190",   # 1k LED series
    "D601": "C12624",            # KT-0603G green - power LED (symbol reuse, see below)
    "D602": "C2287",             # KT-0603Y yellow - status LED (symbol reuse)
    "D603": "C2286",             # KT-0603R red - fault LED (exact symbol match)
}

# U601 pad -> net, from architecture/mcu_pinmap.md verbatim. "NC" pads are
# the pinmap's explicit unused list (PC14/PC15/PF0/PF1: no crystal fitted;
# PA5/PA6/PA11/PA12/PB1/PB2: not used by this design's GPIO budget).
U601_PINS = {
    "1": "+3V3",          # VBAT tied to VDD - no RTC battery (pinmap)
    "2": "USER_SW",        # PC13, SW602 to GND, firmware internal pull-up
    "3": "NC", "4": "NC",  # PC14-OSC32_IN / PC15-OSC32_OUT, no crystal
    "5": "NC", "6": "NC",  # PF0-OSC_IN / PF1-OSC_OUT, HSI clock, no crystal
    "7": "NRST",           # PG10-NRST
    "8": "VBUS_SENSE",     # PA0, ADC12_IN1
    "9": "ISENSE_A",       # PA1, ADC12_IN2 + COMP1_INP
    "10": "VSENSE_A",      # PA2, ADC1_IN3
    "11": "VSENSE_B",      # PA3, ADC1_IN4
    "12": "VSENSE_C",      # PA4, ADC2_IN17
    "13": "NC", "14": "NC",   # PA5, PA6 - unused
    "15": "ISENSE_B",      # PA7, ADC2_IN4 + COMP2_INP
    "16": "ISENSE_C",      # PB0, ADC1_IN15 + COMP4_INP
    "17": "NC", "18": "NC",   # PB1, PB2 - unused
    "19": "GND",           # VSSA
    "20": "VDDA",          # VREF+ tied to VDDA (no VREFBUF), pinmap
    "21": "VDDA",          # VDDA
    "22": "HALL_C",        # PB10, TIM2_CH3
    "23": "GND",           # VSS
    "24": "+3V3",          # VDD
    "25": "LED_STATUS",    # PB11 -> D602 via R603
    "26": "LED_FAULT",     # PB12 -> D603 via R604
    "27": "INLA",          # PB13, TIM1_CH1N
    "28": "INLB",          # PB14, TIM1_CH2N
    "29": "INLC",          # PB15, TIM1_CH3N
    "30": "INHA",          # PA8, TIM1_CH1
    "31": "INHB",          # PA9, TIM1_CH2
    "32": "INHC",          # PA10, TIM1_CH3
    "33": "NC", "34": "NC",   # PA11, PA12 - unused
    "35": "GND",           # VSS
    "36": "+3V3",          # VDD
    "37": "SWDIO",         # PA13 -> J601 pin 2
    "38": "SWCLK",         # PA14 -> J601 pin 4
    "39": "HALL_A",        # PA15, TIM2_CH1
    "40": "HALL_B",        # PB3, TIM2_CH2 (JTDO freed: SWD-only debug)
    "41": "ENC_A",         # PB4, TIM3_CH1 (JTRST freed)
    "42": "ENC_B",         # PB5, TIM3_CH2
    "43": "UART_TX",       # PB6, USART1_TX
    "44": "UART_RX",       # PB7, USART1_RX
    "45": "BOOT0",         # PB8-BOOT0, 10k pull-down -> boot from flash
    "46": "ENC_Z",         # PB9, GPIO/EXTI9, index pulse
    "47": "GND",           # VSS
    "48": "+3V3",          # VDD
}
U601_EXPECT = {
    "1": "VBAT", "2": "PC13", "3": "PC14-OSC32_IN", "4": "PC15-OSC32_OUT",
    "5": "PF0-OSC_IN", "6": "PF1-OSC_OUT", "7": "PG10-NRST", "8": "PA0",
    "9": "PA1", "10": "PA2", "11": "PA3", "12": "PA4", "13": "PA5",
    "14": "PA6", "15": "PA7", "16": "PB0", "17": "PB1", "18": "PB2",
    "19": "VSSA", "20": "VREF+", "21": "VDDA", "22": "PB10", "23": "VSS",
    "24": "VDD", "25": "PB11", "26": "PB12", "27": "PB13", "28": "PB14",
    "29": "PB15", "30": "PA8", "31": "PA9", "32": "PA10", "33": "PA11",
    "34": "PA12", "35": "VSS", "36": "VDD", "37": "PA13", "38": "PA14",
    "39": "PA15", "40": "PB3", "41": "PB4", "42": "PB5", "43": "PB6",
    "44": "PB7", "45": "PB8-BOOT0", "46": "PB9", "47": "VSS", "48": "VDD",
}

# Decoupling: 100nF per VDD pin pair + one shared 4.7uF bulk (C529355.json
# Figure 16 power supply scheme); VDDA 1uF+10nF; VREF+ 1uF+100nF, tied to
# VDDA (this package has no separate VREF-).
U601_DECOUPLING = [
    {"cap": "C601", "pin": "24", "rail": "+3V3", "value": "100nF 50V X7R",
     "lib_id": "aiee:CC0603KRX7R9BB104", "footprint": C0603},
    {"cap": "C602", "pin": "36", "rail": "+3V3", "value": "100nF 50V X7R",
     "lib_id": "aiee:CC0603KRX7R9BB104", "footprint": C0603},
    {"cap": "C603", "pin": "48", "rail": "+3V3", "value": "100nF 50V X7R",
     "lib_id": "aiee:CC0603KRX7R9BB104", "footprint": C0603},
    {"cap": "C604", "pin": "24", "rail": "+3V3", "value": "4.7uF 25V X5R",
     "lib_id": "aiee:CL21A475KAQNNNE", "footprint": C0805},
    {"cap": "C605", "pin": "21", "rail": "VDDA", "value": "1uF 50V X7R",
     "lib_id": "aiee:CL21B105KBFNNNE", "footprint": C0805},
    {"cap": "C606", "pin": "21", "rail": "VDDA", "value": "10nF 50V X7R",
     "lib_id": "Device:C", "footprint": C0603},
    {"cap": "C607", "pin": "20", "rail": "VDDA", "value": "1uF 50V X7R",
     "lib_id": "aiee:CL21B105KBFNNNE", "footprint": C0805},
    {"cap": "C608", "pin": "20", "rail": "VDDA", "value": "100nF 50V X7R",
     "lib_id": "aiee:CC0603KRX7R9BB104", "footprint": C0603},
]

# Cross-sheet nets exposed as hierarchical pins (sheets.md mcu row), in
# pinmap order. Free-cluster variant: the local label merges with the
# already-wired U601 pin by NAME on this sheet (lumina-carrier idiom), so
# these do not need ref/pad and can be laid out as a tidy column.
HIER_IN = [
    ("VDDA", "input"), ("VBUS_SENSE", "input"),
    ("ISENSE_A", "input"), ("ISENSE_B", "input"), ("ISENSE_C", "input"),
    ("VSENSE_A", "input"), ("VSENSE_B", "input"), ("VSENSE_C", "input"),
    ("HALL_A", "input"), ("HALL_B", "input"), ("HALL_C", "input"),
    ("ENC_A", "input"), ("ENC_B", "input"), ("ENC_Z", "input"),
    ("UART_RX", "input"),
]
HIER_OUT = [
    ("INHA", "output"), ("INHB", "output"), ("INHC", "output"),
    ("INLA", "output"), ("INLB", "output"), ("INLC", "output"),
    ("UART_TX", "output"),
]


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME, title="PCB-0018-A bldc-motor-driver: mcu (STM32G431CBT6)",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=600)

    # ---- U601 + decoupling -------------------------------------------------
    sh.place_ic_with_decoupling(
        "U601", f"{FP}:STM32G431CBT6", "STM32G431CBT6", at=(177.8, 152.4),
        pins=U601_PINS, expect=U601_EXPECT,
        footprint=f"{FP}:LQFP-48_L7.0-W7.0-P0.50-LS9.0-BL",
        decoupling=U601_DECOUPLING, caps_at=(25.4, 254.0), caps_dx=25.4)

    # Globalise +3V3/GND across the hierarchy from U601's own supply pins
    # (lumina-carrier mcu.py idiom): every other +3V3/GND connection on this
    # sheet is a plain same-name label, which merges with these by name.
    sh.power_symbol_at_pin("U601", "24", "power:+3V3")
    for pad in ("19", "23", "35", "47"):
        sh.power_symbol_at_pin("U601", pad, "power:GND")

    # ---- NRST: 100nF to GND + SW601 to GND + J601 pin 10 nRESET -----------
    sh.add_component("aiee:CC0603KRX7R9BB104", "C609", "100nF 50V X7R",
                     at=(279.4, 63.5), footprint=C0603)
    sh.wire_pins("C609", {"1": "NRST", "2": "GND"})
    sh.add_component(f"{FP}:TS-1088-AR02016", "SW601", "Reset switch SMD",
                     at=(279.4, 76.2), footprint="aiee:SW-SMD_L3.9-W3.0-P4.45")
    sh.wire_pins("SW601", {"1": "NRST", "2": "GND"})

    # ---- BOOT0: 10k pull-down (boot from flash) ----------------------------
    sh.add_component("aiee:0603WAF1002T5E", "R601", "10k 1%",
                     at=(279.4, 88.9), footprint=R0603)
    sh.wire_pins("R601", {"1": "BOOT0", "2": "GND"})

    # ---- SW602 user switch: PC13 to GND, firmware configures the internal
    # pull-up (mcu_pinmap.md); C610 100nF debounce across the same net -----
    sh.add_component(f"{FP}:TS-1088-AR02016", "SW602", "User switch SMD",
                     at=(279.4, 114.3), footprint="aiee:SW-SMD_L3.9-W3.0-P4.45")
    sh.wire_pins("SW602", {"1": "USER_SW", "2": "GND"})
    sh.add_component("aiee:CC0603KRX7R9BB104", "C610", "100nF 50V X7R",
                     at=(279.4, 127.0), footprint=C0603)
    sh.wire_pins("C610", {"1": "USER_SW", "2": "GND"})

    # ---- J601 SWD header: 2x5 1.27mm, standard Cortex debug pinout --------
    # 1 VTref(+3V3) 2 SWDIO 3 GND 4 SWCLK 5 GND 6 SWO(NC) 7 KEY(NC) 8 NC
    # 9 GND 10 nRESET.
    sh.add_component(f"{FP}:PZ127VS-12-10-H10-A38", "J601", "SWD 2x5 1.27mm",
                     at=(342.9, 152.4),
                     footprint="aiee:CONN-SMD_10P-P1.27_XFCN_PZ127VS-12-10-H10-A38")
    sh.wire_pins("J601", {
        "1": "+3V3", "2": "SWDIO", "3": "GND", "4": "SWCLK", "5": "GND",
        "6": "NC", "7": "NC", "8": "NC", "9": "GND", "10": "NRST",
    })

    # ---- status LEDs: D601 power (+3V3 direct via R602), D602 status
    # (PB11 via R603), D603 fault (PB12 via R604). Only KT-0603R (red) is
    # pulled into lib/aiee.kicad_sym; D601/D602 reuse that symbol (identical
    # 2-pin A/K 0603 LED footprint/pinout) with the LCSC field overridden to
    # the real green/yellow parts.json line, the same symbol-reuse idiom
    # PCB-0004-A_lumina-carrier/kicad/gen/mcu.py uses for D30.
    leds = [("R602", "D601", "+3V3", "LED_D601_A", 63.5, "LED green (power)"),
            ("R603", "D602", "LED_STATUS", "LED_D602_A", 88.9, "LED yellow (status)"),
            ("R604", "D603", "LED_FAULT", "LED_D603_A", 114.3, "LED red (fault)")]
    for r_ref, d_ref, a_net, mid_net, y, desc in leds:
        sh.add_component("aiee:0603WAF1001T5E", r_ref, "1k 1%",
                         at=(368.3, y), footprint=R0603)
        sh.wire_pins(r_ref, {"1": a_net, "2": mid_net})
        sh.add_component("aiee:KT-0603R", d_ref, desc, at=(393.7, y),
                         footprint=LED0603, expect={"1": "A", "2": "K"})
        sh.wire_pins(d_ref, {"1": mid_net, "2": "GND"})

    # ---- cross-sheet hierarchical pins -------------------------------------
    for i, (net, shape) in enumerate(HIER_IN):
        sh.hier_pin(net, shape=shape, at=(25.4, 25.4 + i * 7.62))
    for i, (net, shape) in enumerate(HIER_OUT):
        sh.hier_pin(net, shape=shape, at=(88.9, 25.4 + i * 7.62))

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    return sh


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else HERE.parents[1]
    try:
        sh = build()
        path = sh.save(out_dir, project=True)
        meta = sh.emit_decoupling(out_dir / "mcu_decoupling.json")
    except Exception as exc:  # noqa: BLE001  (any error -> exit 2)
        print(json.dumps({"script": f"gen.{NAME}", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({
        "script": f"gen.{NAME}", "status": "pass",
        "files": [str(path), str(meta)],
        "components": len(LCSC),
        "hier_pins": sorted(sh.hier_pins),
        "decoupling_associations": len(sh.decoupling),
        "place_report": sh.place_report,
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
