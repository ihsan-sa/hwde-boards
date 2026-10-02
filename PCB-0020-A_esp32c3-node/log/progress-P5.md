# progress P5 (board setup) + P6 placement (2026-10-01)
Started: P5 per agents/board-setup.md (inline), then P6 placement, stop at H3.

## Owner-visible waivers
- USB D+/D- are routed as an uncontrolled 0.20/0.30 mm pair (~140 ohm), not 90 ohm. The constraints now record 140 because rules_gen silently assumes 90 ohm and sized 1.09 mm traces. USB full speed over < 30 mm is fine with it.
- J1 USB-C library footprint edited: the GND/VBUS pad outline stroke was removed, so copper is the datasheet 0.6 mm, not 0.7 mm. A lib_pull re-run would undo it.
- Hand DRU rule aiee_samefp_J1_usbc: J1's own pads may sit 0.127 mm apart (VBUS-CC is 0.15 mm by design). A rules_gen re-run drops it.
- U1 antenna overhangs the top edge by ~5.4 mm (Espressif's preferred option). The keep-out sits fully off-board. JLC assembly may ask about an overhanging part.
- Constraints placement.edges gained J2 bottom and J3 right (architecture notes asked for J2/J3 on free edges).
- Board is 26 x 38 mm (plus the 5.4 mm antenna overhang), longer than the 32-36 mm estimate. Three connectors, two 5 mm tactile switches and two 0.1 in edge rows need the room.
- The interim drc gate fails on 142 unconnected items only (0 real errors). gates.yaml says those should be warnings before routing, but the project file rates them as errors (skill mismatch).

## Journal
- P5 board_init: 2L JLC2313_1.6, 2layer_1oz floors (clr 0.127, track 0.127, via 0.6/0.3, edge 0.3), 0 holes, r=2 mm, outline auto (provisional 79x102). parity 0, unconnected 142 (P7), 4 DRC errors = J1 USB-C pad-pad 0.15 < Default class clearance (fixing next). log/board_init-P5.json
- P5 rules_gen: rc0, 2layer_1oz, classes Pwr_0p25mm (VBUS/VSYS/VBAT/+3V3), Pwr_0p35mm (GND), Diff140 for USB. Gotcha: rules_gen defaults a missing diff impedance to 90 ohm -> 1.09 mm traces; set constraints diff_pairs impedance_ohm=140 (natural 0.2/0.3 geometry, uncontrolled) in architecture/ + kicad/ copies.
- P5 J1 fix: (a) lib USB-C footprint GND/VBUS custom pads had a 0.1 mm poly stroke -> 0.7 mm copper, 0.10 mm gap (< 0.127 floor); stroke set to 0 + fill -> datasheet 0.6x1.3 mm. (b) DRU hand rule aiee_samefp_J1_usbc (clearance 0.127 between J1's own pads; VBUS-CC 0.15 < power-class 0.2). rules_gen re-run DROPS it - re-append.
- P5 re-ran board_init (rc0) + rules_gen (rc0) + rule append. DRC --parity: parity 0, setup violations 0, unconnected 142. P5 DONE. Next: set-phase P6, place_seed, anneal.
- P6: seed applied (hpwl 2200->1074). Plan: hand placement W=26 (J4 right rot180, J5 left, U1 antenna overhangs top), J1/J2/J3 mate off bottom, U5 bottom-right. Writing place/hand.ops.json
- P6: hand placement applied (place/hand.ops.json), outline 26x38 r1 via board_edit. Gate overlap shape = courtyard+padded pads (~1mm bigger) -> 23 overlaps. J3 moved to right edge (constraints edge right), locked U1 J1-J5 SW1 SW2; running anneal to legalize small parts. Backup place/hand-prelegal.kicad_pcb
- P6: anneal (no side flips) found no legal candidate (19 viol) - discarded. Hand legalization against placelib precise shapes (place/legal.ops.json, planner scratch/plan.py). Gate place PASS a3 (0 violations). Next: silk_place, drc interim gate, render, H3.
- P6: silk_place moved 33/41 refdes, 8 residual (J5 U2 Q1 ...; channel too narrow) - fix in the P9 silk sweep or hide tiny-part refdes. Render reports/place/*_top.png: J1/J2 mate off bottom, J3 off right, antenna off top. Gate place PASS (log/gate-place-a3.json).
- DONE: P5 complete; phase P6 with place gate green. STOP at H3 (placement render review, default ON). NEXT after H3: board_edit --outline keep if needed, P7 routing (USB pair down the x 29.4-31.3 channel between SW and J4; no pour under U5).
- STOPPED at context bound. ERC re-check (log/gate-erc-recheck.json) exit 1 after constraints.json edits - UNREAD; likely freshness/sidecar, not a schematic change (schematic untouched in P5/P6). NEXT: read that file, fix/re-run erc gate, then H3.
