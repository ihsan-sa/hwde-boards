# P7 digest - routing (2026-10-01)
- Fully routed, 2 layers, GND pours F.Cu + B.Cu with stitching vias. DRC 0 errors, 0 unconnected, 0 warnings; gate drc_routed PASS.
- Silk: outline graphics removed/clipped on R0603, C0603, SW-SMD, U1 and J1, both on the board and in lib/aiee.pretty (pads, courtyard, fab and U1 antenna keep-out unchanged). C11 refdes on B.SilkS.
## Owner-visible waivers
- USB D+/D- skew 5.95 mm (~42 ps) vs 5.0 mm limit, and via count 4 vs 3. Full-speed USB (12 Mb/s) tolerates it; not rerouted.
- USB pair routed as a 140-ohm uncoupled pair (Diff140 class), not a coupled pair.
- 10 sub-track-width jogs remain (style warnings, not DRC).
- C11.2 / C12.2 GND pads solid-connected to the pour (thermal spokes were starved).
