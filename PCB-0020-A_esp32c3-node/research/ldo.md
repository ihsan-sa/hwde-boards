# ldo - 3.3 V regulator (component scout, P1)

Must-haves: >= 500 mA (module peak 350 mA + 100 mA Qwiic), dropout small enough to run
from a 3.5 V cell, low Iq (battery), Vin up to ~5 V (VBUS minus Schottky), ceramic stable.

| rank | mpn | lcsc | pkg | B/E | stock | price | fit |
|---|---|---|---|---|---|---|---|
| 1 | RT9080-33GJ5 | C841192 | TSOT-23-5 | E | 40252 | 0.12 | 600 mA, 0.31 V dropout @600 mA, 2 uA Iq, Vin 1.2-5.5 V |
| 2 | AP2112K-3.3TRG1 | C51118 | SOT-23-5 | E | 39133 | 0.17 | pin-compatible, 600 mA, 55 uA Iq |
| 3 | ME6211C33M5G-N | C82942 | SOT-23-5 | E | 165213 | 0.06 | pin-compatible, 500 mA |
| 4 | XC6206P332MR-G | C5446 | SOT-23 | B | 474665 | 0.14 | only Basic option; 200 mA - rejected |

RT9080 (parts/U3_RT9080-33GJ5_C841192.pdf): VIN/VOUT/EN abs max 6.5 V; theta-JA 230.6 C/W
(TSOT-23-5, 2-layer EVB); current limit 610 mA min; thermal shutdown 150 C typ.
Risk: theta-JA is the binding limit on USB at full load - see power.md.
No Basic LDO meets 500 mA in a small package (AMS1117 SOT-223 has 1.1 V dropout: it cannot
run from a LiPo).
