"""PCB-0018-A bldc-motor-driver `sensing` sheet: 3x INA240A1 Kelvin shunt
current-sense amps + phase/bus voltage dividers.

Refdes range (architecture/sheets.md): base 500 -> U5xx, R5xx, C5xx,
#PWR/#FLG 500+.

Interface (sheets.md):
  in:  /ISNS_A_P /ISNS_A_N /ISNS_B_P /ISNS_B_N /ISNS_C_P /ISNS_C_N
       (Kelvin taps off the power_stage shunts), /PHASE_A /PHASE_B /PHASE_C,
       VM, +3V3 (all global rails except the /ISNS_x and /PHASE_x hier pins)
  out: /ISENSE_A /ISENSE_B /ISENSE_C, /VSENSE_A /VSENSE_B /VSENSE_C,
       /VBUS_SENSE

GROUND TRUTH: parts/C2060769.json (INA240A1DR, TI SBOS851 pin/layout
extract). Two facts drive every wiring choice here:
  * REF1/REF2 = +3V3/GND (blocks.md decision #4/conflicts-resolved): output
    idles at VS/2 = 1.65 V, giving the bidirectional +-1.2 V swing at 20 A
    peak that blocks.md's arithmetic assumes.
  * layout_notes[0] in the datasheet extract: "Input filters are not
    required for accurate measurement and are not recommended at the input
    pins ... prefer filtering at the amplifier output instead." So there is
    NO RC at IN+/IN- (would also violate Kelvin purity and add differential
    error via bias-current mismatch per the same note) - ASSUMED per the
    brief's own fallback ("if it says none, use none and say so"). A small
    output RC (R50x 100R + C50x 2.2nF, corner ~723 kHz, above the amp's
    400 kHz BW) sits between OUT and the ISENSE_x hier pin instead, which is
    exactly what the datasheet note recommends.
  * pin 4 (NC) "Reserved. Connect to ground or leave floating" -> tied to
    GND (a harmless, defined choice; zero cost, avoids a floating pad near
    a switching board).

Dividers: 150k/10k (1:16, blocks.md conflict #5) with a 100nF filter cap at
the tap, for VSENSE_A/B/C (off /PHASE_x) and VBUS_SENSE (off VM). 45 V clamp
-> 2.8 V at the ADC (blocks.md arithmetic).

Every hier pin here uses the free-cluster `hier_pin(net, at=...)` idiom
(schlib.py, S7 pattern used by lumina-carrier's mcu.py stub rows): it ties
into the local net purely by matching label text, so it never double-wires
a component pin that a `pins=` dict or `wire_pins` call already wired.

Rebuild standalone:
    ~/.local/hwde-venv/bin/python kicad/gen/sensing.py
"""
from __future__ import annotations

import argparse
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

NAME = "sensing"
FP = "aiee"
R0603 = f"{FP}:R0603"
C0603 = f"{FP}:C0603"

SYM_INA240A1 = f"{FP}:INA240A1DR"          # C2060769
SYM_R150K = f"{FP}:0603WAF1503T5E"         # C22807
SYM_R10K = f"{FP}:0603WAF1002T5E"          # C25804 (shared w/ power_stage)
SYM_R100R = f"{FP}:0603WAF1000T5E"         # C22775 (shared w/ io)
SYM_C100N = f"{FP}:CC0603KRX7R9BB104"      # C14663
SYM_C2N2 = f"{FP}:0603B222K500NT"          # C1604 (shared w/ regulators)

