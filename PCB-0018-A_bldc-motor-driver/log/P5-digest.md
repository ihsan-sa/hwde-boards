# P5 digest - board setup
- board_init PASS: 4L JLC04162H-7628A (2 oz outer), 4layer_2oz floors, parity 0, setup 0, unconnected 365 (P7's).
- Outline auto (shelf pack); target ~60-70 mm square is set at P6 with board_edit --outline.
- rules_gen PASS: 43 rules; classes Pwr_4p2566mm (VM_IN/VM/GND/phases 13 A), Pwr_2p9666mm, Pwr_0p225mm, Diff90 (ISNS pairs); 0.4 mm HV clearance on phase nets.
- Host note: stock libs passed via --fp-lib ~/.local/kicad10/usr/share/kicad/footprints; project fp-lib-table names MountingHole/NetTie/TestPoint via ${KICAD10_FOOTPRINT_DIR}.
- OPEN for P6/P7: silkscreen "PCB-0018 REV A" gr_text once the outline is final; ISNS diff pairs at 0.56 mm are wide for the CSA pins - neck down at the IC.
