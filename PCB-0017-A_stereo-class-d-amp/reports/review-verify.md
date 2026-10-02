# PCB-0017-A stereo-class-d-amp - P8 verify review (fresh-context reviewer, 2026-09-27)

## Verdict: SHIP-WITH-WAIVERS

All four proposed waivers are technically sound: none hides a defect that must be fixed
before this fab package is called done. The thermal waiver's 30 C/W figure is optimistic
(I estimate 35-40 C/W for this board as drawn, because the exposed-pad path into B.Cu is
nine 0.3 mm holes landing on thermal-relief spokes), but the 1.5 W design point still
lands at Tj ~95-100 C at Ta 40 C, inside the 125 C bound the constraints set. The two
+12V pin links and the four OUT pad-entry stubs are pitch-bound necks between wide
copper, exactly as the waiver says; the pour_neckdown is a tool artefact on a fill that
is split on F.Cu but stitched to a single-piece B.Cu pour (I confirmed B.Cu is one
polygon, 1859 mm2). Two should-fixes are cheap and belong in the next revision (or now
if the designers want them before COMPARISON.md is final): solid pad connection on the
B.Cu zone plus a denser EP via array, and +/- and L/R silk marks at the speaker and
line-in wire pads. No blocker.

Machine state I re-ran: `gate.py --gate verify` -> fail, 8 errors / 23 warnings, the
same eight items as the proposal. `reports/checks/summary.json` does not exist, so
verify_all's SKIPPED list is not visible to me (hole, see OPEN). My own 2400 px renders
timed out in kicad-cli (600 s) and were not produced; findings below use the existing
`reports/PCB-0017-A_stereo-class-d-amp_top.png` / `_bottom.png` and direct pcbnew inspection.

## Findings, worst first

### Blockers
None.

### Should-fix

1. **B.Cu GND zone uses thermal-relief pad connection, so U1's nine thermal vias meet the
   heat spreader through 0.5 mm spokes** (zone at line ~10192 of the .kicad_pcb:
   `connect_pads` default = thermal, `thermal_gap 0.5`, `thermal_bridge_width 0.5`; the F.Cu
   zone is `connect_pads yes`). Nothing is soldered on B.Cu, so reliefs buy nothing there
   and cost copper on every GND via, including the 5 J1 GND return vias carrying 4 A.
   Thermally it is only ~1 C/W (spokes in parallel are small next to the ~18 C/W of nine
   0.3 mm barrels), but it is the wrong default for a plane whose stated job is heat
   spreading. Fix: `connect_pads yes` on the B.Cu zone. Domain: plane. Location: whole
   B.Cu zone; visible in the bottom render as spoked rings on every via.

2. **EP thermal via array is sparse: 9 x 0.3 mm drill (3 x 3 at 1.0 mm pitch) on a
   3.81 x 3.71 mm pad, and no board-level vias inside the pad** (footprint pads "33",
   thru_hole 0.61/0.3, at x 25-27, y 26-28). Barrel conduction ~160 C/W each, ~18 C/W
   for nine, in series with the B.Cu pour: that is the single largest term in the heat
   path and why I put theta_JA at 35-40 C/W rather than the waiver's 30 C/W. TI's 22 C/W
   EVM figure was reached with a denser array. A 4 x 4 at 0.9 mm pitch (16 vias, ~10 C/W)
   fits the pad and JLC's 0.3 mm drill. At the 1.5 W design point the board passes either
   way; at 4-ohm full-power sine (3.0-4.2 W, out of scope by decision P1) the sparse
   array sends it into thermal shutdown sooner. Domain: library (footprint). Location:
   U1 EP, (26.0, 27.0).

3. **Wire pads J2/J3/J4 carry no polarity or channel marks on silk.** Only J1 has "+12V"
   and "GND" text; J3/J4 (SPK L/R +/-) and J2 (IN R/GND/L) show just their refdes. The
   outputs are BTL: a user who assumes "-" is ground and ties it to the supply return
   shorts one half-bridge to GND on every power-up (U1's OC latch should catch it, but it
   is a field failure mode the silk could prevent). Board footprint value strings hold the
   text already ("SPK L +/-", "LINE IN R/GND/L"). Domain: silk. Location: J2 (12, 26),
   J3 (58.5, 40.2), J4 (58.5, 16.0). Evidence: top render, silk text list (3 strings only:
   "PCB-0017 REV A", "+12V", "GND").

4. **Two bootstrap capacitors sit 9 mm from their pins.** C16 (BSPL/OUTPL) at (38.4, 31.6)
   is 9.4 mm from U1 pin 24; C17 (BSNR/OUTNR) at (38.4, 27.7) is 8.8 mm from pin 26. C15
   and C18 are at 3.1 and 4.1 mm. The datasheet asks for the BS caps close to the pins;
   a long bootstrap loop adds ringing at the switch node and asymmetry between the two
   halves of each bridge. Not a field failure at 12 V, but it is the one EMI-relevant
   placement the checks do not see. Domain: placement. Location: C16, C17.

### Notes

5. Switch-node runs are long and unequal per bridge: OUTPL ~11 mm to L1, OUTNL ~20 mm to
   L2, OUTPR ~10 mm to L3, OUTNR ~19 mm to L4 (all F.Cu, 0.624 mm). Fine for function at
   400 kHz; a radiated-EMI test would prefer the inductors closer to U1's right pin row.
   Domain: placement.
