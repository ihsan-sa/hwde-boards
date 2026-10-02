# P6 digest - placement (2026-10-01)
- 26 x 38 mm, r 1 mm, 2 layers; U1 antenna overhangs the top edge ~5.4 mm (keep-out fully off-board).
- J1 USB-C and J2 mate off the bottom, J3 off the right, J4/J5 0.1 in rows on right/left edges; U1, J1-J5, SW1/2 locked.
- seed + anneal could not legalize; hand legalization (place/legal.ops.json). Gate place PASS (log/gate-place-H3.json).
- Silk: silk_place moved 33/41 refdes; the 8 that had no room (J5 U2 Q1 R5 R13 C3 R15 D10) now sit on B.SilkS.
  Footprint-outline silk overlaps between neighbours remain (~67 warnings) - P7's drc_routed sees them.
- ERC re-check PASS: added stock power + Connector_Generic libs to kicad/sym-lib-table.
- H3 approved by delegate (state.json human.3).
