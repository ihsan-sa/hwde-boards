# P1 Research digest - esp32c3-node (2026-10-01)

Roster (played inline by one agent, spend cap): component scout x4 (module, charger, ldo,
sensor-io), power architect, interface spec (usb-fs, from the canonical fragment),
reference design x2 (esp32c3-module, charger-loadshare), plus the XIAO comparison.

- Module ESP32-C3-MINI-1-N4 C2838502 (13.5k stock, 3.03 USD); -H4X alternate.
- Charger MCP73831-2 C424093 + AO3401A (Basic) + B5819W (Basic) load sharing; TP4054
  pin-compatible alternate. RPROG 5.1k -> 196 mA (provisional safety value).
- LDO RT9080-33 C841192 (600 mA, 2 uA Iq); AP2112K/ME6211 pin-compatible. Thermal is the
  binding limit on USB: 0.32 W worst sustained -> Tj ~114 C at 40 C (theta-JA 230.6).
- BME280 C92489 7.05 USD, Bosch-only; SHT40 fallback if stock drops.
- Straps per module DS: GPIO2/8 10k up, GPIO9 BOOT, EN 10k/1uF; LED GPIO10, VBAT GPIO3.
- USB-FS: 90 ohm dropped on 2L, no series R, USBLC6 at the receptacle, VBUS bulk <= 10 uF.
- XIAO: MIT licence covers Seeed's OSHW-XIAO-Series repo (library/docs); the wiki's
  C3 schematic/KiCad downloads state no licence. XIAO has no battery sense, external antenna.