6. No fiducials. JLC PCBA accepts boards without them for a 53 x 37 mm single-sided
   assembly; add two if a later revision goes to another assembler. Domain: fab.
7. No reverse-polarity protection; D1 (SMBJ15A) will conduct as a forward diode on a
   reversed 12 V and the adapter or D1 fails. This is the recorded Q7 default, not drift.
8. Board is 53.65 x 36.9 mm outline vs the reference design's 44 x 34; COMPARISON.md records the +32 %
   and why. Not drift.
9. Silk "PCB-0017 REV A" is present (18, 12). Electrolytic polarity marks on C13/C14 are
   visible after assembly (render). TP1 is GND as the requirements assumed.
10. Warnings triage (23): 6 check_current warnings are the 0.882/0.624 mm traces read
    against the tool's rounding, 7 check_decoupling are the 100 uF bulk and BS caps beyond
    the tool's distance (bulk at 8.7/9.1 mm is fine; the two BS caps are item 4), 7
    check_silk are refdes-under-body on the 0402/0603 parts (cosmetic for PCBA), 2
    check_thermal and 1 verify_all are the modelling notes already covered. None escalates.

## The four proposed waivers

1. **thermal_area on U1 - SOUND, with items 1-2 as the honest caveat.** The check's 2-layer
   model floors at 73.8 C/W and cannot express a via-coupled bottom spreader; that part of
   the argument is right. My own estimate of the board as drawn: die-to-pad ~2 C/W, nine
   0.3 mm barrels ~18 C/W, relief spokes ~1 C/W, one-piece 2 oz B.Cu pour of 1859 mm2
   convecting with the F.Cu side ~25-30 C/W, in parallel with a fragmented F.Cu GND path
   (~50-60 C/W): ~35-40 C/W total. At 1.5 W that is a 53-60 C rise, Tj ~95-100 C at Ta
   40 C, under the 125 C bound. Waive; do not lower the rule; take items 1-2 next time.
2. **+12V 0.343 mm links - SOUND.** Pin 19 is fed only by the 0.343 x 0.65 mm link from
   pin 18 (which has the 0.882 mm feed from pin 17); pin 31 only by the link from pin 32
   (two 0.882 mm feeds). Pins 18/19 and 31/32 are the same PVCC node inside the package,
   so a link carries at most one pin's share (< 1 A rms) over 0.65 mm between copper that
   is 0.882 mm and a 0.343 mm pad of the same width. IPC-2152 steady-state width does not
   apply to a sub-millimetre neck. Nothing hidden.
3. **OUT 0.300 mm pad-entry stubs - SOUND.** 0.30 x 1.18 mm from a 0.343 mm pad to a
   0.624 mm trace, one per output; same argument. Note that 0.624 mm for 3 A / dT 20 is
   the 2 oz number: the stackup (`JLC2313_1.6_2oz`) and constraints say 2 oz; the fab
   order must too (see OPEN).
4. **pour_neckdown GND F.Cu at C20 - SOUND (tool artefact).** F.Cu GND fills as 3
   polygons (1161 / 122 / 26 mm2), split by the OUT rows; B.Cu GND is a single polygon
   (1859 mm2) and holds the C20 pad point, the J1 GND pad point and the U1 region. The
   eroded-width test reads 0 because it asks the F.Cu fill alone to be one piece. The
   real 4 A return runs on B.Cu from J1's five GND vias (49.8, 10.1-14.9) to U1's EP
   holes and the F.Cu GND pins; adequate. Item 1 improves every one of those via joints.

## The specific questions

(2) U1 heat path: credible for the stated design point (1.5 W, 8 ohm, 13.2 V, 10 % THD);
    the weak link is the 9-hole array plus relief spokes, not the pour. Not credible for
    sustained 4-ohm full power, which the record already excludes.
(3) LC filters / BTL / GND return: 10 uH + 680 nF gives fc ~61 kHz, Zobel 3.3 R + 10 nF
    on each leg; damping-cap returns reach GND vias within a few mm except C21 (nearest
    GND via ~7 mm, but the F.Cu main polygon reaches it). Nothing that fails in the field.
    Items 3-5 are the risks worth naming: unlabelled BTL pads, long BS loops, long
    switch-node runs.
(4) Vias under L1: they are not GND vias. Six are /SPK_L_P (the F.Cu->B.Cu layer
    transition, 0.6/0.3 mm, at x 39.6-41.3, y 36.9-37.75) plus one GND via at (41.0, 34.6).
    All vias on the board are tented both sides (board default `tenting front yes back
    yes`), they sit 2.2-3.1 mm from L1's pads, DRC is clean, and six 0.3 mm barrels meet
    the >= 6 per layer change rule for 3 A. The MHCI06030 body is metal-composite and
    not guaranteed insulating, so the tenting is what makes this safe; keep it, and do
    not switch JLC's option to "untented". Assembly risk: low. Short risk: low.

## OPEN
- `reports/checks/summary.json` absent: I could not see which verify_all checks were
  SKIPPED for missing inputs. Whoever lands this should run verify_all and confirm.
- Confirm the fab order / quote is 2 oz outer copper (fab/quote.json shows no copper
  weight field I could find; fab_export.json lists only layer names). The 0.624 / 0.882 mm
  widths and the thermal case both assume 2 oz.
- My high-res/iso renders did not complete (kicad-cli render timeout); iso view unchecked.
