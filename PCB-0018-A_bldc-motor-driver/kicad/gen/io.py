"""PCB-0018-A bldc-motor-driver `io` sheet: control + sensor connectors.

Refdes range (architecture/sheets.md): base 700 -> J7xx, F7xx, R7xx, C7xx,
D7xx, #PWR/#FLG 700+.

Interface (sheets.md):
  in:  +5V, +3V3 (global rails)
  bidir: /UART_TX, /UART_RX, /HALL_A /HALL_B /HALL_C, /ENC_A /ENC_B /ENC_Z

Parts (parts/parts.json, all "io" block):
  J701 SM04B-GHS-TB(LF)(SN)   JST-GH 4p: GND, CTL_5V, UART_TX, UART_RX
  J702 SH-SM08B-GHS-TB(LF)(SN) JST-GH 8p: SEN_5V, GND, HALL_A/B/C, ENC_A/B/Z
  F701/F702 nSMD020-30V PTC (0.2A hold), +5V -> CTL_5V / SEN_5V
  R7xx 0603WAF1000T5E (100R) series on every signal line at both connectors
  R7xx 0603WAF4701T5E (4.7k) Hall pull-ups to +3V3 (open-drain per blocks.md)
  D7xx PESD5V0S1BA-ES per signal line, connector side of the series R
       ("placed at the connector side before the series/pull-up resistors" -
       parts.json role note)

GROUND TRUTH for connector pin assignment: no datasheet pin-numbered
extract was staged for J701/J702 (parts/ has no C189895.json/C42376901.json);
blocks.md gives only the SIGNAL LIST per connector, not a pin order. The
footprint pad map (lib/aiee.pretty/CONN-SMD_4P-P1.25_SM04B-GHS-TB-LF-SN and
.../CONN-SMD_SH-SM08B-GHS-TB) shows pins 1-4 (4p) / 1-8 (8p) as the real
signal pads (0.6-0.7mm narrow pads) and pins 5-6 / 9-10 as wide mechanical
tabs at the connector shoulders - those get NC. ASSUMED pin order (signal
list order, first-to-last): J701 1=GND 2=CTL_5V 3=UART_TX 4=UART_RX; J702
1=SEN_5V 2=GND 3=HALL_A 4=HALL_B 5=HALL_C 6=ENC_A 7=ENC_B 8=ENC_Z. OPEN item:
verify against the JST-GH tape/reel pin-1 mark before order (a same-family
right-angle SMD JST-GH numbers pin 1 nearest the polarity key, consistent
between the 4p and 8p bodies here, but the exact silkscreen orientation is
P6/P9's job).

Filter policy per blocks.md's io section, read literally: "4.7k pull-ups to
+3V3 (Halls are open-drain...)" scopes the pull-up to the 3 Hall lines only;
"100 ohm / 1nF filters" reads as the general EMI/ESD RC on the sensor
connector's 6 signal lines (Halls + encoders). Encoder lines get NO pull-up:
blocks.md's own parenthetical says "5V push-pull encoders land on FT pins" -
a push-pull driver pulled up to +3V3 would fight the driver on its LOW state
and is the wrong topology; ASSUMED no pull-up on ENC_A/B/Z, only series R +
RC filter, consistent with the brief's own conditional ("...if blocks.md
says"). UART_TX/RX (control connector) get series R + ESD only, no filter
cap - blocks.md's control-connector sentence names only "series 100 ohm +
ESD", no capacitor.

No 1nF-class capacitor was staged in parts.json for this filter; C1604
(2.2nF 50V X7R 0603, "0603B222K500NT") is already pulled into lib/ for the
regulators sheet and is the closest available part (a 100R/2.2nF corner is
~723 kHz, still well above Hall/encoder mechanical rates). ASSUMED reuse of
that LCSC part rather than adding a new one from this P4 seat.

Rebuild standalone:
    ~/.local/hwde-venv/bin/python kicad/gen/io.py
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

NAME = "io"
FP = "aiee"
R0603 = f"{FP}:R0603"
C0603 = f"{FP}:C0603"
SOD323 = f"{FP}:SOD-323_L1.7-W1.3-LS2.6-BI"
F1206 = f"{FP}:F1206"
CONN4P = f"{FP}:CONN-SMD_4P-P1.25_SM04B-GHS-TB-LF-SN"
CONN8P = f"{FP}:CONN-SMD_SH-SM08B-GHS-TB"

SYM_J4P = f"{FP}:SM04B-GHS-TB"             # C189895
SYM_J8P = f"{FP}:SH-SM08B-GHS-TB"          # C42376901
SYM_PTC = f"{FP}:nSMD020-30V"              # C69680
SYM_ESD = f"{FP}:PESD5V0S1BA-ES"           # C5180216
SYM_R100R = f"{FP}:0603WAF1000T5E"         # C22775
SYM_R4K7 = f"{FP}:0603WAF4701T5E"          # C23162
SYM_C2N2 = f"{FP}:0603B222K500NT"          # C1604 (shared w/ regulators)


def _line(sh, *, tag, conn_ref, conn_pad, raw_net, final_net, shape,
         esd_ref, r_ref, esd_at, r_at, pullup=None, pullup_at=None,
         filt=None, filt_at=None):
    """One connector signal line: conn pin --(raw_net)-- ESD(->GND) --
    100R series --(final_net)-- [pull-up to +3V3] [RC filter cap to GND] --
    hier pin. `shape` is the hier_pin shape (bidirectional for every net on
    this sheet - MCU drives some, the connector drives others)."""
    sh.wire_pin(conn_ref, conn_pad, raw_net)
    sh.add_component(SYM_ESD, esd_ref, "PESD5V0S1BA-ES", at=esd_at,
                     footprint=SOD323)
    sh.wire_pins(esd_ref, {"1": raw_net, "2": "GND"})
    sh.add_component(SYM_R100R, r_ref, "100 ohm", at=r_at, footprint=R0603)
    sh.wire_pins(r_ref, {"1": raw_net, "2": final_net})
    if pullup:
        sh.add_component(SYM_R4K7, pullup, "4.7k", at=pullup_at,
                         footprint=R0603)
        sh.wire_pins(pullup, {"1": final_net, "2": "+3V3"})
    if filt:
        sh.add_component(SYM_C2N2, filt, "2.2nF 50V X7R", at=filt_at,
                         footprint=C0603)
        sh.wire_pins(filt, {"1": final_net, "2": "GND"})
    sh.hier_pin(final_net, shape=shape,
               at=(r_at[0] + 25.4, r_at[1]))


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME,
        title="PCB-0018-A bldc-motor-driver: io (JST-GH control + sensor "
              "connectors, PTC + ESD + filtering)",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=700)

    # ---- J701 control connector: 1 GND, 2 CTL_5V, 3 UART_TX, 4 UART_RX --
    j1_at = (38.1, 30.48)
    sh.add_component(SYM_J4P, "J701", "JST-GH 4p SMD", at=j1_at,
                     footprint=CONN4P)
    sh.wire_pin("J701", "1", "GND")
    sh.wire_pin("J701", "2", "CTL_5V")
    # pins 5/6: wide mechanical tabs (footprint pad size 1.0x2.7mm vs the
    # 0.6x1.7mm signal pads) - no signal, explicit NC.
    sh.wire_pin("J701", "5", "NC")
    sh.wire_pin("J701", "6", "NC")

    sh.add_component(SYM_PTC, "F701", "PTC 0.2A hold 30V", at=(38.1, 45.72),
                     footprint=F1206)
    sh.wire_pins("F701", {"1": "+5V", "2": "CTL_5V"})

    _line(sh, tag="UART_TX", conn_ref="J701", conn_pad="3",
         raw_net="UART_TX_RAW", final_net="UART_TX", shape="bidirectional",
         esd_ref="D701", r_ref="R701",
         esd_at=(50.8, 21.59), r_at=(76.2, 21.59))
    _line(sh, tag="UART_RX", conn_ref="J701", conn_pad="4",
         raw_net="UART_RX_RAW", final_net="UART_RX", shape="bidirectional",
         esd_ref="D702", r_ref="R702",
         esd_at=(50.8, 33.02), r_at=(76.2, 33.02))

    # ---- J702 sensor connector: 1 SEN_5V, 2 GND, 3-5 HALL_A/B/C,
    #      6-8 ENC_A/B/Z --------------------------------------------------
    j2_at = (38.1, 101.6)
    sh.add_component(SYM_J8P, "J702", "JST-GH 8p SMD", at=j2_at,
                     footprint=CONN8P)
    sh.wire_pin("J702", "1", "SEN_5V")
    sh.wire_pin("J702", "2", "GND")
    # pins 9/10: wide mechanical tabs, same reasoning as J701 5/6.
    sh.wire_pin("J702", "9", "NC")
    sh.wire_pin("J702", "10", "NC")

    sh.add_component(SYM_PTC, "F702", "PTC 0.2A hold 30V", at=(38.1, 116.84),
                     footprint=F1206)
    sh.wire_pins("F702", {"1": "+5V", "2": "SEN_5V"})

    # Halls: open-drain -> 4.7k pull-up to +3V3, plus the 100R/2.2nF filter
    # blocks.md's sensor-connector sentence gives every line there.
    hall_rows = [
        ("HALL_A", "3", 80.01), ("HALL_B", "4", 92.71), ("HALL_C", "5", 105.41),
    ]
    for i, (net, pad, y) in enumerate(hall_rows, start=703):
        _line(sh, tag=net, conn_ref="J702", conn_pad=pad,
             raw_net=f"{net}_RAW", final_net=net, shape="bidirectional",
             esd_ref=f"D{i}", r_ref=f"R{i}",
             esd_at=(50.8, y), r_at=(76.2, y),
             pullup=f"R{i+3}", pullup_at=(76.2, y - 7.62),
             filt=f"C{700 + (i - 703) + 1}", filt_at=(91.44, y))

    # Encoders: 5V push-pull outputs landing on FT (5V-tolerant) MCU pins
    # (blocks.md parenthetical) -> NO pull-up (would fight the driver's LOW
    # state); series R + RC filter only, same as the Hall filter leg.
    enc_rows = [
        ("ENC_A", "6", 118.11), ("ENC_B", "7", 130.81), ("ENC_C_Z", "8", 143.51),
    ]
    enc_net_names = {"ENC_A": "ENC_A", "ENC_B": "ENC_B", "ENC_C_Z": "ENC_Z"}
    for i, (tag, pad, y) in enumerate(enc_rows, start=709):
        net = enc_net_names[tag]
        _line(sh, tag=net, conn_ref="J702", conn_pad=pad,
             raw_net=f"{net}_RAW", final_net=net, shape="bidirectional",
             esd_ref=f"D{i}", r_ref=f"R{i}",
             esd_at=(50.8, y), r_at=(76.2, y),
             filt=f"C{704 + (i - 709)}", filt_at=(91.44, y))

    # Promote +5V/+3V3/GND to global exactly once each on this sheet
    # (sourced on power_in/regulators; sheets.md s1.1 rails). Every other
    # "+5V"/"+3V3"/"GND" label on this sheet joins by name.
    sh.power_symbol_at_pin("F701", "1", "power:+5V")
    sh.power_symbol_at_pin("R706", "2", "power:+3V3")   # first Hall pull-up
    sh.power_symbol_at_pin("J701", "1", "power:GND")

    return sh


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(BOARD / "kicad"),
                    help="directory to write io.kicad_sch into (use a "
                         "scratch dir for standalone verification - the root "
                         "generator owns WS/kicad/*.kicad_sch)")
    ap.add_argument("--project", action="store_true",
                    help="also write io.kicad_pro (standalone ERC only)")
    args = ap.parse_args(argv)
    try:
        sh = build()
        path = sh.save(args.out, project=args.project)
    except Exception as exc:  # noqa: BLE001 (SPEC 6: any error -> exit 2)
        print(json.dumps({"script": "gen.io", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({
        "script": "gen.io", "status": "pass",
        "sheet": str(path),
        "components": len(list(sh.sch.components)),
        "hier_pins": sorted(sh.hier_pins),
        "decoupling_associations": len(sh.decoupling),
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
