# P4 digest - schematic (2026-10-01)
- Generators: kicad/gen/power_sheet.py, main_sheet.py, root.py (+ _libs.py). Build output:
  kicad/PCB-0020-A_esp32c3-node.kicad_sch + power/main sheets + kicad/decoupling.json (8 assoc).
- 41 parts, 48 nets; interface nets match the sheets.md contract (/USB_DP, /USB_DM, /VBAT_SENSE
  root labels; VBUS/VBAT/VSYS/+3V3/GND global). PWR_FLAGs on VBUS, VSYS, GND.
- Gate erc: PASS attempt 1 (0 errors, 0 warnings). netlist_audit: pass (182/182 pins).
- schematic-reviewer: 0 errors, 6 warnings, all dispositioned in reports/erc-waivers.md.
- J4/J5 edge pads use stock Conn_01x08/01x04 + PinHeader 2.54 footprints copied into lib/aiee.pretty, DNP.
- Files for H2: reports/schematic.pdf, reports/review-schematic.md, reports/erc-waivers.md,
  reports/design_doc/.
