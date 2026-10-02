# PCB-0020-A esp32c3-node vs the Seeed Studio XIAO ESP32C3

The brief asked for a small WiFi + Bluetooth LE sensor node "in the spirit of" the Seeed XIAO ESP32C3.
Nothing was copied from its schematic or layout: this board comes from a few-line brief and the vendor
datasheets. The XIAO's figures are from Seeed's wiki and one third-party write-up (research/reference-xiao-esp32c3.md).

**Original and licence.** The XIAO ESP32C3 is by Seeed Studio. Its wiki offers the schematic PDF and a
KiCad project but states no licence for them. Seeed's `OSHW-XIAO-Series` GitHub repository is MIT
licensed, but it holds the XIAO symbol and footprint library and docs, not this board's design files, so
I don't assume the MIT grant covers the board itself.

| | XIAO ESP32C3 | esp32c3-node, PCB-0020 rev A |
|---|---|---|
| Board size | 21 x 17.8 mm | 26 x 38 mm, 2 layers |
| Radio | bare ESP32-C3 SoC, external antenna on U.FL | ESP32-C3-MINI-1 certified module, PCB antenna over the board edge with its keep-out |
| USB | USB-C, native USB | USB-C, native USB, plus USBLC6 ESD and 5.1k CC pull-downs |
| Charger | ETA4054-class linear, ~380 mA | MCP73831 linear, ~200 mA (0.5C for a 400 mAh cell) |
| Power path | not verified | Schottky + PMOS load sharing, so it runs with or without a cell |
| 3.3 V | 500 mA LDO | RT9080, 600 mA, 2 uA quiescent |
| Battery sense | none (no free pin) | 1M/1M divider into an ADC pin |
| Battery connector | solder pads | JST-PH 2-pin |
| Sensor | none | BME280 on I2C, placed away from the LDO and module |
| Expansion | 11 GPIO on castellated pins | Qwiic (JST-SH) plus 0.1 in edge pads |
| Buttons, LEDs | BOOT, RESET, charge LED | BOOT, RESET, charge LED and a user status LED |
| Fabricated / measured | yes, a shipping product | no, fab package only |

## Where they differ, and why

- **Ours is about 2.6 times the area.** The XIAO's size comes from a bare SoC and an external antenna.
  The brief asked for the MINI-1 module, which is pre-certified but 13.2 x 16.6 mm on its own and needs
  a copper-free keep-out at the edge. The sensor, two connectors and the power-path parts take the rest.
- **The sensor-node parts are additions.** The BME280, Qwiic port, battery sense and user LED are in
  the brief and aren't on the XIAO. Seeed's wiki says the XIAO has no battery sense because the pins ran
  out; the MINI-1 leaves enough GPIO for it here.
- **Slower charge.** I set ~200 mA to suit a small cell. The XIAO charges at ~380 mA.
- **The same core.** Both use native ESP32-C3 USB on USB-C, a linear single-cell charger, a 3.3 V LDO
  and BOOT/RESET buttons.

## What neither board's numbers prove here

Ours hasn't been built. Its verify pass holds only with the waivers listed in the PR: the full-speed
USB pair isn't impedance-controlled, and GND is marked plane-fed. The XIAO's power path and LDO part
number weren't checked against its schematic.
