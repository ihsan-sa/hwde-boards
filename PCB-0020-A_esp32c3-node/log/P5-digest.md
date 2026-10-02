# P5 digest - board setup (2026-10-01)
- board_init: 2L JLC2313_1.6 (1 oz), fab profile 2layer_1oz (clr/track 0.127, via 0.6/0.3, edge 0.3), no
  mounting holes (requirements 5), corner r 2 mm, outline auto (provisional; P6 earns it with --outline fit).
- Self-check: parity 0, setup violations 0, unconnected 142 (P7's). log/board_init-P5.json, log/drc-P5.json.
- rules_gen: 15 generated rules + classes Pwr_0p25mm (VBUS/VSYS/VBAT/+3V3), Pwr_0p35mm (GND), Diff140 (USB pair
  0.20/0.30 mm). Constraints diff_pairs impedance_ohm set to 140 = the natural uncontrolled geometry; the skill
  defaults a missing value to 90 ohm, which solved to 1.09 mm traces.
- J1 USB-C: lib footprint GND/VBUS pad stroke removed (0.7 -> 0.6 mm, datasheet); hand DRU rule
  aiee_samefp_J1_usbc (J1 pad-to-pad 0.127). A rules_gen re-run drops it - re-append from progress-P5.md.
- Sidecars beside the board: kicad/constraints.json, kicad/decoupling.json.
- P6 started: hand placement on 26 x 38 mm (r 1 mm), antenna overhangs top; gate place PASS; H3 pending.
