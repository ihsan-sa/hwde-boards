# sheets - esp32c3-node (P2)

Root `esp32c3-node.kicad_sch` holds two sheet symbols. Global power nets (power symbols, bare
names): VBUS, VBAT, VSYS, +3V3, GND. Root-level labels between the sheets: /USB_DP, /USB_DM,
/VBAT_SENSE.

## power.kicad_sch (B1, B2, B3), pwr_base=100
J1 USB-C; R1, R2 5.1k CC; D1 SMF5.0A; U4 USBLC6-2SC6; C1 4.7u VBUS; U2 MCP73831; C2 4.7u VBAT;
R3 5.1k RPROG; D2 red LED + R4 1k (STAT); J2 JST-PH 2-pin (pin 1 = +); Q1 AO3401A; R5 100k;
D3 B5819W; U3 RT9080-33; C3 1u VSYS; C4 1u +3V3; R6, R7 1M divider; C5 100n.
Refdes ranges: J1-J2, U2-U4, Q1-Q9, D1-D9, R1-R9, C1-C9.

## main.kicad_sch (B4, B5), pwr_base=200
U1 ESP32-C3-MINI-1-N4; C10 10u, C11 100n; R10 10k + C12 1u EN; SW1 RESET; SW2 BOOT;
R11, R12, R13 10k pull-ups IO9/IO8/IO2; D10 green LED + R16 1k on IO10; U5 BME280; C13, C14 100n;
R14, R15 4.7k I2C; J3 Qwiic; J4 1x8 edge pads; J5 1x4 power pads.
Refdes ranges: U1, U5-U9, J3-J9, D10-D19, R10-R19, C10-C19, SW1-SW9.

## Interface-net contract
| Net | From | To |
|---|---|---|
| VBUS | J1 | D1, U4.5, C1, U2 VDD, D3 A, Q1 G, R4, J5 |
| VBAT | U2 VBAT | C2, J2.1, Q1 D, R6, J5 |
| VSYS | D3 K, Q1 S | U3 VIN/EN, C3 |
| +3V3 | U3 VOUT | C4, U1, U5, R10-R15, J3.2, J5 |
| /USB_DP, /USB_DM | J1 D+/D- (both rows joined) via U4 | U1 IO19 / IO18 |
| /VBAT_SENSE | R6/R7 midpoint, C5 | U1 IO3 |
| /main/SDA, /main/SCL | U1 IO6 / IO7 | U5, J3, R14/R15 |
| /main/EN, /main/BOOT, /main/LED | U1 EN / IO9 / IO10 | C12+SW1 / SW2 / R16-D10 |

J4 edge pads: IO0, IO1, IO2, IO4, IO5, IO8, IO20, IO21. J5: VBUS, VBAT, +3V3, GND.
