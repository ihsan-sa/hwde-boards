# P4 digest - schematic
- 7 sheets generated from kicad/gen/*.py (root.py stitches); ERC gate PASS 0/0, netlist_audit PASS.
- schematic-reviewer: 2 errors (LM5164 ripple injection, TP101/102 pad size) fixed; dispositions in reports/review-schematic.md.
- Closed OPEN items: C212 1 nF CFF on TPS61040 (datasheet eq. 6); L202 rated 1.05 A vs 0.47 A peak; C104 second 470 uF bulk cap (bus ripple), derating note in requirements.md; NT401-406 in leg groups.
- Kelvin: net ties NT401-406 must sit on the shunt pads' inner edge at P6.
- DNP: RC snubbers C431-436/R431-436 (placeholders 3.3R/2.2nF).
