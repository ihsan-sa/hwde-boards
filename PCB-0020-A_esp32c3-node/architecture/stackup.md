# stackup - esp32c3-node (P2)

Chosen: `JLC2313_1.6` - JLCPCB standard 2-layer, 1.6 mm FR-4, 1 oz, HASL lead-free.

- Impedance: none controlled. USB full-speed (12 Mb/s, 4 ns edges) over < 30 mm of trace does
  not need 90 ohm; 2L 1.6 mm cannot reach it at routable widths. Route the pair coupled over
  unbroken GND.
- Planes: B.Cu full GND pour except the module antenna keep-out (no copper on ANY layer
  there) and under the BME280 island.
- Density: ~40 parts on a XIAO-class outline is the binding factor, not layer count; the module
  carries the RF. 2 layers is the fewest that honestly work.
- Current: < 0.7 A anywhere; 1 oz is ample.

## Board size: an output
Stated ~21 x 17.8 mm (XIAO) is SOFT. The module alone is 13.2 x 16.6 mm plus the antenna
keep-out at an edge, USB-C at the opposite edge, JST-PH 2 mm battery connector, Qwiic, two
buttons and two rows of 0.1 in edge pads. Expect the earned outline around 22-26 x 32-36 mm.
P5 opens with `board_init --outline auto`, P6 earns it, and the excess is recorded.
