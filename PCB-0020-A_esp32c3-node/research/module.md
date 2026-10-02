# module - WiFi/BLE MCU module (component scout, P1)

Live parts_search 2026-10-01; prices at qty 1 (build qty 5). Sweep: raw/module.json.

| rank | mpn | lcsc | pkg | B/E | stock | price | fit |
|---|---|---|---|---|---|---|---|
| 1 | ESP32-C3-MINI-1-N4 | C2838502 | SMD 13.2x16.6 | E | 13531 | 3.03 | PCB antenna, 4 MB flash, pre-certified, native USB IO18/IO19 |
| 2 | ESP32-C3-MINI-1-H4X | C41349510 | same | E | 1348 | 2.95 | 105 C rated, pin-compatible alternate |
| 3 | ESP32-C3-MINI-1U-N4 | C2911374 | SMD 13.2x12.5 | E | 2117 | 3.13 | U.FL version: no keep-out but adds antenna+cable |

Pick for P3: -1-N4 (brief prefers PCB antenna; -1U only if the keep-out cannot sit at an
edge, and it can - the module goes at a short edge with the antenna overhanging/at the edge).

Risks: Espressif is single-source by nature; -H4X is the in-family alternate. MSL 3
(168 h floor life) - JLC handles baking. Datasheet: ESP32-C3-MINI-1 & MINI-1U v2.2
(parts/U1_esp32-c3-mini-1_datasheet_en.pdf).