INA240A1_EXPECT = {
    "1": "IN-", "2": "GND", "3": "REF2", "4": "NC", "5": "OUT",
    "6": "VS", "7": "REF1", "8": "IN+",
}


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME,
        title="PCB-0018-A bldc-motor-driver: sensing (3x INA240A1 shunt CSA "
              "+ phase/bus dividers)",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=500)

    # ---- three CSA channels, stacked vertically -------------------------
    legs = [
        ("A", "U501", (76.2, 30.48), "R501", "C501", "C511"),
        ("B", "U502", (76.2, 71.12), "R502", "C502", "C512"),
        ("C", "U503", (76.2, 111.76), "R503", "C503", "C513"),
    ]
    for ph, u_ref, u_at, r_ref, c_filt_ref, c_byp_ref in legs:
        pins = {
            "1": f"ISNS_{ph}_N",   # IN- : load side of shunt (Kelvin)
            "2": "GND",
            "3": "GND",            # REF2 = GND -> mid-supply w/ REF1=+3V3
            "4": "GND",            # NC: "connect to ground or leave floating"
            "5": f"CSA_{ph}_OUT",  # OUT -> output RC -> ISENSE_x
            "6": "+3V3",           # VS, 2.7-5.5V
            "7": "+3V3",           # REF1 = +3V3 -> Vs/2 = 1.65V mid-supply
            "8": f"ISNS_{ph}_P",   # IN+ : supply side of shunt (Kelvin)
        }
        sh.place_ic_with_decoupling(
            u_ref, SYM_INA240A1, "INA240A1", at=u_at,
            footprint=f"{FP}:SOIC-8_L5.0-W4.0-P1.27-LS6.0-BL",
            pins=pins, expect=INA240A1_EXPECT,
            decoupling=[{"cap": c_byp_ref, "pin": "6", "rail": "+3V3",
                        "value": "100nF 50V X7R", "lib_id": SYM_C100N,
                        "footprint": C0603, "max_dist_mm": 5.0}],
            caps_at=(u_at[0] - 43.18, u_at[1]))

        # Kelvin taps IN from power_stage (free-cluster hier pin: the IC
        # pins are already wired to these exact net names above via `pins`,
        # this just exports them - never re-touches U50x's pins 1/8).
        sh.hier_pin(f"ISNS_{ph}_P", shape="input", at=(15.24, u_at[1] - 5.08))
        sh.hier_pin(f"ISNS_{ph}_N", shape="input", at=(15.24, u_at[1] + 5.08))

        # No input RC (datasheet layout_notes[0]: not recommended, prefer
        # output filtering instead). Output RC: OUT -> R (100R) -> node,
        # node -> C (2.2nF) to GND, node -> ISENSE_x hier pin. Corner
        # ~723 kHz, above the 400 kHz CSA bandwidth so it does not eat the
        # signal, well below the ADC's sampling Nyquist floor for FOC.
        r_at = (u_at[0] + 20.32, u_at[1] - 7.62)
        sh.add_component(SYM_R100R, r_ref, "100 ohm", at=r_at,
                         footprint=R0603)
        sh.wire_pins(r_ref, {"1": f"CSA_{ph}_OUT", "2": f"ISENSE_{ph}"})
        c_at = (r_at[0] + 15.24, r_at[1])
        sh.add_component(SYM_C2N2, c_filt_ref, "2.2nF 50V X7R", at=c_at,
                         footprint=C0603)
        sh.wire_pins(c_filt_ref, {"1": f"ISENSE_{ph}", "2": "GND"})
        sh.hier_pin(f"ISENSE_{ph}", shape="output",
                   at=(c_at[0] + 15.24, c_at[1]))

    # Promote +3V3/GND to global exactly once each on this sheet (rails
    # binder to sheets.md s1.1; every other "+3V3"/"GND" label on this
    # sheet joins by name - same-sheet local labels merge automatically).
    sh.power_symbol_at_pin("U501", "6", "power:+3V3")
    sh.power_symbol_at_pin("U501", "2", "power:GND")

    # ---- phase + bus dividers, 150k/10k (1:16) + filter cap (2.2nF phase, 100nF bus) -------
    div_rows = [
        ("A", "R510", "R511", "C521", 30.48),
        ("B", "R512", "R513", "C522", 71.12),
        ("C", "R514", "R515", "C523", 111.76),
    ]
    dx = 152.4
    for ph, r_top, r_bot, c_filt, y in div_rows:
        vsense_net = f"VSENSE_{ph}"
        top_at = (dx, y)
        sh.add_component(SYM_R150K, r_top, "150k", at=top_at,
                         footprint=R0603)
        sh.wire_pins(r_top, {"1": f"PHASE_{ph}", "2": vsense_net})
        sh.hier_pin(f"PHASE_{ph}", shape="input", at=(dx - 20.32, y))
        bot_at = (dx, y + 20.32)
        sh.add_component(SYM_R10K, r_bot, "10k", at=bot_at,
                         footprint=R0603)
        sh.wire_pins(r_bot, {"1": vsense_net, "2": "GND"})
        c_at = (dx + 15.24, y + 10.16)
        # 2.2nF: corner ~7.7 kHz with the 9.4k divider source, fast enough
        # to follow BEMF (100nF gave ~170 Hz - P4 review).
        sh.add_component(SYM_C2N2, c_filt, "2.2nF 50V X7R", at=c_at,
                         footprint=C0603)
        sh.wire_pins(c_filt, {"1": vsense_net, "2": "GND"})
        sh.hier_pin(vsense_net, shape="output", at=(dx + 30.48, y + 10.16))

    # VBUS_SENSE: same 150k/10k divider, top leg off VM (global rail, not a
    # hier pin - VM is already global per sheets.md s1.1).
    vbus_y = 152.4
    sh.add_component(SYM_R150K, "R516", "150k", at=(dx, vbus_y),
                     footprint=R0603)
    sh.wire_pins("R516", {"1": "VM", "2": "VBUS_SENSE"})
    # No power:VM symbol exists; power:VCC carries VALUE "VM" (matches the
    # power_stage sheet convention - power_symbol_at_pin sets VALUE from the
    # pin's already-wired net, so the symbol body choice is cosmetic).
    sh.power_symbol_at_pin("R516", "1", "power:VCC")
    sh.add_component(SYM_R10K, "R517", "10k", at=(dx, vbus_y + 20.32),
                     footprint=R0603)
    sh.wire_pins("R517", {"1": "VBUS_SENSE", "2": "GND"})
    sh.add_component(SYM_C100N, "C524", "100nF 50V X7R",
                     at=(dx + 15.24, vbus_y + 10.16), footprint=C0603)
    sh.wire_pins("C524", {"1": "VBUS_SENSE", "2": "GND"})
    sh.hier_pin("VBUS_SENSE", shape="output",
               at=(dx + 30.48, vbus_y + 10.16))

    return sh


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(BOARD / "kicad"),
                    help="directory to write sensing.kicad_sch into (use a "
                         "scratch dir for standalone verification - the root "
                         "generator owns WS/kicad/*.kicad_sch)")
    ap.add_argument("--project", action="store_true",
                    help="also write sensing.kicad_pro (standalone ERC only)")
    args = ap.parse_args(argv)
    try:
        sh = build()
        path = sh.save(args.out, project=args.project)
    except Exception as exc:  # noqa: BLE001 (SPEC 6: any error -> exit 2)
        print(json.dumps({"script": "gen.sensing", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({
        "script": "gen.sensing", "status": "pass",
        "sheet": str(path),
        "components": len(list(sh.sch.components)),
        "hier_pins": sorted(sh.hier_pins),
        "decoupling_associations": len(sh.decoupling),
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
