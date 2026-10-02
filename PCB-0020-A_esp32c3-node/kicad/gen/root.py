"""esp32c3-node ROOT sheet: stitches `power` + `main` into
PCB-0020-A_esp32c3-node.kicad_sch (project name = workspace name).

SOURCE; every .kicad_sch under kicad/ and kicad/decoupling.json are BUILD
OUTPUT. Rebuild from the repo root:

    ~/.local/hwde-venv/bin/python PCB-0020-A_esp32c3-node/kicad/gen/root.py

Rails are global power symbols on both children; the only sheet pins are
the three cross-sheet signals, joined on the root by labels so their final
netlist names are /USB_DP, /USB_DM, /VBAT_SENSE (constraints.json).
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
import power_sheet  # noqa: E402
import main_sheet  # noqa: E402

PROJECT = BOARD.name          # PCB-0020-A_esp32c3-node
NETS = ["USB_DP", "USB_DM", "VBAT_SENSE"]


def build() -> schlib.Project:
    root = schlib.Sheet(
        PROJECT,
        title="PCB-0020-A esp32c3-node: ESP32-C3 LiPo sensor node",
        paper="A4", date="2026-10-01", company="ai-ee")
    proj = schlib.Project(root)
    proj.add_sheet(power_sheet.build(), at=(76.20, 50.80),
                   size=(50.80, 38.10), nets=NETS)
    proj.add_sheet(main_sheet.build(), at=(76.20, 114.30),
                   size=(50.80, 38.10), nets=NETS)
    return proj


def _strip_klc_private(path: Path) -> int:
    """Drop `(property private "KLC_..." ...)` blocks that kicad-sch-api
    mis-serialises from stock KiCad symbols (PCB-0015 root.py)."""
    text = path.read_text(encoding="utf-8")
    needle = '(property private "KLC_'
    out, i, n = [], 0, 0
    while True:
        j = text.find(needle, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        depth, k = 0, j
        while k < len(text):
            if text[k] == "(":
                depth += 1
            elif text[k] == ")":
                depth -= 1
                if depth == 0:
                    k += 1
                    break
            k += 1
        i, n = k, n + 1
    if n:
        path.write_text("".join(out), encoding="utf-8")
    return n


def main(argv=None) -> int:
    out_dir = Path(argv[0]) if argv else HERE.parents[1]
    try:
        proj = build()
        sch = proj.save(out_dir, decoupling=out_dir / "decoupling.json")
        stripped = sum(_strip_klc_private(p) for p in
                       [sch, out_dir / "power.kicad_sch",
                        out_dir / "main.kicad_sch"])
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"script": "gen.root", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({"script": "gen.root", "status": "pass",
                      "root": str(sch),
                      "decoupling_associations": len(proj.decoupling),
                      "klc_private_properties_stripped": stripped}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
