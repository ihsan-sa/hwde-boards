# PCB-0017-A stereo-class-d-amp - schematic sheet plan (P2)

## Ruling: ONE sheet, no hierarchy

38 fitted parts around one IC, on one signal path (J2 -> U1 -> LC -> J3/J4) with
one rail. A hierarchy would buy nothing but hierarchical pins and sheet-path net
names; a single A3-class sheet shows the whole amplifier at a glance and the
placement groups at P6 read straight off it. Root sheet = the only sheet:
`PCB-0017-A_stereo-class-d-amp.kicad_sch` (same name as the KiCad project and the
workspace directory, boards CLAUDE.md).

Net naming: power nets bare (`+12V`, `GND`); every other net is a local label
and carries a leading `/` in the netlist (`/OUTPL`). These are the CANONICAL
names: `constraints.json` uses them and the schematic must produce them exactly.

## Drawing layout (left to right, mirroring the board)

J2 and the four input caps at the far left; U1 in the middle drawn with pins
1-16 on its left and 17-32 on its right (the DAP footprint's own orientation:
pin 1 top-left, PVCC 31/32 top-right, AVCC/PVCC 17-19 bottom-right); the
configuration cluster (R1, R2, R3, C5, the MODSEL/AM/SYNC ties) below-left of
U1; bootstrap and PVCC decoupling caps drawn at their pins on the right; the two
LC filters to the right of U1 with the right channel above the left (matching
pins 27/29 above 21/23); J4 then J3 at the far right; J1 with C13/C14 along the
top right; TP1 on GND anywhere; one PWR_FLAG each on `+12V` and `GND` (external
rail, no on-board source - ERC needs them).

## Pin-by-pin tie table (TI SLOS708G, DAP package - P3/P4 verify against the symbol)

| pin | name | net | tie / part |
|---|---|---|---|
| 1 | MODSEL | `GND` | BD mode |
| 2 | SDZ | `/SDZ` | joined with FAULTZ; R2 100k to `+12V` |
| 3 | FAULTZ | `/SDZ` | open-drain, same node as SDZ (auto-clearing fault) |
| 4 | RINP | `/RINP` | C3 2.2 uF from `/IN_R` |
| 5 | RINN | `/RINN` | C4 2.2 uF to `GND` |
| 6 | PLIMIT | `/GVDD` | direct tie, no limit |
| 7 | GVDD | `/GVDD` | C5 1 uF to `GND` |
| 8 | GAIN/SLV | `/GAIN` | R1 5.6k to `GND`, GVDD leg open: 20 dB master |
| 9 | GND | `GND` | |
| 10 | LINP | `/LINP` | C1 2.2 uF from `/IN_L` |
| 11 | LINN | `/LINN` | C2 2.2 uF to `GND` |
| 12 | MUTE | `/MUTE` | R3 100k to `GND` (outputs enabled) |
| 13 | AM2 | `GND` | 400 kHz (AM2/AM1/AM0 = 0/0/0) |
| 14 | AM1 | `GND` | |
| 15 | AM0 | `GND` | |
| 16 | SYNC | no connect | output in master mode; ERC no-connect flag |
| 17 | AVCC | `+12V` | C6 100 nF to `GND` at the pin |
| 18, 19 | PVCC | `+12V` | C7 1 nF, C9 100 nF, C11 10 uF, C14 100 uF electrolytic |
| 20 | BSNL | `/BSNL` | C15 220 nF to `/OUTNL` |
| 21 | OUTNL | `/OUTNL` | L2 -> `/SPK_L_N` |
| 22 | GND | `GND` | |
| 23 | OUTPL | `/OUTPL` | L1 -> `/SPK_L_P` |
| 24 | BSPL | `/BSPL` | C16 220 nF to `/OUTPL` |
| 25 | GND | `GND` | |
| 26 | BSNR | `/BSNR` | C17 220 nF to `/OUTNR` |
| 27 | OUTNR | `/OUTNR` | L4 -> `/SPK_R_N` |
| 28 | GND | `GND` | |
| 29 | OUTPR | `/OUTPR` | L3 -> `/SPK_R_P` |
| 30 | BSPR | `/BSPR` | C18 220 nF to `/OUTPR` |
| 31, 32 | PVCC | `+12V` | C8 1 nF, C10 100 nF, C12 10 uF, C13 100 uF polymer |
| 33 | PowerPAD | `GND` | via array to B.Cu |

## Nets that leave a block (placement groups at P6, net classes at P5)

