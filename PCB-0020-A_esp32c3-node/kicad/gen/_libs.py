"""Register the symbol libraries the generators use with kicad-sch-api's
global cache (it never reads kicad/sym-lib-table): the board's pulled lib
plus KiCad's stock power and Connector_Generic libs."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import kicad_sch_api as ksa


def _stock_symbol_dir() -> Path:
    for var in ("KICAD10_SYMBOL_DIR", "KICAD9_SYMBOL_DIR", "KICAD_SYMBOL_DIR"):
        if os.environ.get(var) and Path(os.environ[var]).is_dir():
            return Path(os.environ[var])
    cli = shutil.which("kicad-cli")
    if cli:
        root = Path(cli).resolve().parent.parent
        for cand in (root / "usr" / "share" / "kicad" / "symbols",
                     root / "share" / "kicad" / "symbols"):
            if cand.is_dir():
                return cand
    return Path("/usr/share/kicad/symbols")


def register(board: Path) -> None:
    cache = ksa.get_symbol_cache()
    cache.add_library_path(board / "lib" / "aiee.kicad_sym")
    stock = _stock_symbol_dir()
    for lib in ("power", "Connector_Generic"):
        cache.add_library_path(stock / f"{lib}.kicad_sym")
