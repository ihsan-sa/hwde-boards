# P2 Architecture digest - esp32c3-node (2026-10-01)

- architecture/{blocks,power_tree,stackup,sheets,decisions}.md + constraints.json written.
- JLC2313_1.6 2L; sheets root + power (pwr 100) + main (pwr 200); nets VBUS, VBAT, VSYS, +3V3, GND,
  /USB_DP, /USB_DM, /VBAT_SENSE.
- Blocks: B1 usbc-sink, B2 li-charger (MCP73831 + AO3401A/B5819W), B3 ldo (RT9080-33),
  B4 mcu (ESP32-C3-MINI-1-N4), B5 bme280. U1 antenna at top edge, J1 bottom edge.
- Coverage P2 (log/coverage-P2.json, mapping 0 edges): 1 provisional, 5 gap. PCB-0015 checklists
  (ldo, mcu, usbc-sink) and 9 verified records reused into research/. Gaps recorded as
  "designing under coverage gap" decisions; no research loops (spend cap).
- H1 approved-by-delegate with the provisional list and accepted VBUS attach-charge deviation.