| net | from | to | class / note |
|---|---|---|---|
| `+12V` | J1.1 | C13, C14, C11, C12, C9, C10, C7, C8, U1 17/18/19/31/32, R2 | 4 A, >= 1.0 mm at 2 oz |
| `GND` | J1.2, J2.2, TP1 | everything; B.Cu pour + F.Cu pour | 4 A return, heat spreader |
| `/IN_L`, `/IN_R` | J2.3, J2.1 | C1, C3 | signal, keep >= 10 mm from L1-L4 |
| `/LINP`, `/RINP` | C1, C3 | U1 10, 4 | 60 kOhm high-Z nodes, short |
| `/LINN`, `/RINN` | C2, C4 | U1 11, 5 | high-Z, short |
| `/GVDD` | U1 7 | U1 6, C5 | local |
| `/GAIN` | U1 8 | R1 | local; sets gain and master mode, latched at start-up |
| `/SDZ` | U1 2, 3 | R2 | local |
| `/MUTE` | U1 12 | R3 | local |
| `/OUTPL`, `/OUTNL` | U1 23, 21 | L1, L2, C16, C15 | 3 A switch nodes, >= 0.8 mm, symmetric pair, tight |
| `/OUTPR`, `/OUTNR` | U1 29, 27 | L3, L4, C18, C17 | same |
| `/BSPL`, `/BSNL`, `/BSPR`, `/BSNR` | U1 24, 20, 30, 26 | C16, C15, C18, C17 | bootstrap, loop local to its pin pair |
| `/SPK_L_P`, `/SPK_L_N` | L1, L2 | C19, C20, R4, R5, J3.1, J3.2 | 3 A, >= 0.8 mm |
| `/SPK_R_P`, `/SPK_R_N` | L3, L4 | C21, C22, R6, R7, J4.1, J4.2 | 3 A |
| `/ZL_P`, `/ZL_N`, `/ZR_P`, `/ZR_N` | R4, R5, R6, R7 | C23, C24, C25, C26 | damping-branch midpoints, local |

## Refdes ranges (one sheet; fixed so a later renumber lands in the same places)

| class | range | assigned |
|---|---|---|
| U | U1-U9 | U1 TPA3118D2DAPR |
| L | L1-L9 | L1 OUTPL, L2 OUTNL, L3 OUTPR, L4 OUTNR - 10 uH 7.3 x 6.6 mm |
| R | R1-R19 | R1 5.6k gain; R2 100k SDZ pull-up; R3 100k MUTE pull-down; R4 SPK_L_P, R5 SPK_L_N, R6 SPK_R_P, R7 SPK_R_N damping 3.3R 0603 |
| C | C1-C39 | C1 LINP / C2 LINN / C3 RINP / C4 RINN 2.2 uF 0805; C5 1 uF GVDD 0603; C6 100 nF AVCC 0603; C7, C8 1 nF C0G 0603 (PVCC 18/19, 31/32); C9, C10 100 nF 0603; C11, C12 10 uF 0805; C13 100 uF polymer (31/32), C14 100 uF electrolytic 35 V (18/19); C15 BSNL, C16 BSPL, C17 BSNR, C18 BSPR 220 nF 0805; C19 SPK_L_P, C20 SPK_L_N, C21 SPK_R_P, C22 SPK_R_N 680 nF 0805; C23-C26 10 nF 0402 damping (same order) |
| J | J1-J9 | J1 power 2 pads; J2 line in 3 pads (R, GND, L); J3 left spk 2 pads; J4 right spk 2 pads - all SMD wire pads, no connector body |
| TP | TP1-TP9 | TP1 GND |
| `#PWR` | `pwr_base = 100` -> `#PWR0101...` | `+12V`, `GND` symbols |
| `#FLG` | `#FLG0101...` | one PWR_FLAG on `+12V`, one on `GND` |

## Values and ratings the schematic must carry

| ref | value | rating / dielectric | why |
|---|---|---|---|
| C1-C4 | 2.2 uF | X7R, 50 V (25 V min), 0805 | the reference design's value; 1.2 Hz corner at 60 k |
| C5 | 1 uF | X7R 25 V 0603 | GVDD LDO decoupling, datasheet-mandated |
| C6 | 100 nF | X7R 50 V 0603 | AVCC |
| C7, C8 | 1 nF | C0G/NP0 50 V 0603 | switching-edge loop |
| C9, C10 | 100 nF | X7R 50 V 0603 | mid-frequency |
| C11, C12 | 10 uF | X7R 25 V 0805 | P1 decision (Basic 0805, not 1206) |
| C13 | 100 uF | Al-polymer 25 V, ESR <= 30 mOhm, >= 2 A rms | ripple |
| C14 | 100 uF | Al-electrolytic 35 V low-ESR | ripple + damps hot-plug ring |
| C15-C18 | 220 nF | X7R 50 V 0805 | bootstrap, one per output |
| C19-C22 | 680 nF | X7R 50 V 0805 | LC filter, f0 61 kHz with 10 uH |
| C23-C26 | 10 nF | X7R 50 V 0402 | damping branch |
| L1-L4 | 10 uH | Isat >= 4 A (5.5 A lead), Irms >= 3 A, DCR <= 70 mOhm, 7.3 x 6.6 mm shielded | 3.5 A peak, 7.5 A OC trip |
| R1 | 5.6k | 1 %, 0603 | 20 dB / master; latched at power-up |
| R2, R3 | 100k | 1 %, 0603 | SDZ+FAULTZ pull-up, MUTE pull-down |
| R4-R7 | 3.3R | 1 %, 0603 (>= 100 mW) | damping |
