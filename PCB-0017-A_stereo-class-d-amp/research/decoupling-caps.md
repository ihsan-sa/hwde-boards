# decoupling-caps — input coupling, bootstrap, PVCC/GVDD/AVCC decoupling

All values below have deep JLC Basic stock — none of this block needs an Extended part.

## Input coupling: 2.2 uF X7R, >=25V (the reference design's value, req/brief)
| rank | mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|
| 1 | CL21A225KBQNNNE | C377773 | 0805 | 682,011 | $0.053 | **Basic** | 2.2uF X7R 50V, best fit |
| 2 | CL31B225KBHNNNE | C50254 | 1206 | 414,087 | $0.0856 | **Basic** | same value, larger 1206 if 0805 X7R DC-bias derating is a concern |

## GVDD decoupling (1 uF) and bootstrap (four x 0.22 uF / 220 nF)
Relabeled per refdesign-amp's datasheet read: the 1uF is GVDD's own decoupling cap (its internal
LDO, one per IC), not a bootstrap value; the four bootstrap caps (one per half-bridge FET) are
0.22uF/220nF each.

| rank | mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|
| 1 | CL10A105KB8NNNC | C15849 | 0603 | 6,785,078 | $0.0752 | **Basic** | GVDD decoupling, 1uF X7R 50V, smallest Basic footprint at value |
| 2 | CL21B105KBFNNNE | C28323 | 0805 | 2,497,202 | $0.0397 | **Basic** | GVDD alt, 0805, cheaper |
| 3 | CL21B224KBFNNNE | C5378 | 0805 | 671,741 | $0.0187 | **Basic** | bootstrap, 0.22uF/220nF X7R 50V, x4 per board (one per half-bridge FET) |

## Per-PVCC-pair decoupling: 1 nF C0G + 100 nF X7R 50V + 10 uF (25V, orchestrator specified 1206)
| rank | mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|
| 1 | CL10B102KB8NNNC | C1588 | 0603 | 8,224,224 | $0.0089 | **Basic** | 1nF C0G, best stock |
| 2 | CC0603KRX7R9BB104 | C14663 | 0603 | 51,362,410 | $0.0122 | **Basic** | 100nF X7R 50V, huge stock |
| 3 | CL05B104KB54PNC | C307331 | 0402 | 14,254,822 | $0.0089 | **Basic** | 100nF alt, smaller 0402 if board area is tight |
| 4 | CGA1206X7R106K250NT | C6119987 | 1206 | 37,711 | $0.1576 | Extended | 10uF X7R 25V in 1206 as specified — no Basic 1206 hit at this value |
| 5 | CL21A106KAYNNNE | C15850 | 0805 | 5,536,330 | $0.0788 | **Basic** | 10uF X7R 25V, same electrical spec, smaller 0805, **Basic** — flagging as the cheaper/Basic alternate to the specified 1206 footprint |

## Risks / open note
- The 10uF/25V value has no JLC Basic listing in 1206 specifically (checked, empty); #5 (0805,
  Basic) meets the same voltage/capacitance and is both smaller and Basic-priced — if 1206 was
  chosen for a specific reason (higher self-resonant frequency headroom, footprint matching an
  existing library part, etc.) that reason should be confirmed, otherwise #5 is the better default.
- 1nF/100nF/2.2uF/1uF/0.22uF all have ample Basic stock with no single-source risk.
