# charger - 1S LiPo charger with power path (component scout, P1)

Must-haves: 4.20 V CC/CV, charge current settable to <= 200 mA (P0 provisional 0.5C of
400 mAh), thermal regulation, runs from USB 4.75-5.25 V, system runs with or without a cell.

| rank | mpn | lcsc | pkg | B/E | stock | price | fit |
|---|---|---|---|---|---|---|---|
| 1 | MCP73831T-2ACI/OT | C424093 | SOT-23-5 | E | 9441 | 0.78 | 4.20 V +/-0.75%, IREG = 1000 V/RPROG, thermal reg., + AN1149 load sharing = power path |
| 2 | TP4054-42-SOT25R | C32574 | SOT-23-5 | E | 27009 | 0.13 | pin-compatible alternate, same RPROG law |
| 3 | MCP73871-2CCI/ML | C511310 | QFN-20 4x4 | E | 1834 | 2.18 | integrated power path, but QFN-20 and 3x cost |
| 4 | BQ24074RGTR | C54313 | QFN-16 3x3 | E | 415 | 2.50 | integrated DPPM power path; stock too thin |
| 5 | ETA6003Q3Q | C5455585 | QFN-16 3x3 | E | 10320 | 0.52 | integrated power path; English datasheet not verified |

Power path decision input (for the architect): MCP73831 + P-MOSFET (AO3401A, Basic) +
Schottky (B5819W SL, Basic) is the Microchip AN1149 "load sharing" circuit. With VBUS
present the system is fed from VBUS through the Schottky and the PMOS gate (tied to VBUS)
holds the battery off the system, so the charger sees only the cell and terminates
correctly; without VBUS a 100k pulls the gate low and the PMOS connects the cell. That is
a true power path in function (load never steals termination current), for ~0.85 USD and
three SOT/SOD parts, no QFN. Integrated ICs win only on efficiency (DPPM) which a 200 mA
charge current does not need.

Grounding (parts/U2_MCP73831T-2ACI-OT_C424093.pdf): VREG 4.168-4.232 V (-2 option);
IREG 90-110 mA at PROG 10k; precondition 10% (AC option); termination 5%; VDD abs max 7.0 V;
4.7 uF in and out in the typical application.
Risk: AN1149 not fetched this run (citation from memory of the application note title -
marked OPINION until P2 coverage research or the schematic reviewer confirms it).
