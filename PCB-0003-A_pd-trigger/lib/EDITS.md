# Library edits - boards/pd-trigger/lib/aiee.pretty

Hand edits to pulled easyeda2kicad footprints. Every edit here was made by the P3
librarian agent under explicit orchestrator approval. Re-pulling a part with
`lib_pull.py --overwrite` DISCARDS these edits - re-apply from this file if that happens.
(Do not re-pull just to "clean up": the EasyEDA CAD endpoint rate-limits after ~3 passes,
and symbol pulls are not idempotent for names containing a space or `/`.)

Untouched by every edit below: all SMD pad geometry (position, size, shape, layers), all
courtyard geometry, all 3D model references, all `(property "LCSC Part" ...)` values.
Only `F.SilkS` graphics, two mechanical hole padstacks, and the `(model ...)` path string
changed.

## 2026-07-28 - P3 librarian

### Edit 0 (housekeeping, all 16 footprints): absolute 3D model paths

`lib_pull.py` was invoked with a RELATIVE `--out-dir`, and easyeda2kicad copies that
string verbatim into every footprint:

- BEFORE: `(model "boards/pd-trigger/lib/aiee.3dshapes/<name>.wrl"`
- AFTER:  `