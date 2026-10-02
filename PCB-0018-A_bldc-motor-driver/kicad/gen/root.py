"""Root generator for PCB-0018-A bldc-motor-driver: stitches the seven sheets.

One generator per sheet (architecture/sheets.md) + this root, per the P4
pattern. Each child's sheet-pin list is read from its own `Sheet.hier_pins`,
so the root never hand-transcribes interface nets. Rails (VM, +12V, +5V,
+3V3, GND) are global power symbols inside the sheets and need no sheet pin.
Root-sheet parts: the M3 corner holes H1-H4.

Rebuild:  ~/.local/hwde-venv/bin/python PCB-0018-A_bldc-motor-driver/kicad/gen/root.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "hwde" / "scripts"))
sys.path.insert(0, str(HERE.parent))

import schlib  # noqa: E402
import gate_driver  # noqa: E402
import mcu  # noqa: E402
import power_in  # noqa: E402
import power_stage  # noqa: E402
import regulators  # noqa: E402
import sensing  # noqa: E402

import importlib.util  # noqa: E402

# The io sheet's module name shadows stdlib `io`; load it by path.
_spec = importlib.util.spec_from_file_location("io_sheet", HERE.parent / "io.py")
io_sheet = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(io_sheet)

PROJECT = "PCB-0018-A_bldc-motor-driver"
GRID = 1.27
WIDTH = 50.8
GAP = 12.7
COL_X = (101.6, 203.2, 304.8)


def _snap(v: float) -> float:
    return round(round(v / GRID) * GRID, 4)


def _height(n_pins: int) -> float:
    """schlib needs h > 2*GRID*n_pins for the pin stack; add a margin."""
    return _snap(max(25.4, 2 * GRID * (n_pins + 3)))


def build() -> schlib.Project:
    root = schlib.Sheet(PROJECT, title="PCB-0018 REV A 3-phase BLDC motor driver: root",
                        paper="A3")
    for i, (x, y) in enumerate([(25.4, 50.8), (25.4, 63.5), (25.4, 76.2), (25.4, 88.9)], 1):
        root.add_component("Mechanical:MountingHole", f"H{i}", "M3", at=(x, y),
                           footprint="MountingHole:MountingHole_3.2mm_M3")
        # the stock footprint is exclude_from_bom; match it or parity flags it
        root.sch.components.get(f"H{i}").in_bom = False
    proj = schlib.Project(root)

    children = [power_in.build(), regulators.build(), gate_driver.build(),
                power_stage.build(), sensing.build(), mcu.build(), io_sheet.build()]
    x_i, y = 0, 25.4
    for child in children:
        nets = sorted(child.hier_pins)
        h = _height(len(nets))
        if y + h > 260.0:
            x_i += 1
            y = 25.4
        if x_i >= len(COL_X):
            raise ValueError("ran out of columns on A3")
        proj.add_sheet(child, at=(COL_X[x_i], _snap(y)), size=(WIDTH, h), nets=nets)
        y = _snap(y + h + GAP)
    return proj


GLOBAL_RAILS = {"VM", "GND", "+5V", "+12V", "+3V3"}


def _qualify(child, net: str) -> str:
    """Name a net as the exported netlist does: global power rails bare,
    sheet-pin nets at root level (/NET), the rest sheet-local (/sheet/NET).
    schlib records the name the sheet wired, which netlist_audit cannot
    match for anything but a global rail."""
    if net in GLOBAL_RAILS or net.startswith("/"):  # already qualified
        return net
    if net in child.hier_pins:
        return f"/{net}"
    return f"/{child.name}/{net}"


def _write_decoupling(proj, path: Path) -> None:
    assocs = list(proj.root.decoupling)
    for child in proj.children:
        for a in child.decoupling:
            a = dict(a)
            a["rail"] = _qualify(child, a["rail"])
            a["gnd"] = _qualify(child, a.get("gnd", "GND"))
            assocs.append(a)
    path.write_text(json.dumps({"associations": assocs}, indent=1) + "\n",
                    encoding="utf-8")


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else HERE.parents[1]  # .../kicad
    try:
        proj = build()
        sch = proj.save(out_dir)
        _write_decoupling(proj, out_dir / "decoupling.json")
    except Exception as exc:  # noqa: BLE001  (any error -> exit 2)
        print(json.dumps({"script": "gen.bldc-motor-driver", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({
        "script": "gen.bldc-motor-driver",
        "status": "pass",
        "root": str(sch),
        "files": sorted(p.name for p in out_dir.glob("*.kicad_sch")),
        "sheet_pins": {c.name: sorted(c.hier_pins) for c in proj.children},
        "decoupling_associations": len(proj.decoupling),
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
