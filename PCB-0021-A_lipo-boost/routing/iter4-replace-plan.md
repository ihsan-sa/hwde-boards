# iter 4 routing plan (stopped at context bound, nothing applied)

State on disk: board has 281 freerouted signal tracks from a route_auto run at 08:08 (power nets
unrouted, 48 violations). The brief said zero tracks; it was stale. No edits made by iter 4.

Why the current placement can't route cleanly: U2's VOUT faces left (away from J4) and U1 rot 0
puts VBUS on top, so +5V must cross SYS and VBUS must cross TMR/ISET. Re-place the boost stage to the
right of U1 (VIN faces U1, VOUT faces J4) and rotate U1 to 90 (VBUS left to J1, SYS up/right, VBAT down
to C3/J2). That makes all power nets planar on F.Cu except one unavoidable VBUS/VBAT crossing.

Next steps:
1. `state.py restore --label pre-route`, then `place_edit.py --ops kicad/fix11.ops.json`, then
   `gate.py --gate place`. Nudge any courtyard overlaps; R9/R11 and L1/R6 have about 0.05 mm margin.
2. Draw the power copper as F.Cu zones with `connect: solid` (polygons through lib/route_swig.py
   add_zones), plus tracks at the floor width where there's room:
   - SW: U2.5 (exits right) down x 51.95-52.8 to L1.2.
   - +5V: zone x 50.35-57.4, y 41.4-43.65 (U2.6, R10.1, C11/12/13), then 0.8 mm track
     (57.8,35.6)-(57.8,49.0)-(59.46,50.66)-J4.1, with a stub up to J3.4.
   - SYS: zone covering U1 pins 10/11, C2.1, R9.1, C10.1, C14.1, L1.1, U2.3 and R5/R6/R8 pad1; a strip
     up x 44.2-45.4 to y 38.8; a 1.24 mm track along y 38.8 from R7.1 to x 54, then up to J3.3. U1 pin 5
     (EN2) joins it through a strip going right at y 52.
   - VBAT: lobe from U1 pins 2/3 to C3.1, a 1.1 mm track down-left to J2.1, and a branch up x 33.5 to
     U3.3, then y 37.0 to x 51.4 and up to J3.2.
   - VBUS: J1 pad1 lobe through the gap between pads 8 and 9 (y 50.42-51.15), a 0.8 mm track at y 50.0,
     and a B.Cu jumper under the VBAT branch: 3 vias at x 30.55/31.35/32.15 and 3 at x 35.0
     (y 49.2/50.0/50.8), joined by a priority B.Cu VBUS zone. Then the F.Cu VBUS lobe to C4.1, C1.1 and
     U1.13.
   - GND: pins 4/6/8 reach the EP through a small F.Cu GND zone (corridors about 0.3 mm, min_width 0.2).
     4 EP thermal vias (5 don't fit a 1.8 mm pad at 0.5 mm hole-to-hole). Vias at C10.2/C14.2
     (51.45,47.55) and (50.4,49.1).
3. Run `route_auto --exclude-classes Pwr_0p68mm,Pwr_0p8mm,Pwr_1p1mm,Pwr_1p24mm,Pwr_1p4569mm` for the
   signals. CHG, PGOOD, EN and LBO will need B.Cu hops.
4. Add a full F.Cu GND zone at the lowest priority (solid) on top of the B.Cu GND pour. Then
   stitch_vias, refill, and `gate.py --gate drc_routed --workspace`.
