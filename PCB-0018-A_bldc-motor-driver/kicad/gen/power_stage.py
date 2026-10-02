"""PCB-0018-A `power_stage` sheet: three NTMFS5C628NL half-bridges with
low-side 3 mOhm Kelvin shunts.

Refdes block 400 (architecture/sheets.md, constraints.json placement groups):
  leg A: Q401 HS, Q402 LS, R401 shunt, C401-C403 10 uF 1210, C404 100 nF 1210
  leg B: Q403 HS, Q404 LS, R402 shunt, C405-C407, C408
  leg C: Q405 HS, Q406 LS, R403 shunt, C409-C411, C412
  gate R R411-R416 (odd = HS, even = LS), gate-source pull-downs R421-R426,
  DNP snubbers R431-R436 / C431-C436, phase pads TP401-TP403,
  Kelvin net ties NT401-NT406, #PWR400+.

Ground truth: parts/C145537.json and `schlib.py --pins aiee:NTMFS5C628NLT1G`:
pins 1-3 = S, 4 = G, 5 = D (the SO-8FL drain pins 5-8 AND the exposed tab
are one custom pad 5 on the aiee DFN-5 footprint - FET EP = drain).

Per leg X (A/B/C):
  HS FET  D=VM        S=PHASE_X   G=GATE_HX
  LS FET  D=PHASE_X   S=LS_SRC_X  G=GATE_LX
  GHX -> 10R -> GATE_HX, 10k GATE_HX->PHASE_X (pull-down across G-S at the FET)
  GLX -> 10R -> GATE_LX, 10k GATE_LX->LS_SRC_X
  shunt 3 mOhm 2512: LS_SRC_X (top) -> GND (bottom)
  Kelvin: the shunt is a 2-terminal 2512 (no 4-terminal part/footprint in
  parts.json or lib), so the sense nets are made DISTINCT nets with a net
  tie at each shunt pad: NT(P) LS_SRC_X <-> ISNS_X_P, NT(N) GND <-> ISNS_X_N.
  Without them ISNS_X_P would simply be LS_SRC_X (one net, one name) and
  ISNS_X_N would be GND, and neither the diff-pair rules nor the router
  could keep the sense traces off the power copper. Layout must put each
  net tie ON its shunt pad (inner edge), so the tap is the pad itself.
  Leg MLCC bank: 3x 10 uF 50 V X7R 1210 + 100 nF 50 V 1210, VM to GND -
  i.e. HS drain to shunt bottom, spanning the whole commutation loop.
  DNP RC snubber across each FET (D-S), values are placeholders.
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

NAME = "power_stage"
FP = "aiee"
FET = f"{FP}:NTMFS5C628NLT1G"
FET_FP = f"{FP}:DFN-5_L4.9-W5.9-P1.27-LS6.2-BL"
FET_EXPECT = {"1": "S", "2": "S", "3": "S", "4": "G", "5": "D"}
SHUNT = f"{FP}:HOYLR2512-3W-3MR-1%"
NETTIE = "Device:NetTie_2"
NETTIE_FP = "NetTie:NetTie-2_SMD_Pad0.5mm"
PHASE_PAD_FP = "TestPoint:TestPoint_THTPad_4.0x4.0mm_Drill2.0mm"

LEGS = ("A", "B", "C")


def _wire_all_drains(sh: schlib.Sheet, ref: str, net: str) -> None:
    """The aiee FET symbol carries FOUR pins numbered 5 (D) at different
    places; wire_pin reaches only the first, and KiCad ERC then reports the
    others as a duplicate pin on separate nets. Stub + label each of the
    remaining pin-5 instances onto the same drain net (rotation 0 only)."""
    ax, ay = sh._anchors[ref]
    first = sh.pin_pos(ref, "5")
    for p in sh.sch.components.get(ref).pins:
        if p.number != "5":
            continue
        pos = (round(ax + p.position.x, 4), round(ay - p.position.y, 4))
        if pos == first:
            continue
        d = schlib.stub_dir(p.rotation, 0)
        end = (round(pos[0] + d[0] * schlib.STUB, 4),
               round(pos[1] + d[1] * schlib.STUB, 4))
        seg = sh._add_wire(pos, end)
        sh._assert_label_clear(end, net, own=seg)
        sh.sch.add_label(net, position=end)
COL_X = (63.5, 190.5, 317.5)   # one column per leg


def build() -> schlib.Sheet:
    sh = schlib.Sheet(
        NAME, title="PCB-0018 REV A power stage: 3x NTMFS5C628NL half-bridge, 3 mOhm Kelvin shunts",
        paper="A3", date="2026-09-27", company="hwde", pwr_base=400)
    lcsc: dict[str, str] = {}
    dnp: list[str] = []
    no_bom: list[str] = []

    for i, x in enumerate(LEGS):
        cx = COL_X[i]
        hs, ls = f"Q{401 + 2 * i}", f"Q{402 + 2 * i}"
        rg_h, rg_l = f"R{411 + 2 * i}", f"R{412 + 2 * i}"
        rp_h, rp_l = f"R{421 + 2 * i}", f"R{422 + 2 * i}"
        rs = f"R{401 + i}"
        nt_p, nt_n = f"NT{401 + 2 * i}", f"NT{402 + 2 * i}"
        caps = [f"C{401 + 4 * i + k}" for k in range(4)]
        sn_rh, sn_rl = f"R{431 + 2 * i}", f"R{432 + 2 * i}"
        sn_ch, sn_cl = f"C{431 + 2 * i}", f"C{432 + 2 * i}"
        tp = f"TP{401 + i}"
        ph, lsrc = f"PHASE_{x}", f"LS_SRC_{x}"
        g_h, g_l = f"GATE_H{x}", f"GATE_L{x}"

        # --- FETs (column centre)
        sh.add_component(FET, hs, "NTMFS5C628NL", at=(cx, 50.8),
                         footprint=FET_FP, expect=FET_EXPECT)
        sh.wire_pins(hs, {"1": ph, "2": ph, "3": ph, "4": g_h, "5": "VM"})
        _wire_all_drains(sh, hs, "VM")
        sh.add_component(FET, ls, "NTMFS5C628NL", at=(cx, 101.6),
                         footprint=FET_FP, expect=FET_EXPECT)
        sh.wire_pins(ls, {"1": lsrc, "2": lsrc, "3": lsrc, "4": g_l, "5": ph})
        _wire_all_drains(sh, ls, ph)
        lcsc[hs] = lcsc[ls] = "C145537"

        # --- gate resistors (series) and gate-source pull-downs, left of FETs
        for ref, y, a, b in ((rg_h, 38.1, f"GH{x}", g_h),
                             (rg_l, 88.9, f"GL{x}", g_l)):
            sh.add_component(f"{FP}:0603WAF100JT5E", ref, "10R", at=(cx - 38.1, y),
                             footprint=f"{FP}:R0603")
            sh.wire_pins(ref, {"1": a, "2": b})
            lcsc[ref] = "C22859"
        for ref, y, a, b in ((rp_h, 63.5, g_h, ph), (rp_l, 114.3, g_l, lsrc)):
            sh.add_component(f"{FP}:0603WAF1002T5E", ref, "10k", at=(cx - 38.1, y),
                             footprint=f"{FP}:R0603")
            sh.wire_pins(ref, {"1": a, "2": b})
            lcsc[ref] = "C25804"

        # --- shunt (LS source -> GND) and its two Kelvin net ties
        sh.add_component(SHUNT, rs, "3mR 2512 3W 1%", at=(cx, 142.24),
                         footprint=f"{FP}:R2512")
        sh.wire_pins(rs, {"1": lsrc, "2": "GND"})
        lcsc[rs] = "C5375459"
        sh.add_component(NETTIE, nt_p, "NetTie_2", at=(cx - 25.4, 160.02),
                         footprint=NETTIE_FP)
        sh.wire_pins(nt_p, {"1": lsrc, "2": f"ISNS_{x}_P"})
        sh.add_component(NETTIE, nt_n, "NetTie_2", at=(cx - 25.4, 172.72),
                         footprint=NETTIE_FP)
        sh.wire_pins(nt_n, {"1": "GND", "2": f"ISNS_{x}_N"})
        no_bom += [nt_p, nt_n]

        # --- leg MLCC bank VM -> GND (HS drain to shunt bottom)
        for k, ref in enumerate(caps):
            big = k < 3
            sh.add_component(
                f"{FP}:{'CS3225X7R106K500NRL' if big else '1210B104K500NT'}",
                ref, "10uF 50V X7R" if big else "100nF 50V X7R",
                at=(cx - 45.72 + k * 17.78, 195.58), footprint=f"{FP}:C1210")
            sh.wire_pins(ref, {"1": "VM", "2": "GND"})
            lcsc[ref] = "C2918502" if big else "C76567"
            # recorded against the HS drain pad: the leg's hard-switched
            # input loop; the 100 nF is the HF (<= 1 uF) member.
            sh.decoupling.append({"cap": ref, "ic": hs, "pin": "5",
                                  "rail": "VM",
                                  "value": "10uF 50V X7R" if big else "100nF 50V X7R",
                                  "role": "reg_input"})

        # --- DNP RC snubbers across each FET (D-S), right of FETs
        for rr, cc, y, d, s, mid in ((sn_rh, sn_ch, 38.1, "VM", ph, f"SNB_H{x}"),
                                     (sn_rl, sn_cl, 88.9, ph, lsrc, f"SNB_L{x}")):
            sh.add_component("Device:R", rr, "3.3R DNP", at=(cx + 25.4, y),
                             footprint=f"{FP}:R0603")
            sh.wire_pins(rr, {"1": d, "2": mid})
            sh.add_component("Device:C", cc, "2.2nF 100V DNP", at=(cx + 25.4, y + 17.78),
                             footprint=f"{FP}:C0603")
            sh.wire_pins(cc, {"1": mid, "2": s})
            dnp += [rr, cc]

        # --- phase output pad
        sh.add_component("Connector:TestPoint", tp, f"PHASE {x}", at=(cx + 25.4, 142.24),
                         footprint=PHASE_PAD_FP)
        sh.wire_pins(tp, {"1": ph})
        no_bom.append(tp)

    # interface: gate inputs, phase outputs, Kelvin sense pairs
    hier = []
    for x in LEGS:
        hier += [(f"GH{x}", "input"), (f"GL{x}", "input"),
                 (f"PHASE_{x}", "bidirectional"),
                 (f"ISNS_{x}_P", "output"), (f"ISNS_{x}_N", "output")]
    for j, (net, shape) in enumerate(hier):
        sh.hier_pin(net, shape=shape, at=(378.46, 30.48 + j * 7.62))

    # global rails (driven on power_in; no PWR_FLAG here). No power:VM symbol
    # exists; power:VCC carries VALUE "VM", which names the global net.
    sh.power_flag("VM", at=(25.4, 254.0), sym="power:VCC", flag=False)
    sh.power_flag("GND", at=(50.8, 254.0), sym="power:GND", flag=False)

    for ref, code in lcsc.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    for ref in dnp:
        # DNP alone: board_swig mirrors only the DNP flag onto the footprint,
        # so in_bom=False here is a parity mismatch; bom_cpl drops DNP sites.
        sh.mark_dnp(ref)
    for ref in no_bom:          # net ties and bare plated pads: nothing to buy
        sh.sch.components.get(ref).in_bom = False
    return sh


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else Path("/tmp/p18-power_stage")
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
