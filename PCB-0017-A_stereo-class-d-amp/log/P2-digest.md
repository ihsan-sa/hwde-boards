# P2 digest
- Architect (fable/high): 4 blocks - B1 12 V/4 A wire-pad input + 100 uF polymer & 100 uF electrolytic bulk; B2 stereo line-in, 2.2 uF X7R coupling; B3 TPA3118D2DAPR BTL, BD, 400 kHz, 20 dB, master; B4 10 uH + 680 nF LC per leg, 3.3R+10nF damping.
- One schematic sheet, no hierarchy (38 fitted parts); canonical net names in sheets.md, used by constraints.json.
- Stackup: 2 layers, 2 oz outer preferred; B.Cu one GND pour with the PowerPAD thermal-via array into it.
- Size driver: four 7.3x6.6 mm inductors; target <= 44x34 mm, placement earns the outline (provisional, then fit).
- constraints_lint exit 0 (11 unitless operating-point warnings, informational).
- Coverage P2: 4/4 slots gap (no checklists for these topologies) -> 4 research tasks opened automatically.
