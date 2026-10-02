# Power tree - PCB-0021-A

| Rail | Source | Range | Budget | Notes |
|---|---|---|---|---|
| VBUS | J1 | 4.5-5.5 V | 1.5 A (ILIM) | raw, before U1 |
| +SYS | U1 OUT | 4.4 V (USB) / VBAT (no USB) | boost Iin up to ~1.9 A (3.0 V cell) + 1.0 A charge | U1 dissipates up to ~1.1 W |
| VBAT | J2 | 3.0-4.2 V | charge 1.0 A / discharge ~2 A | cell assumed protected |
| +5V | U2 | 4.95 V typ | 1.0 A rated, ~1.3 A margin | ~0.45 W total loss |
LEDs 1-2 mA each from +SYS. Under full load plugged in, boost takes ~1.24 A of the 1.5 A limit, so charge falls to ~0.25 A (inherent; stated in spec). Charge 1 A is 1C only for a 1000 mAh cell: reduce RISET for smaller cells (PROVISIONAL). Reconciles research/power.md; no budget changed.
