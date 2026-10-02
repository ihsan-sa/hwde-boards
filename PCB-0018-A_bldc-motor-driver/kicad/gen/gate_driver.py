"""PCB-0018-A `gate_driver` sheet: U301 DRV8300D 3-phase bootstrap gate driver.

Refdes block 300 (architecture/sheets.md): U301, C301-C305, R301-R302,
#PWR300+. Build output: kicad/gate_driver.kicad_sch (written by root.py).

Ground truth: parts/C3655801.json + parts/C3655801.pdf (TI SLVSFY0, DRV8300
Table 6-1) and `schlib.py --pins aiee:DRV8300DRGER_C3655801`. The VQFN-24
(RGE) DRV8300D has NO VDRAIN/VM pin and NO SLx/low-side return pin: the
low-side drivers return through GND (pin 6 + PowerPAD), the high-side
drivers through SHx. Every pin is listed in U301_PINS below.

Pin decisions (one line each):
  * GVDD (4) = +12V (TPS61040 boost, regulators sheet); C304 10 uF + C305
    1 uF to GND. 10 uF >= 10 x CBOOT (1 uF) per the GVDD/CBOOT ratio rule.
  * MODE (5) EXISTS on the VQFN part (it is absent only on TSSOP). Floating
    = non-inverted GLx; it also has an internal 200 k pull-down (RPD_MODE).
    R302 10 k to GND makes the non-inverted strap explicit and noise-proof
    (VIL_MODE 0.6 V). Never tie to GVDD: that inverts GLx vs INLx.
  * DT (21) R301 40.2 k to GND -> tDEAD ~200 ns (datasheet: 40 k -> 150/200/
    260 ns). Place R301 at the pin (layout note in the datasheet).
  * NC (7, 8) tied to GND: datasheet 11.1 allows it and it widens the
    PowerPAD's copper to the ground plane.
  * PowerPAD (25) -> GND. The package drawing only says "must be soldered";
    GND is inferred from 11.1 (NC-to-GND "increases ground connection between
    thermal pad and external ground plane") and TI's EVM. Flagged in OPEN.
  * INHx (22-24), INLx (1-3): hier inputs from the MCU (TIM1 CH/CHN). Both
    have internal 200 k pull-downs (INLx in non-inverted mode), so an
    un-driven MCU pin reads low = FETs off; no external pull-downs.
  * BSTx (20/17/14): CBOOT 1 uF (C301-C303) BSTx->SHx, local nets BSTA/B/C
    (constraints.json names /gate_driver/BSTA..C at 57 V).
  * SHx (18/15/12) = PHASE_x hier (bidirectional): HS source sense.
  * GHx/GLx: hier outputs to power_stage, where the 10R gate resistors sit.
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

import schlib  # noqa: E402

NAME = "gate_driver"
FP = "aiee"
C0805 = f"{FP}:C0805"
R0603 = f"{FP}:R0603"

U301_PINS = {
    "1": "INLA", "2": "INLB", "3": "INLC",
    "4": "+12V",                 # GVDD
    "5": "MODE",                 # R302 10k to GND = non-inverted GLx
    "6": "GND",
    "7": "GND", "8": "GND",      # NC: tied to GND per datasheet 11.1
    "9": "GLC", "10": "GLB", "11": "GLA",
    "12": "PHASE_C", "13": "GHC", "14": "BSTC",
    "15": "PHASE_B", "16": "GHB", "17": "BSTB",
    "18": "PHASE_A", "19": "GHA", "20": "BSTA",
    "21": "DT",                  # R301 40.2k to GND = ~200 ns dead time
    "22": "INHA", "23": "INHB", "24": "INHC",
    "25": "GND",                 # PowerPAD -> GND (see OPEN)
}
U301_EXPECT = {
    "1": "INLA", "2": "INLB", "3": "INLC", "4": "GVDD", "5": "MODE",
    "6": "GND", "7": "NC", "8": "NC", "9": "GLC", "10": "GLB", "11": "GLA",
    "12": "SHC", "13": "GHC", "14": "BSTC", "15": "SHB", "16": "GHB",
    "17": "BSTB", "18": "SHA", "19": "GHA", "20": "BSTA", "21": "DT",
    "22": "INHA", "23": "INHB", "24": "INHC", "25": "EP",
}


def _dec(cap, pin, rail, value, lib, gnd="GND", **kw) -> dict:
    ent = {"cap": cap, "pin": pin, "rail": rail, "value": value,
           "lib_id": f"{FP}:{lib}", "footprint": C0805, "gnd": gnd}
    ent.update(kw)
    return ent


# GVDD pair + one CBOOT per phase. Boot caps: rail = BSTx (sheet-local ->
# /gate_driver/BSTx), return = SHx = the root-level /PHASE_x net.
U301_DECOUPLING = [
    # 1210 X7R 50 V: keeps ~7 uF at 12 V bias (the DS asks >=10 uF nominal;
    # a 25 V X5R 0805 keeps only 3-5 uF there - P4 review).
    _dec("C304", "4", "+12V", "10uF 50V X7R", "CS3225X7R106K500NRL",
         footprint=f"{FP}:C1210"),
    _dec("C305", "4", "+12V", "1uF 50V X7R", "CL21B105KBFNNNE",
         max_dist_mm=5.0),
    _dec("C301", "20", "BSTA", "1uF 50V X7R", "CL21B105KBFNNNE",
         gnd="PHASE_A", rail_net="/gate_driver/BSTA", gnd_net="/PHASE_A",
         max_dist_mm=5.0),
    _dec("C302", "17", "BSTB", "1uF 50V X7R", "CL21B105KBFNNNE",
         gnd="PHASE_B", rail_net="/gate_driver/BSTB", gnd_net="/PHASE_B",
         max_dist_mm=5.0),
    _dec("C303", "14", "BSTC", "1uF 50V X7R", "CL21B105KBFNNNE",
         gnd="PHASE_C", rail_net="/gate_driver/BSTC", gnd_net="/PHASE_C",
         max_dist_mm=5.0),
]

LCSC = {
    "U301": "C3655801",
    "C301": "C28323", "C302": "C28323", "C303": "C28323", "C305": "C28323",
    "C304": "C2918502",
    "R301": "C12447", "R302": "C25804",
}

HIER = [  # (net, shape)
    ("INHA", "input"), ("INLA", "input"), ("INHB", "input"),
    ("INLB", "input"), ("INHC", "input"), ("INLC", "input"),
    ("GHA", "output"), ("GLA", "output"), ("GHB", "output"),
    ("GLB", "output"), ("GHC", "output"), ("GLC", "output"),
    ("PHASE_A", "bidirectional"), ("PHASE_B", "bidirectional"),
    ("PHASE_C", "bidirectional"),
]


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME, title="PCB-0018 REV A gate driver: DRV8300D, GVDD 12 V, 6-PWM, 200 ns DT",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=300)

    sh.place_ic_with_decoupling(
        "U301", f"{FP}:DRV8300DRGER_C3655801", "DRV8300DRGER",
        at=(190.5, 114.3),
        footprint=f"{FP}:VQFN-24_L4.0-W4.0-P0.50-TL-EP2.5",
        pins=U301_PINS, expect=U301_EXPECT,
        decoupling=U301_DECOUPLING, caps_at=(101.6, 203.2), caps_dx=25.4)

    # straps: DT and MODE resistors to GND
    for ref, y, lib, val, net in (
            ("R301", 50.8, "0603WAF4022T5E", "40.2k 1%", "DT"),
            ("R302", 76.2, "0603WAF1002T5E", "10k", "MODE")):
        sh.add_component(f"{FP}:{lib}", ref, val, at=(76.2, y),
                         footprint=R0603)
        sh.wire_pins(ref, {"1": net, "2": "GND"})

    # interface nets: free-area hier clusters (local label <-> hier label)
    for i, (net, shape) in enumerate(HIER):
        sh.hier_pin(net, shape=shape, at=(330.2, 45.72 + i * 7.62))

    # global rails: power symbol + local label (no PWR_FLAG: driven elsewhere)
    sh.power_flag("+12V", at=(38.1, 254.0), sym="power:+12V", flag=False)
    sh.power_flag("GND", at=(63.5, 254.0), sym="power:GND", flag=False)

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    return sh


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else Path("/tmp/p18-gate_driver")
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
