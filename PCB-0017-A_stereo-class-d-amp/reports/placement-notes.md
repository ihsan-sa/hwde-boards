# PCB-0017-A stereo-class-d-amp - P6 placement notes (2026-09-27)

**Chosen: a hand-built canonical placement (anneal/manual3-5.ops.json), not the seed or an anneal candidate.**
The seed (anneal/seed.ops.json, HPWL 2187 -> 856 mm) was legal but spread over the 74x97 provisional outline;
the annealer cannot shrink an outline, so the compact layout was written as absolute ops around the datasheet rules.

Layout (all top side, U1 rot 270: pins 1-16 face left/J2, pins 17-32 face right):
- J2 line-in on the left edge, R/GND/L top to bottom; C3/C4/C1/C2 input caps and R2/C5/R1/R3 between J2 and U1's pin 1-16 side.
- PVCC 31/32 (top right): C8 1nF, C10 100nF, C12 10uF in a stack right at the pins, C13 100uF above them, D1 and J1 (+12V left pad, GND right pad) at the top edge.
- PVCC 18/19 (bottom right): C7, C9, C11, C6 (AVCC) stack, C14 100uF below.
- Bootstrap C18/C17/C16/C15 vertical in two staggered columns beside their BS/OUT pin pairs.
- L3/L4 (right ch, top row) and L1/L2 (left ch, bottom row) as a 2x2 grid right of U1, OUT pads facing U1; a 4.6 mm channel between rows carries OUTNR/OUTNL to the second column and holds R7/C26/C22/C20.
- Right-channel 680nF + Zobel (C21, R6, C25) above the grid; left-channel (C19, R4, C23, R5, C24) below it. J4 (upper) and J3 (lower) on the right edge, pads long-axis horizontal.
- TP1 bottom-left. Nothing sits under U1; the 25x25 thermal square holds only U1, its decouplers and the input parts.

Gate: place PASS (0 violations) after 5 edit iterations (manual1..5). silk_place --apply moved 44 refdes, 0 residuals; gate still passes.
Outline: board_edit --outline fit --margin 0.8 -> bbox [9.1, 8.3, 62.65, 45.1] = 53.6 x 36.8 mm (vs 44 x 34 reference).

Why larger than 44 x 34: (1) the inductor footprint's pads (2.5 x 3.1 at +/-3.08) reach +/-4.34 mm, outside its 6.7 x 6.6 courtyard, so the 2x2 grid needs a 9.6 mm column pitch; (2) the gate's courtyard model is pads + ~0.5 mm, so every stack needs 0.5-0.6 mm gaps; (3) J3/J4 (7.2 x 6.8 wire pads) sit outside the second inductor column instead of overlapping it vertically; (4) the bulk caps are 8.8 mm wide pad-to-pad. Recovering ~8 mm width means stacking J3/J4 between the inductor rows and the board corners, or swapping the 7.3 mm inductors for a 6 mm part.

Not done in the 28 min cap: route_auto --probe (routability), full kicad-cli DRC after silk, "PCB-0017 REV A" and "+12V/GND" silk texts. Room for them: the REV text fits along the bottom edge between TP1 and C14 (x 19-31, y 43.5); "+12V/GND" fits above J1's pads at y 9.2 (x 44-51).
Open items: IND-SMD_L7.3-W6.6_MHCI06030 courtyard smaller than its pads (footprint fix in lib); bootstrap-cap OUT traces must leave the cap pads sideways (see anneal/manual3.ops.json layout); SPK_L_P route to J3's lower pad goes under J3's upper pad, so route it at y ~43 from x 46.
Backups: kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb.p5bak (board_init state), anneal/pass-before-silk.kicad_pcb.
