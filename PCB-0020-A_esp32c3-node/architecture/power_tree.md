# power tree - esp32c3-node (P2)

Lifted from research/power.json, reconciled against the final blocks.

| Rail | Source | Current budget | Consumers | Dissipation |
|---|---|---|---|---|
| VBUS | USB-C 4.75-5.25 V | 0.5 A (default USB) | U2 charger 0.20 A, D3 -> VSYS 0.25 A avg / 0.45 A peak, U4 ref | ~0 |
| VBAT | 1S LiPo 3.0-4.2 V | 0.45 A discharge / 0.20 A charge | Q1 -> VSYS, divider 2.1 uA | Q1 ~14 mW |
| VSYS | D3 (VBUS - ~0.45 V) or Q1 (VBAT) | 0.45 A | U3 VIN | D3 ~0.11 W |
| +3V3 | U3 RT9080-33 | 0.45 A peak | U1 350 mA TX peak, U5 < 1 mA, LEDs ~3 mA, Qwiic 100 mA | U3 0.32 W worst |

- Worst USB draw: 0.20 A charge + 0.45 A system peak = 0.65 A transient above the 0.5 A
  default; average system load is ~0.1 A (WiFi duty), so the steady draw is < 0.35 A.
  The charger's own current falls as VBUS sags (its input regulation); accepted.
- Battery-only: dropout limits the run to cells >= ~3.6 V at 450 mA peak; below that the
  3V3 rail tracks VBAT - 0.3 V. ESP32-C3 operates down to 3.0 V. Accepted.
- U3 thermal: 0.32 W x 230.6 C/W -> Tj ~114 C at 40 C; GND pad to B.Cu with >= 2 vias.
- VBUS attach charge ~65 uC exceeds the USB 2.0 50 uC / 10 uF guideline (D3 + C3 + C10
  charge through the Schottky). Accepted deviation: the LDO current limit bounds the surge.
