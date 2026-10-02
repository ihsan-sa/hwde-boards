# sensor-io - sensor, ESD, connectors, buttons (component scout, P1)

| function | mpn | lcsc | pkg | B/E | stock | price | fit |
|---|---|---|---|---|---|---|---|
| T/RH/P sensor | BME280 | C92489 | LGA-8 2.5x2.5 | E | 4847 | 7.05 | Bosch; BMP280 has 0 stock, so no fallback in family |
| USB ESD | USBLC6-2SC6 | C7519 | SOT-23-6 | E | 37351 | 0.18 | ST original; clone C2827654 0.045 |
| USB-C | TYPE-C-31-M-12 | C165948 | SMD 16P | E | 449864 | 0.19 | D+/D- pins, used on PCB-0015 |
| battery conn | S2B-PH-SM4-TB | C295747 | SMD RA 2.0 mm | E | 21059 | 0.24 | JST original |
| Qwiic | SM04B-SRSS-TB | C160404 | SMD RA 1.0 mm | E | 35535 | 0.26 | JST original, used on PCB-0015 |
| buttons | TS-1187A-B-A-B | C318884 | SMD 5.1x5.1 | B | 477817 | 0.02 | Basic |

Risks: BME280 is the single most expensive part (7 USD) and single-source; if stock
drops below 25 at P3, fall back to SHT40 (proven on PCB-0015) and lose pressure.
