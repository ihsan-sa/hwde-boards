# reference - Seeed Studio XIAO ESP32C3 (comparison, P1)

Purpose: a fair comparison with the board this brief was written "in the spirit of".
Nothing from its schematic is copied; our design comes from the brief and the vendor
datasheets. Web reading 2026-10-01, sources at the end.

## What the XIAO ESP32C3 has

- Size 21 x 17.8 mm (wiki spec table).
- SoC: ESP32-C3 on the board itself (not a MINI module); antenna is EXTERNAL - a U.FL
  connector with an included external antenna (wiki: "external RF antenna included",
  U.FL-R-SMT1).
- USB-C, native ESP32-C3 USB (no bridge chip mentioned on the wiki).
- Charger: ETA4054 (or equivalent XC6802) linear Li-ion charger, ~370-380 mA fast /
  40 mA trickle (wiki: "380mA(Fast) / 40mA(Trickle)"; third-party write-up names the IC).
- 3.3 V: an LDO rated 500 mA (wiki); a third-party summary names it TLV75733P - NOT
  verified against the schematic PDF this run.
- Battery sense: NONE on board. The wiki says: "Due to the limitation of the number of
  pins in the ESP32C3, engineers had no extra pins to allocate to the battery for voltage
  measurement" and suggests an external divider on A0.
- Battery: BAT+/BAT- solder pads on the bottom, no connector.
- LED: one red LED tied to the charger, no user LED on a GPIO (third-party write-up).
- Sensor / Qwiic: none.
- Power path topology (how VBUS and the cell are combined): NOT verified - the schematic
  PDF was not read, to keep this comparison inside its budget.

## Licence of the design files

- The wiki's resource list offers the "XIAO ESP32-C3 Schematic" (PDF) and the
  "XIAO ESP32-C3 KiCad Project". The wiki page states NO licence for these files.
- Seeed's GitHub repo `Seeed-Studio/OSHW-XIAO-Series` carries an MIT License
  ("Copyright (c) 2024 Seeed-Projects", checked via the GitHub API, license key `mit`).
  That repo holds the XIAO KiCad symbol/footprint library (including
  `XIAO-ESP32-C3-SMD.kicad_mod`), docs and a project index; I found no ESP32-C3 board
  schematic or board KiCad project in its file tree, so the MIT grant covers the library
  and docs, and I would not assume it covers the board design files on the wiki.
- I did not open the downloadable KiCad project archive to look for a licence file inside.

## Same / different vs our architecture (PCB-0020-A)

| aspect | XIAO ESP32C3 | esp32c3-node (ours) |
|---|---|---|
| radio | ESP32-C3 SoC on board, external U.FL antenna | ESP32-C3-MINI-1 pre-certified module, PCB antenna at the board edge |
| size | 21 x 17.8 mm | larger (module 13.2 x 16.6 mm + keep-out at an edge + sensor + 2 connectors); earned at P6, soft target |
| USB | USB-C, native C3 USB | same; plus USBLC6 ESD and 5.1k CC Rd (verified on ours) |
| charger | ETA4054-class linear, ~380 mA | MCP73831 linear, ~196 mA (0.5C of 400 mAh, conservative) |
| power path | not verified | Schottky + PMOS load sharing - runs with or without a cell, charger terminates cleanly |
| 3.3 V | 500 mA LDO | RT9080 600 mA, 2 uA Iq |
| battery sense | none (pins ran out) | 1M/1M divider + 100 nF into GPIO3 ADC1_CH3 |
| battery connection | solder pads | JST-PH 2-pin SMD |
| sensor | none | BME280 on I2C, away from LDO/module heat |
| expansion | castellated/0.1 in pins, 11 GPIO | Qwiic JST-SH + plated 0.1 in edge pads for spare GPIOs |
| buttons | BOOT + RESET | BOOT (GPIO9) + RESET (EN) |
| user LED | none (charge LED only) | status LED on GPIO10 + charge LED on STAT |

Fair summary: the XIAO buys its size with an external antenna, a bare SoC and no
connectors; ours spends area on a certified module with a PCB antenna, a sensor and two
connectors, and adds battery sense and a verified power path.

## Sources

- https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/ (spec table, battery note,
  resources list)
- https://github.com/Seeed-Studio/OSHW-XIAO-Series (LICENSE file, file tree)
- https://mischianti.org/seeed-studio-xiao-esp32-c3-high-resolution-pinout-datasheet-schema-and-specs/
  (charger IC name, LED wiring - third party)
- Search-result summary naming the LDO TLV75733P (unverified; third party)
