# PCB-0017-A stereo-class-d-amp - stackup (P2)

## Choice

**`JLC2313_1.6_2oz`** - JLCPCB 2-layer, 1.6 mm, 2 oz outer copper, HASL.
`available: true` in `reference/stackups.yaml` (vendor_page provenance, verified
2026-08-06; core thickness derived 1.6 - 2 x 0.070). Fab class: **2L**, 2 oz
copper option, no controlled impedance (JLC sells no impedance-controlled 2-layer
product, and nothing here would use one). Design-rule class `2layer_2oz` in
`jlc_capabilities.yaml`: 0.1524 mm trace/space floor, 0.3 mm drill / 0.6 mm via.

```
F.Cu        0.070 mm  2 oz   - all parts (JLC PCBA top side), all routing,
                               GND pour joining the PowerPAD, GND pins and returns
dielectric  1.460 mm  FR4 core, er 4.5 (assumed)
B.Cu        0.070 mm  2 oz   - unbroken GND pour: current return and heat spreader;
                               no parts; the only tracks allowed are outside the
                               thermal square around U1
```

## Why 2 layers

The brief fixes 2 layers and the design honestly needs no more. There is no
controlled impedance (the fastest thing on the board is a 400 kHz PWM with
~10-20 ns edges; every trace is a lumped wire), no digital aggressor, and one
rail. What the board needs from its copper is (a) a continuous low-impedance
ground that is also the heat spreader for a pad-down HTSSOP, and (b) wide,
short paths for 4 A in and 3 A out. A single unbroken B.Cu GND pour delivers
(a); 2 oz copper and local pours deliver (b). A 4-layer stack would put a ground
0.24 mm under the switch nodes (tighter loops, less EMI), but EMI is not a
stated requirement, it costs a fab class, and it breaks the like-for-like
comparison with the reference design's 2-layer board. Rejected.

## Why 2 oz (P1 decision "Prefer 2 oz outer copper if the stackup table offers it")

- Widths: 4 A at dT 20 C needs 0.88 mm at 2 oz vs 1.76 mm at 1 oz; 3 A needs
  0.62 vs 1.25 mm. On a board whose output side is four 7.3 x 6.6 mm inductors
  wide, the 1 oz widths would push the outline out.
- Spreading: 2 oz halves the sheet resistance of the GND heat spreader (~37 vs
  ~74 K/W per square), worth about 5 C/W off RthJA here (power.md section 4,
  EST) - it is what turns 4 ohm music into a comfortable case and 8 ohm full
  power into a cool one.
- Cost: a 2 oz adder on a small 2L order (unquoted in the pricing table; P10's
  `order_quote` would show it) against nothing else - the board has no
  fine-pitch part that 2 oz's 0.1524 mm floor would trouble (HTSSOP 0.65 mm
  pitch leaves 0.35 mm between 0.30 mm pads).

`JLC2313_1.6` (1 oz) is the fallback if 2 oz is ever refused: then the +12V trunk
is 1.8 mm wide, outputs 1.3 mm, and the thermal margin at 1.5 W shrinks from
about 40 C to about 30 C (power.md table: ~35 C/W EST at 44 x 34 mm 1 oz) - still
a pass at the design point.

## What the layout needs from this stackup (geometry is P6's output)

- **B.Cu**: one GND zone over the whole board; within a >= 25 x 25 mm square
  centred on U1 it is uncut by any track (that square is the 645 mm2 the thermal
  screen saturates at, and where the heat actually spreads - reach ~14 mm). The
  +12V trunk between the two PVCC pairs, if it goes to the bottom, runs outside
  that square along the board edge.
- **F.Cu**: a GND zone too (`planes` entry, solid pad connection so the PowerPAD
  and pins 9/22/25/28 have no thermal relief), merging the PowerPAD land, the
  GND pins, the decoupling and filter-cap returns and TP1. Solid connect also
  applies to the small GND pads on this zone; accepted at 0402/0603 for the
  thermal benefit.
- **Vias**: >= 15 GND vias within ~6.5 mm of U1's centroid, 0.3 mm drill / 0.6
  mm pad at ~1.1 mm pitch - the exposed pad is only 3.04 x 3.74 mm max (DAP
  drawing), so P3's footprint extends the mask-covered thermal land per TI
  SLMA002 (a ~6 x 8 mm land is typical) and the rest of the count comes from
  stitching vias at the four GND pins and around the body. Tent from the top
  (component) side or leave open; never thermal-relief them.
- **Widths**: +12V >= 1.0 mm, outputs >= 0.8 mm, >= 8 vias per +12V layer
  change, >= 6 per output (power_tree.md section 7).
