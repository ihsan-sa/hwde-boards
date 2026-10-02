"""Generator for the PCB-0017-A stereo-class-d-amp schematic - ONE FLAT root sheet.

Source of truth for kicad/PCB-0017-A_stereo-class-d-amp.kicad_sch (+ .kicad_pro,
decoupling.json). Rebuild from the repo root:

    .venv/bin/python PCB-0017-A_stereo-class-d-amp/kicad/gen/root.py

Wiring facts (parts/C46497.json = TI SLOS708G pin table; architecture/sheets.md
tie table; research: FAULTZ joined to SDZ for auto-clearing faults, PLIMIT tied
to GVDD = no power limit, AM2/AM1/AM0 = 0/0/0 = 400 kHz, MODSEL low = BD mode,
GAIN/SLV 5.6k to GND with the GVDD leg open = 20 dB master, SYNC is an OUTPUT
in master mode and is the design's one intentional no-connect, pin 33 EP is
the PowerPAD and goes to GND).

Net names are the CANONICAL ones of architecture/constraints.json: power nets
bare (+12V, GND, made global by power symbols), every other net a root-sheet
local label that the netlist reports with a leading '/' (/OUTPL, /SPK_L_P...).

J1-J4 and TP1 are bare copper pads (no LCSC part): in_bom is cleared here and
their aiee footprints carry exclude_from_bom + exclude_from_pos_files, so JLC
neither quotes nor places them.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BOARD = HERE.parents[2]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "hwde" / "scripts"))

# KiCad 10 stock libraries (power:*, Connector*): kicad-sch-api discovers
# KICAD_SYMBOL_DIR / KICAD9_SYMBOL_DIR only, not the KICAD10_SYMBOL_DIR the
# hwde env exports - alias it before the cache is first built.
if not os.environ.get("KICAD_SYMBOL_DIR"):
    for _cand in (os.environ.get("KICAD10_SYMBOL_DIR"),
                  str(Path.home() / ".local/kicad10/usr/share/kicad/symbols")):
        if _cand and Path(_cand).is_dir():
            os.environ["KICAD_SYMBOL_DIR"] = _cand
            break

import kicad_sch_api as ksa  # noqa: E402

ksa.get_symbol_cache().add_library_path(BOARD / "lib" / "aiee.kicad_sym")

import schlib  # noqa: E402

NAME = "PCB-0017-A_stereo-class-d-amp"
FP = "aiee"
C0402 = f"{FP}:C0402"
C0603 = f"{FP}:C0603"
C0805 = f"{FP}:C0805"
R0603 = f"{FP}:R0603"
WIREPAD2 = f"{FP}:WirePad_2P_3.0x6.0mm_P4.6mm"
WIREPAD3 = f"{FP}:WirePad_3P_1.5x3.0mm_P2.7mm"
TESTPAD = f"{FP}:TestPoint_SMD_1.5mm_Round"

# LCSC numbers straight from parts/parts.json (P3, live-verified 2026-09-27)
LCSC = {
    "U1": "C46497",
    "L1": "C207842", "L2": "C207842", "L3": "C207842", "L4": "C207842",
    "C13": "C46550467", "C14": "C2992596", "D1": "C113988",
    "C1": "C28323", "C2": "C28323", "C3": "C28323", "C4": "C28323",
    "C5": "C106858",
    "C6": "C14663", "C9": "C14663", "C10": "C14663",
    "C7": "C106246", "C8": "C106246",
    "C11": "C15850", "C12": "C15850",
    "C15": "C5378", "C16": "C5378", "C17": "C5378", "C18": "C5378",
    "C19": "C107133", "C20": "C107133", "C21": "C107133", "C22": "C107133",
    "C23": "C15195", "C24": "C15195", "C25": "C15195", "C26": "C15195",
    "R1": "C23189",
    "R2": "C25803", "R3": "C25803",
    "R4": "C137725", "R5": "C137725", "R6": "C137725", "R7": "C137725",
}
BARE_PADS = ("J1", "J2", "J3", "J4", "TP1")   # board features, nothing to buy

# U1 pin -> net (SLOS708G pin table, sheets.md tie table). "NC" = no-connect.
U1_PINS = {
    "1": "GND",       # MODSEL low = BD mode
    "2": "SDZ",       # shutdown, pulled to +12V by R2 (outputs enabled)
    "3": "SDZ",       # FAULTZ open-drain joined to SDZ: faults auto-clear
    "4": "RINP", "5": "RINN",
    "6": "GVDD",      # PLIMIT tied to GVDD = no power limit
    "7": "GVDD",      # GVDD LDO out, C5 1 uF only
    "8": "GAIN",      # GAIN/SLV: R1 5.6k to GND, GVDD leg open = 20 dB master
    "9": "GND",
    "10": "LINP", "11": "LINN",
    "12": "MUTE",     # R3 100k to GND = outputs enabled
    "13": "GND", "14": "GND", "15": "GND",   # AM2/AM1/AM0 = 0/0/0 = 400 kHz
    "16": "NC",       # SYNC: clock OUTPUT in master mode, nothing to drive
    "17": "+12V",     # AVCC
    "18": "+12V", "19": "+12V",              # PVCC pair, left-channel end
    "20": "BSNL", "21": "OUTNL", "22": "GND", "23": "OUTPL", "24": "BSPL",
    "25": "GND",
    "26": "BSNR", "27": "OUTNR", "28": "GND", "29": "OUTPR", "30": "BSPR",
    "31": "+12V", "32": "+12V",              # PVCC pair, right-channel end
    "33": "GND",      # PowerPAD (EP) - GND, via array to the B.Cu pour
}
U1_EXPECT = {
    "1": "MODSEL", "2": "SDZ", "3": "FAULTZ", "4": "RINP", "5": "RINN",
    "6": "PLIMIT", "7": "GVDD", "8": "GAIN", "9": "GND", "10": "LINP",
    "11": "LINN", "12": "MUTE", "13": "AM2", "14": "AM1", "15": "AM0",
    "16": "SYNC", "17": "AVCC", "18": "PVCC", "19": "PVCC", "20": "BSNL",
    "21": "OUTNL", "22": "GND", "23": "OUTPL", "24": "BSPL", "25": "GND",
    "26": "BSNR", "27": "OUTNR", "28": "GND", "29": "OUTPR", "30": "BSPR",
    "31": "PVCC", "32": "PVCC", "33": "EP",
}


def _dec(cap, pin, rail, value, lib, fp, **kw) -> dict:
    ent = {"cap": cap, "pin": pin, "rail": rail, "value": value,
           "lib_id": f"{FP}:{lib}", "footprint": fp}
    if rail != "+12V":
        ent["rail_net"] = f"/{rail}"       # root-local label -> "/NAME"
    ent.update(kw)
    return ent


# One decoupler per entry; the PVCC tiers carry role reg_input so
# check_decoupling insists on an HF ceramic within 7.5 mm of each PVCC pin -
# the class-D power stage draws the same trapezoidal switch current a
# regulator input does, and the 1 nF/100 nF tier is only useful tight to
# the pin (SLOS708G 8.2.2.4 / 10.1).
U1_DECOUPLING = [
    _dec("C5", "7", "GVDD", "1uF 25V X7R", "CC0603KRX7R8BB105", C0603,
         max_dist_mm=8.0),
    _dec("C6", "17", "+12V", "100nF 50V X7R", "CC0603KRX7R9BB104", C0603,
         max_dist_mm=7.5),
    _dec("C7", "18", "+12V", "1nF 50V NP0", "CC0603JRNPO9BN102", C0603,
         role="reg_input"),
    _dec("C9", "18", "+12V", "100nF 50V X7R", "CC0603KRX7R9BB104", C0603,
         role="reg_input"),
    _dec("C11", "18", "+12V", "10uF 25V X5R", "CL21A106KAYNNNE", C0805,
         role="reg_input", max_dist_mm=15.0),
    _dec("C14", "18", "+12V", "100uF 35V elec", "FZ100UF35V90RV0064",
         f"{FP}:CAP-SMD_BD6.3-L6.6-W6.6-LS7.3-FD", role="reg_input"),
    _dec("C8", "31", "+12V", "1nF 50V NP0", "CC0603JRNPO9BN102", C0603,
         role="reg_input"),
    _dec("C10", "31", "+12V", "100nF 50V X7R", "CC0603KRX7R9BB104", C0603,
         role="reg_input"),
    _dec("C12", "31", "+12V", "10uF 25V X5R", "CL21A106KAYNNNE", C0805,
         role="reg_input", max_dist_mm=15.0),
    _dec("C13", "31", "+12V", "100uF 35V polymer", "MA35V100M6X8",
         f"{FP}:CAP-SMD_BD6.3-L6.6-W6.6-RD", role="reg_input"),
]


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME,
        title="PCB-0017-A stereo-class-d-amp: TPA3118D2 stereo class-D amp, 12 V, BD mode 400 kHz, 20 dB",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=100)

    # ---- B2 line input (far left): J2 pads R / GND / L, AC coupling
    sh.add_component("Connector_Generic:Conn_01x03", "J2", "LINE IN R/GND/L",
                     at=(45.72, 78.74), footprint=WIREPAD3)
    sh.wire_pins("J2", {"1": "IN_R", "2": "GND", "3": "IN_L"})
    # C1/C3 couple the pads into the + inputs; C2/C4 AC-ground the unused
    # - inputs so both legs see the same source impedance (DC-detect).
    incaps = [("C3", 60.96, "IN_R", "RINP"), ("C4", 73.66, "RINN", "GND"),
              ("C1", 86.36, "IN_L", "LINP"), ("C2", 99.06, "LINN", "GND")]
    for ref, y, a, b in incaps:
        sh.add_component(f"{FP}:CL21B105KBFNNNE", ref, "1uF 50V X7R",
                         at=(83.82, y), footprint=C0805)
        sh.wire_pins(ref, {"1": a, "2": b})

    # ---- B3 amplifier: U1 in the middle, pins 1-16 left, 17-33 right
    sh.place_ic_with_decoupling(
        "U1", f"{FP}:TPA3118D2DAPR", "TPA3118D2DAPR", at=(139.7, 127.0),
        footprint=f"{FP}:HTSSOP-32_L11.0-W6.1-P0.65-LS8.1-BL-EP",
        pins=U1_PINS, expect=U1_EXPECT,
        decoupling=U1_DECOUPLING, caps_at=(38.1, 190.5), caps_dx=27.94)

    # configuration cluster, below-left of U1
    cfg = [("R1", 124.46, "0603WAF5601T5E", "5.6k 1%", "GAIN", "GND"),
           ("R2", 137.16, "0603WAF1003T5E", "100k 1%", "SDZ", "+12V"),
           ("R3", 149.86, "0603WAF1003T5E", "100k 1%", "MUTE", "GND")]
    for ref, y, lib, val, a, b in cfg:
        sh.add_component(f"{FP}:{lib}", ref, val, at=(83.82, y),
                         footprint=R0603)
        sh.wire_pins(ref, {"1": a, "2": b})

    # bootstrap caps, one per BSxx/OUTxx pin pair, never shared
    boot = [("C17", 63.5, "BSNR", "OUTNR"), ("C18", 76.2, "BSPR", "OUTPR"),
            ("C15", 88.9, "BSNL", "OUTNL"), ("C16", 101.6, "BSPL", "OUTPL")]
    for ref, y, a, b in boot:
        sh.add_component(f"{FP}:CL21B224KBFNNNE", ref, "220nF 50V X7R",
                         at=(195.58, y), footprint=C0805)
        sh.wire_pins(ref, {"1": a, "2": b})

    # ---- B4 LC output filters, right channel above left (pins 27/29 above
    # 21/23): L -> filter C to GND -> 3.3R + 10 nF damping branch to GND
    rows = [  # y, L, out net, spk net, filter C, damping R, Z net, damping C
        (114.3, "L3", "OUTPR", "SPK_R_P", "C21", "R6", "ZR_P", "C25"),
        (127.0, "L4", "OUTNR", "SPK_R_N", "C22", "R7", "ZR_N", "C26"),
        (139.7, "L1", "OUTPL", "SPK_L_P", "C19", "R4", "ZL_P", "C23"),
        (152.4, "L2", "OUTNL", "SPK_L_N", "C20", "R5", "ZL_N", "C24"),
    ]
    for y, l, out, spk, cf, rd, z, cd in rows:
        sh.add_component(f"{FP}:SLO0630H100MTT", l, "10uH 5.5A", at=(195.58, y),
                         footprint=f"{FP}:IND-SMD_L7.3-W6.6_MHCI06030")
        sh.wire_pins(l, {"1": out, "2": spk})
        sh.add_component(f"{FP}:CC0805KKX7R9BB684", cf, "680nF 50V X7R",
                         at=(238.76, y), footprint=C0805)
        sh.wire_pins(cf, {"1": spk, "2": "GND"})
        sh.add_component(f"{FP}:RC0603FR-073R3L", rd, "3.3R 1%", at=(281.94, y),
                         footprint=R0603)
        sh.wire_pins(rd, {"1": spk, "2": z})
        sh.add_component(f"{FP}:CL05B103KB5NNNC", cd, "10nF 50V X7R",
                         at=(325.12, y), footprint=C0402)
        sh.wire_pins(cd, {"1": z, "2": "GND"})

    # speaker pads (BTL: neither terminal is ground), J4 right above J3 left
    sh.add_component("Connector_Generic:Conn_01x02", "J4", "SPK R +/-",
                     at=(368.3, 119.38), footprint=WIREPAD2)
    sh.wire_pins("J4", {"1": "SPK_R_P", "2": "SPK_R_N"})
    sh.add_component("Connector_Generic:Conn_01x02", "J3", "SPK L +/-",
                     at=(368.3, 144.78), footprint=WIREPAD2)
    sh.wire_pins("J3", {"1": "SPK_L_P", "2": "SPK_L_N"})

    # ---- B1 12 V input pads, top right; bulk C13/C14 sit in the
    # decoupling row (associated with PVCC 31 and 18 respectively)
    sh.add_component("Connector_Generic:Conn_01x02", "J1", "12V IN +/GND",
                     at=(368.3, 63.5), footprint=WIREPAD2)
    sh.wire_pins("J1", {"1": "+12V", "2": "GND"})
    # D1 TVS across the input (schematic review W1): clamps the hot-plug
    # ring below U1's 30 V PVCC abs max. K = pin 1 = +12V.
    sh.add_component(f"{FP}:SMBJ15A_C113988", "D1", "SMBJ15A",
                     at=(342.9, 63.5), footprint=f"{FP}:SMB_L4.6-W3.6-LS5.3-RD")
    sh.wire_pins("D1", {"1": "+12V", "2": "GND"})

    # GND probe pad
    sh.add_component("Connector:TestPoint", "TP1", "GND", at=(38.1, 233.68),
                     footprint=TESTPAD)
    sh.wire_pins("TP1", {"1": "GND"})

    # ---- rails: external 12 V, no on-board source -> power symbol + PWR_FLAG
    sh.power_flag("+12V", at=(101.6, 228.6), sym="power:+12V", flag=True)
    sh.power_flag("GND", at=(139.7, 228.6), sym="power:GND", flag=True)

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    for ref in BARE_PADS:
        sh.sch.components.get(ref).in_bom = False
    return sh


def hide_lcsc_fields(path: Path) -> None:
    """Hide the LCSC property text (BOM data; ksa draws it over pin labels).
    Pure text edit on the saved file, electrically inert."""
    txt = path.read_text(encoding="utf-8")
    txt = re.sub(r'(\(property "LCSC" "[^"]*"\n\s*\(at [^)]*\)\n\s*\(effects\n)',
                 r'\1\t\t\t\t(hide yes)\n', txt)
    path.write_text(txt, encoding="utf-8")


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else HERE.parents[1]
    try:
        sh = build()
        sch = sh.save(out_dir, project=True)
        hide_lcsc_fields(sch)
        meta = sh.emit_decoupling(out_dir / "decoupling.json")
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"script": f"gen.{NAME}", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({"script": f"gen.{NAME}", "status": "pass",
                      "files": [str(sch), str(meta)],
                      "components": len(LCSC) + len(BARE_PADS),
                      "place_report": sh.place_report}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
