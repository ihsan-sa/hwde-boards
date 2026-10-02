# PCB-0017-A stereo-class-d-amp - P7 routing notes (router subagent, 2026-09-27 08:37-09:02Z)

Hard time cap 25 min. Snapshots before every mutating step in routing/pre-<step>.kicad_pcb.

## Chain run
1. planes_gen: PASS. Two GND pours added (B.Cu 1878 mm2, F.Cu 1558 mm2, both one island),
   9 thermal vias at C14/D1/J1 GND pads. U1's EP vias were already present.
   Constraint fix needed first: `planes[].{_why}` is rejected by the validator; the two notes
   were moved to a top-level `_planes_why` key (pre-edit copy: routing/constraints.pre-router.json).
2. route_critical --pad-window: PASS, every +12V pad ceiling >= 0.882 mm (widest 5.4-8.0 mm).
   route_critical (power, KRT) was NOT run to completion: the first KRT invocation exceeded a 60 s
   cap and the default is 600 s per net, which did not fit the window. Skipped by decision; the
   netclasses (Pwr_0p624mm / Pwr_0p882mm) carry the IPC widths so Freerouting honours them.
3. route_auto: two aborted starts before a live run -
   a) DISPLAY=:99 had no Xvfb (only :163/:187 exist) -> export_dsn failed; used :163.
   b) Freerouting's bundled JRE could not load libXtst.so.6 -> both rungs died at JVM start.
      Fix: LD_LIBRARY_PATH=$HOME/.local/kicad10/usr/lib/x86_64-linux-gnu (KiCad bundle ships it).
      hwde-env.sh should export this itself (tooling finding, not a board issue).
   Live run: --max-rungs 2 --timeout-s 150 --no-krt-finish. Result: see below.

## Knowledge records applied
- class-d-amp-2layer-pour-heat-spreader: B.Cu GND pour is the heat spreader; kept as one island.
- audio-line-in-2layer-switch-node-keepaway: no shield layer on 2L, so line-in and OUT nets are
  separated by placement (J2 left, filters right); routing must not cross them on B.Cu under U1.
- lc-output-filter-placement-and-loop / class-d-amp-pvcc-three-tier-decoupling: decoupler returns
  go straight to the pour (F.Cu GND pour connect solid per constraints.planes).

## Result (08:52Z, stopped at the time cap)
- Board = planes_gen state + nothing else. Freerouting never produced a SES: both rungs
  (150 s each) were killed by the per-rung timeout while still iterating. Its log shows it was
  close: pass 1 = 6 unrouted (81 s), passes 2-4 = 5 unrouted (~20 s each, score flat at 976.18),
  i.e. 5 nets it cannot finish with this placement - likely a placement_adjust candidate, but
  route_auto never reached the point of emitting that request.
- Copper: 0 tracks, 0 signal vias; GND pours F/B (one island each) + EP thermal vias + 9 pad vias.
- Gate drc_routed: FAIL, 56 unconnected (was 90 before pours), 0 other DRC errors/warnings.
  Report: reports/gate-drc_routed.json. Not recorded in state.json (a failing gate).
- check_thermal: not run (no routing to screen yet).
- Nothing hand-fixed. No placement change requested yet.

## Exact next step (P7 continues)
Same shell env plus:
  export DISPLAY=:163   (or start Xvfb :99 first; it was not running)
  export LD_LIBRARY_PATH=$HOME/.local/kicad10/usr/lib/x86_64-linux-gnu
1. Optional but wanted for the +12V trunk / OUT widths: route_critical.py --pcb kicad/... (default
   600 s KRT timeout; budget ~10-15 min). Skipped here for time.
2. route_auto.py --pcb kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb --work-dir route --out-report
   routing/route_auto.json with --timeout-s >= 600 (Freerouting needs to finish a run to write the
   SES; 150 s was not enough). Read facts.completion; if it carries placement_adjust_request for
   the ~5 stubborn nets, return it to the orchestrator (P7->P6 backward edge).
3. stitch_vias -> plane_repair (snapshot first) -> route_cleanup --dry-run then live -> gate.
4. check_thermal.py --pcb ... --constraints kicad/constraints.json, then state.py record-gate.
Tooling findings to feed back to hwde: hwde-env.sh should export the KiCad lib dir for the JRE
(libXtst.so.6) and either start or verify the Xvfb display it expects; planes_gen's validator
should accept `_`-prefixed annotation keys inside planes[] like the rest of constraints.json does.

# P7 routing, second router (2026-09-27 09:03-09:20Z, hard stop 09:36Z)

Start: route_auto2 result = 170 tracks, 16 DRC (8 track_width, 3 edge clearance, 5 unconnected).
Snapshots: routing/pre-route_edit_fix.kicad_pcb, pre-refill, pre-rulearea; end state copied to
routing/post-router2.kicad_pcb.

## Steps
1. route_edit (routing/route_edit_fix.json, 22 ops, report route_edit_fix.report.json):
   - +12V left-edge run moved from x=9.806 to x=9.9 (3 tracks re-added, 0.882 mm) -> edge clearance
     0.36 mm, fixes the 3 copper_edge_clearance errors.
   - +12V (31.5,34.6)-(29.9,35.109) three 0.80 mm segments re-added at 0.882 mm.
   - Removed Freerouting's /OUTPR route: it went through a via at (27.886,24.018) UNDER U1's body
     to B.Cu, ran diagonally under the heat-spreader pour to (34.96,16.875) and detoured to L3 from
     above. Wrong per the class-d heat-spreader and outputs-on-TOP records, and 0.343 mm wide.
2. Zones refilled (kicad-cli pcb drc --refill-zones --save-board); the stale fill was hugging the
   old thin tracks and gave 4 clearance errors against the GND pour after step 1.
3. Rule exception, pad-entry neck-down at U1 (0.65 mm pitch, 0.343 mm pads; a 0.882/0.624 mm
   track physically cannot enter these pads - max is 0.345 mm for 0.1524 mm clearance):
   - Rule area "U1_neck" on F.Cu, x 28.6-30.95, y 21.6-32.4 (U1's right pad column + 0.35 mm),
     no keepouts (pure named area). Added with the bundled pcbnew python (route_edit has no op for it).
   - kicad_dru: rule "aiee_neck_fine_pitch_U1", track_width min 0.1524 mm, condition
     A.Type=='track' && A.intersectsArea('U1_neck'), appended LAST so it wins inside the area.
     A.intersectsCourtyard('U1') and A.insideCourtyard('U1') did NOT match in KiCad 10 here
     (courtyard shapes exist) - tooling note. rules_gen.py would overwrite this rule; pre-edit
     copy at routing/pre-neck-rule.kicad_dru. The two remaining 0.343 mm tracks are pin-to-pin
     bridges between adjacent +12V pads (17-18-19, 31-32) inside the pad column.
4. plane_repair --flag-only: PASS, no split planes (B.Cu pour still one piece).
   route_cleanup --dry-run: 0 ops, so no live run. stitch_vias NOT run: routing is unfinished and
   stitch vias would land in the region the OUT re-route needs.
5. gate drc_routed: FAIL 6/6 - 0 DRC errors, 6 unconnected (4 OUT nets). reports/gate-drc_routed.json.
   Not recorded (failing).
6. check_thermal -> reports/check_thermal.json: 1 error + 1 warning on U1 (1.5 W, "0 thermal vias",
   ~111 C rise). It counts board vias only; U1's 9 thermal vias are footprint pads with drills
   (pad 33, 0.61 mm) so it sees none. Tooling finding; the 645 mm2 copper figure is also suspect
   given the 1878 mm2 B.Cu pour. Re-run after the OUT routing is done before acting on it.

## Why the four OUT nets are still open (needs a placement change, P7 -> P6)
U1 right column pins, top to bottom: 30 BSPR 23.42, 29 OUTPR 24.07, 28 GND, 27 OUTNR 25.37,
26 BSNR 26.02, 25 GND, 24 BSPL 27.33, 23 OUTPL 27.98, 22 GND, 21 OUTNL 29.28, 20 BSNL 29.93.
Bootstrap caps today: near column x=32.2 (C18: BSPR 23.4 / OUTPR 25.4; C16: BSPL 27.6 / OUTPL 29.6),
far column x=34.2-34.4 (C17: OUTNR 25.5 / BSNR 27.5; C15: OUTNL 29.5 / BSNL 31.5).
- C18's OUTPR pad (y 24.7-26.1) sits exactly in the path of OUTNR (pin y 25.37) to C17; C16's
  OUTPL pad (y 28.9-30.3) sits in the path of OUTNL (29.28) to C15. Both blocked on F.Cu.
- The gap between the columns is 0.65 mm; a 0.624 mm OUT track needs 0.93 mm, so OUTPR cannot
  climb from C18 to L3 between the caps either - that is why Freerouting dived under U1.
- Space between the PVCC pin groups is 7.6 mm for four 3.4 mm-tall caps in two columns plus
  eight tracks; a re-place of C15-C18 is required, not a nudge. Worked (right channel only):
  C18 -> (32.8,23.4) rot -90 (clears the +12V run at x=31.5/y=21.7), C17 -> far column ~(38.4,26.55)
  rot 90, OUTNR row y=25.55, BSNR row y=26.15, BSPL 27.15. The left channel does not close in the
  same scheme: OUTPL must drop to L1 (y 33.6) past the OUTNL/BSNL rows whichever column C16/C15
  take. Candidate: move L1 up/left or put C15/C16 above/below the pin band and re-run
  place gate + route_auto with C15-C18 fixed; or route OUTPL/OUTNL as F.Cu polygons.

## Files changed by this router
kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb (tracks, rule area, zone refill), kicad/PCB-0017-A_stereo-class-d-amp.kicad_dru
(neck rule), routing/route_edit_fix.json + .report.json, routing/pre-*.kicad_pcb, routing/pre-neck-rule.kicad_dru,
routing/post-router2.kicad_pcb, routing/plane_repair_flag.json, routing/route_cleanup_dry.json,
reports/gate-drc_routed.json, reports/check_thermal.json, this file. Nothing committed, nothing ordered.

## 09:22-09:25Z: P7->P6 attempt, stopped before touching the board (coordinator cap 09:44Z)
Region survey (x 30.5-48.5, y 19.5-37) shows the re-place is bigger than a cap nudge:
- C8 (32.2,21.7) bbox y 21.25-22.15 and C7 (32.2,33.1) bbox y 32.65-33.55 bracket the near column:
  usable y for caps at x~32.8 is 22.3-32.5.
- L3 body bbox reaches y 25.86 and L1 body bbox starts at y 30.15, both from x 35.9 (pads only at
  y 20.8-24.0 / 32.0-35.2). So right of x=35.9 there are only 4.3 mm of free height (25.9-30.1)
  for the far-column caps; two 3.35 mm-tall caps do not stack there, and the rows for the inner
  pairs (OUTNR 26.14, BSNR 26.70, BSPL 27.06, OUTPL 27.62 - derived from C8's edge downward) leave
  no cap-sized gap either.
- Existing BS tracks to remove when re-routing: /BSPR 39c81251, 911ab399, 9227e97e; /BSNR 2d981dc7,
  49ccdffe, 98385004, ac5aa048, ae3ec111, e5955bab; /BSPL 1d8b337c, c05d49bd, c6908c3d;
  /BSNL 023ccccb, 08417efb, 561f827f, e927c9e3. /OUTNL and /OUTNR partials from C15/C17 to L2/L4 exist.
What closes it (pick one in P6, then re-run place gate, route_auto or hand route):
 a) Shift L3/L4 (+SPK_R tracks, R7/C26/ZR_N cluster) up ~2.5 mm and L1/L2 (+SPK_L) down ~2.5 mm,
    or grow the outline; then the two-column cap arrangement above fits (C18 pads y 23.0/25.0 at
    x 32.8; C15 pads 28.77/30.77 at x 32.8; C17 and C16 in a far column x~38.4).
 b) Put C15-C18 on B.Cu under x 31.5-35 (east of U1's EP, pour stays one piece), free F.Cu for
    four straight OUT tracks U1 -> L1..L4, tie the caps with vias. Cheaper on area, costs 8 vias
    in the spreader edge.
Board left exactly at routing/post-router2.kicad_pcb: 0 DRC errors, 6 unconnected, outline
unchanged (53.65 x 36.9 mm, 9.05-62.7 x 8.25-45.15). Place gate not re-run (no placement change).

## 09:24-09:32Z: option (a) started, stopped at the fallback (coordinator cap 09:45Z)
Done on the board, then saved as routing/wip-optionA.kicad_pcb and the clean board restored
(kicad/...kicad_pcb == routing/post-router2.kicad_pcb, drc_routed re-run: 0 DRC errors, 6 unconnected):
1. route_edit rip (routing/optionA_rip.json, 44 removed): all /BSPR /BSNR /BSPL /BSNL tracks, the
   /OUTNL and /OUTNR partials (C15->L2, C17->L4), all /SPK_L_P and /SPK_L_N tracks. /ZL_P, /ZL_N,
   /ZR_* and /SPK_R_* were NOT ripped (right channel not moved). ZL_* stubs at R4/R5/C23/C24 will
   dangle in the wip and must be ripped when resuming.
2. place_edit move (routing/optionA_move.json, --allow-routed because other nets stay routed):
   L1 (40.5,36.4), L2 (50.1,36.4), C19 (40.5,41.4), R4 (43.9,41.4), C23 (46.3,41.4), R5 (50.5,40.7),
   C24 (50.5,42.3) - the left channel down 2.8 mm (2.5 was 0.03 mm short for two caps in the far
   column). Outline NOT changed (53.65 x 36.9 mm); C24's bottom lands at y 42.6 vs edge 45.15.
3. gate place on the wip: FAIL 5 - C11/L1 courtyard 0.10 mm2 and C14/L1 0.60 mm2 (new: L1 cannot
   shift right, L2 and J3 are hard against it, so C11 and C14 have to give way instead, ~0.5 mm
   each), C12/L3 0.21 mm2 (pre-existing), and U1 + C8 "intersect rule area U1_neck" (2).
   reports/gate-place-optionA.json.
The right channel was not moved: above L3/L4 sit C21/R6/C25 (y 17.4) and then J1/D1 at the top
edge, so "up 2.5 mm" means growing the outline upward by ~2.5 mm and moving J1, D1, C13, C12, C21,
R6, C25, L3, L4, J4 plus the +12V trunk. That is the next pass's first decision; the left half of
option (a) is ready in the wip.

Place gate on the CLEAN board (reports/gate-place.json): FAIL 4 - C11/L1 0.08 mm2 and C12/L3
0.21 mm2 courtyard overlaps (pre-existing, never recorded), plus U1 and C8 intersecting the
U1_neck area. The place check treats any rule area as a keepout; U1_neck has no keepouts and only
exists as the DRC condition for the fine-pitch neck rule, so this is a tooling conflict between
check.place and the neck exception. gate.py --waivers is for human-approved findings, so I left it
alone. Ways out for the next pass: teach check.place to skip rule areas with no keepout flags, or
find a KiCad-10 expression that matches the two 0.343 mm pad-to-pad +12V bridges without an area.
Neither gate recorded (both failing). Nothing committed or ordered.

# 09:36-10:00Z: place gate closed, neck rule area gone; OUT nets still open (hard stop 10:12Z)

Board left at routing/post-placefix.kicad_pcb (== kicad/...kicad_pcb) + post-placefix.kicad_dru.
Pre-state snapshots: routing/pre-placefix.kicad_pcb/.kicad_dru (== post-router2), pre-placefix2.

## Result
- gate place: PASS, recorded in state.json (attempt 18). reports/gate-place.json.
- gate drc_routed: FAIL 6/6 - 0 DRC errors, 0 warnings, 6 unconnected (the 4 OUT nets, as before).
  Not recorded. GND pours: F.Cu 1 island, B.Cu 1 island (EP via array untouched).
- Outline unchanged: 53.55 x 36.8 mm edge rect (9.1-62.65 x 8.299-45.1). Silk "PCB-0017 REV A",
  "+12V", "GND" untouched.

## What moved (place_edit --allow-routed, files routing/placefix*_move.json / _route.json)
- C11 -> (34.6, 35.6) rot 90 (vertical, +12V pad below at 36.6, GND above at 34.6). It had 0.08 mm2
  courtyard overlap with L1; horizontally there is no room between C6's GND pad (x 32.05) and L1's
  courtyard (x 35.905) for an 0805 pad field (3.35 mm) plus check.place's margin, so it went vertical.
  +12V feed re-routed: (32.629,38.089)->(34.6,38.089)->(34.6,36.6), 0.882 mm.
- C12 -> (34.65, 19.2) rot -90 (+12V pad on top at 18.2). It overlapped L3 by 0.21 mm2 and at any x
  between the trunk vertical (x 33.6) and L3 it either shorted the trunk or overlapped L3. The +12V
  trunk vertical moved left 0.3: (35.05,15.118)->(33.3,16.868)->(33.3,17.834)->(32.026,19.108), plus a
  stub (33.3,18.2)->(34.65,18.2) into the pad. All 0.882 mm.
- Reference texts moved (they collided with L1/L3 silk and pads after the moves): C11 ref (26.6,33.9),
  C9 ref (34.7,33.3), C12 ref (36.9,17.4). move_text takes field "reference" (lower case).
- check.place's effective courtyard = courtyard UNION pad box, plus a margin of roughly 0.3 mm - the
  KiCad courtyards on these 0805s are body-only (2.09 x 1.33) while the pad field is 3.35 x 1.41.
  Plan positions against pad boxes, not courtyards.

## U1_neck resolved
The rule area is deleted (text edit of the .kicad_pcb; a pcbnew SWIG Save() was tried first and
reverted - not the cause, but avoided). The dru rule "aiee_neck_fine_pitch_U1" now uses
  A.Type == 'track' && A.NetName == '+12V' && A.Start_X > 29mm && A.Start_X < 30.5mm
  && A.End_X > 29mm && A.End_X < 30.5mm
i.e. an x-window on U1's right pad column (pads span x 28.855-30.585), which matches exactly the two
0.343 mm pad-to-pad bridges (pins 17-18-19 and 31-32). Verified with kicad-cli drc: 0 track_width.
Tested and rejected (kicad-cli, /tmp copies): `A.Length < 1.0mm` does NOT parse in KiCad 10 and
silently disables the WHOLE dru (symptom: netclass clearances only, pours refill with 0.5 mm
clearance, F.Cu GND splits into 9 islands, 17 unconnected). `A.intersectsCourtyard('U1')` parses but
never matches because U1's courtyard is body-only (x 22.955-29.045) and excludes the pads.
If rules_gen.py is re-run, re-append this rule from routing/post-placefix.kicad_dru.
Tooling findings: (1) check.place should ignore rule areas with no keepout flags; (2) a dru parse
failure is silent in kicad-cli - gate.py should fail loudly when the dru does not load (detect by
running with and without the dru and comparing the rule-derived violation counts, or grep the log).

## Not done: option (a) re-place of C15-C18 and the OUT/BS/SPK_L routing
Nothing of option (a) was applied (the 25 min went to the place gate + neck rule). Worked geometry
for the next pass, on top of THIS board (C11/C12 already fixed), all F.Cu, clearance 0.2 to power:
- Pad facts: bootstrap caps are 0805, pads at +-1.0 from centre, pad box 1.35 x 1.41, so a vertical
  cap occupies y c-1.705..c+1.705. C8 pad bottom 22.15, C7 pad top 32.65 bound the near column.
- Near column x=32.8: C18 rot -90 centre y 24.1 (BSPR 23.1, OUTPR 25.1); C15 rot 90 centre 30.2
  (OUTNL 29.2, BSNL 31.2). Four rows pass between them: OUTNR 26.35 (0.624), BSNR 26.96 (0.2),
  BSPL 27.36 (0.2), OUTPL 27.98 (0.624) - the clearances are 0.2-0.235, so keep these numbers.
- Far column x=38.4 (needs L1/L2 down 2.8 as in wip-optionA: L1 (40.5,36.4), L2 (50.1,36.4), C19
  (40.5,41.4), R4 (43.9,41.4), C23 (46.3,41.4), R5 (50.5,40.7), C24 (50.5,42.3); L3/L4 stay):
  C17 rot 90 centre 27.35 (OUTNR 26.35, BSNR 28.35); C16 rot -90 centre 31.05 (BSPL 30.05,
  OUTPL 32.05). Drops in x order: OUTPL down at x=36.2 (27.98 -> 34.2, then diagonal into L1 pad 1
  at (37.42,35.4); stub (36.2,32.05)->(38.4,32.05)); BSPL down at x=36.9 (27.36 -> 30.05, then right);
  BSNR down at x=37.4 (26.96 -> 28.35, then right); OUTNR straight into C17 at 26.35, then on to
  (44.6,26.35)->(47.0,23.95)->(47.0,22.6) = L4 pad 1. OUTPR: (32.8,25.1)->(35.9,25.1)->(37.42,23.6)
  = L3 pad 1.
- OUTNL is the hard one: it must cross OUTPL's drop. Take it down WEST of OUTPL: from C15's pad right
  to x=35.0, down to y 39.0, east under L1's pads (pad bottom 37.96 after the move) to x=45.55, up to
  36.4 and into L2 pad 1 (x 46.258+). That x=35.0 vertical needs C11 clear of x 34.69-35.31: C11 as
  placed now (pad box 33.925-35.275) is 0.03 too far right -> shift C11 to x=34.3 first (pad box left
  33.625, still 0.3 clear of C9's GND pad at 33.3). C14 must also move left ~0.7 (its courtyard hits
  the moved L1: 0.60 mm2 in the wip) and its +12V track (30.23,39.757->41.0) re-added.
- Inside U1's pad column use 0.3 mm stubs to x=30.8 before widening to the class width (the GND
  pads 22/25/28 are 0.2 away from the OUT pads; a 0.624 mm end cap at x<30.8 violates). The neck
  rule only covers +12V, so add a second x-window rule for the OUT nets (or widen the net list) before
  routing them, else 4 track_width errors.
- Rip first (routing/optionA_rip.json, 44 uuids, still valid on this board): all BS*, the OUTNL/OUTNR
  partials, SPK_L_*; also rip ZL_* (4+1 tracks) since R4/R5/C23/C24 move.
- Then: place gate -> hand route (route_edit) or route_auto with --timeout-s 480 --no-krt-finish ->
  kicad-cli drc --refill-zones --save-board -> stitch_vias -> route_cleanup -> gate drc_routed ->
  record. Budget: 45-60 min; it did not fit in this window.

# 10:00-10:05Z: option (a) applied once, did not converge, fallback taken (hard stop 10:18Z)

Board restored to routing/post-placefix.kicad_pcb (+ .kicad_dru); place gate re-run PASS and
re-recorded; drc_routed unchanged (0/0/6). The attempt is saved whole as routing/wip-optionA3.kicad_pcb,
wip-optionA3.kicad_dru, wip-optionA3.drc.json, with its op lists routing/optionA3_move.json (13 place
ops) and optionA3_route.json (52 rips + 71 adds, all applied and verified by route_edit).

What the attempt found (all on the wip, one pass, no iteration):
- DRC copper: 4 clearance errors, 1 short, 1 mask bridge, 1 unconnected; the F.Cu GND pour split
  into 2 islands (B.Cu still 1). Causes: (1) BSNR's start (30.9,26.02)->(30.9,26.26) sits 0.15 from
  OUTNR's 45-degree rise - start BSNR's rise further right (x 31.2) instead of a vertical jog;
  (2) OUTNL's x=35.4 vertical and its y=40.0 run hit C14's GND pad (C14 at 31.2 puts pad 2 at 33.87
  with a ~2 mm pad: right edge ~34.9, top ~40.0) - either run OUTNL's horizontal at y 39.4 with L1
  at y 37.4 (pad bottom 38.96, too tight) or put C14 at x<=30.6; (3) SPK_L_P's y=40.95 run from the
  via to C19 crosses C19's GND pad (41.5,41.75) - route it at y 40.4 or enter C19 pad 1 from the
  left; the mask bridge is the same track. The pour split is the OUTNL loop (x 35.4 down, y 40 east,
  x 45.55 up) enclosing the L1 area: a GND island inside a ring of OUT copper - add a stitch via
  inside the ring (far from U1) or leave a gap for the pour.
- Place gate: 5 courtyard overlaps - check.place's margin is ~0.35-0.4 mm around pad boxes, not
  0.2-0.3: C18/C8 (0.245 gap), C17/L3 (crt 25.695 vs pad top 25.645), C16/C17 (0.2 gap),
  C11/C9 (same-net GND pads 0.175 apart still count), C11/C7. So the two-column stack needs ~0.4 mm
  more per gap: C18 centre 24.3, rows from 26.55, C15 centre ~30.6 (C7 pad top 32.65 -> bottom
  limit 32.3, ok), far column C17 centre 27.6, C16 centre 31.5 -> L1 down to ~37.8, then C19/R4/
  C23/R5/C24 and the SPK_L_P bottom run at y ~44.0 (edge 45.1) - or grow the outline 1 mm down.
- Silk: refs of C16, C18, C24, C9 need moving after the re-place; "PCB-0017 REV A" was moved to
  (18,12) in the wip because C14 at x=31.2 reaches it at (24.5,43.6).
- The dru neck rule in the wip drops the NetName clause and widens the window to x 29-31 mm so
  the 0.3/0.2 mm OUT/BS stubs (29.72 -> 30.9) pass; keep that when resuming.
Estimated to close: one more 45-60 min pass from wip-optionA3 fixing the seven items above.

# 10:06-10:28Z: option (a) converged - all nets routed, place PASS, drc_routed PASS (hard stop 10:45Z)

Live board = kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb + .kicad_dru == routing/wip-optionA4.kicad_pcb/.kicad_dru
(dru unchanged from wip-optionA3: neck rule with no NetName clause, window x 29-31 mm).
Resumed from wip-optionA3; op lists routing/optionA4_rip.json (57 removes: every OUT*/BS*/SPK_L_P
track+via plus the two +12V C11 feed tracks), optionA4_route.json (65 adds), optionA4_route2.json
(2 GND stitch vias), optionA4_move.json (+ move2..move5: C14 and reference-text retries). Reports
alongside (*.report.json).

## Gate results (both recorded in state.json)
- gate place: PASS 0/0 (attempt 23). reports/gate-place.json.
- gate drc_routed: PASS 0/0 (attempt 7): kicad-cli DRC --severity-all 0 violations (silk included),
  0 unconnected. reports/gate-drc_routed.json. Zones refilled (--refill-zones --save-board).
- GND pours: B.Cu 1 polygon. F.Cu 4 polygons, all connected (DRC unconnected 0): the U1-side region
  west of the OUT/BS rows, the C7/C9/C11 pocket between U1's column and OUTNL's x=35.5 drop, and the
  region south of OUTNL's y=40 run are each tied to B.Cu by vias (U1's EP array; new stitch vias at
  (34.3,34.9) and (37.0,42.3); plus (41.0,34.6) inside the OUTNL/OUTPL ring). Not literally "one
  island" - that is impossible on F.Cu once the four OUT nets run from U1 to the far column.

## What changed vs wip-optionA3 (all F.Cu, OUT 0.624, BS 0.2, stubs 0.3/0.2 at x 29.72-30.9)
- The key move: C18 is now HORIZONTAL (rot 0) at (33.8, 23.36) - BSPR pad (32.8), OUTPR pad (34.8).
  This takes OUTPR out of the between-column stack, and the vertical budget between C18 and C15
  (which the place gate's 0.25 mm-per-pad-box margin made 0.06 mm too short for 4 rows) is no longer
  needed there. Rows between the columns: OUTPR 24.59 (passes under C18 pad 1, into pad 2, then
  y 23.36 straight into L3 pad 1), OUTNR 25.42, BSNR 26.12, BSPL 26.53 (rises from its pin), OUTPL
  27.98 -> 28.4 after clearing C15's pad box at x 33.6.
- Far column: C17 (38.4, 27.7) rot 90 (OUTNR 26.7 / BSNR 28.7); C16 (38.4, 31.65) rot -90 (BSPL
  30.65 / OUTPL 32.65). Near column: C15 (32.8, 30.4) rot 90 (OUTNL 29.4 / BSNL 31.4).
  Crossings east of x 34: OUTNR diag (35.0,25.42)-(36.28,26.7); BSNR diag (34.5,26.12)-(35.72,27.34)
  then row 27.34 -> drop x 37.42 -> 28.7; BSPL diag (33.5,26.53)-(34.72,27.75) then row 27.75 ->
  drop x 37.0 -> 30.65. OUTPL drop x 36.33 -> 32.65 -> C16 pad -> (38.4,35.9) straight into L1 pad 1.
- OUTNL: row 29.25 -> x 35.5 down to y 40.0 -> east to 45.55 -> up to L2 pad 1 (as A3 but 0.1 right).
- L1, L2, C19, R4, C23, R5, C24, L3, L4 stay where wip-optionA3 put them; outline NOT grown
  (53.55 x 36.8 unchanged) - not needed once C18 went horizontal.
- C11 -> (34.15, 37.3) rot 90 (GND 36.3 / +12V 38.3): 0.5 mm from C9's pad box (place gate counts
  same-net pads), +12V feed is the single track (32.629,38.089)-(34.15,38.089) ending in the pad.
- C14 -> (29.8, 41.0): its pad 2 (3.5 x 1.2 mm!) now ends at x 34.22, clear of OUTNL; its round
  courtyard reaches x 33.35 so C14 at 30.2 still overlapped C11 (0.43 mm2). The +12V track into
  pad 1 (ends 28.53,41.0) is unchanged and still lands in the pad.
- SPK_L_P: L1 pad 2 -> via (43.58,39.0) -> B.Cu -> via (43.58,40.85) -> F.Cu (43.15,41.28) -> R4
  pad 1 -> down to y 43.95 -> J3 as before; C19 pad 1 is fed by a branch from (43.15,42.97) running
  BELOW C19's GND pad at y 42.97 and entering pad 1 from below (fixes the short + mask bridge).
- Silk: refs moved - C18 (33.8,25.05), C16 (40.3,31.65), C11 (34.6,39.75), C24 (50.2,44.35).
  "PCB-0017 REV A" at (18,12) untouched. Full-severity DRC: 0 silk warnings.
- route_edit gotcha: a "remove" and an "add_track" of identical geometry in ONE op list rolls back
  ("not in saved board") - the add is skipped as "exists" against the pre-removal board. Rip and
  add in two runs.

## P8 verify_all preview (/tmp/a4verify.json, not recorded): 9 errors, 21 warnings
- Known / owner waiver, not mine: check_thermal thermal_area U1 (2L model); 2x undersized_track
  +12V 0.343 mm at x 29.72 (U1 PVCC pin-to-pin bridges).
- Same class as those two, needs the same waiver: 4x undersized_track /OUTPR /OUTNR /OUTPL /OUTNL
  0.300 mm at (30.31, pin y) - the 1.18 mm pad-entry stubs inside the neck window; a 0.65 mm pitch
  pad cannot take a 0.624 mm track.
- check_current pour_neckdown GND F.Cu at (56.24, 26.70) "~0.00 mm between via attachments" - NEW
  location (the earlier one near (45.67,30.76) is gone); next to SPK_L_N's x=56.0 vertical. Not
  looked at; likely a stitch via whose pour attachment is pinched between the SPK_L_N track and
  L4/J4 copper. Move or drop that via.
- check_current insufficient_transition_vias /SPK_L_P at (43.58,39.9): 2 vias, 3 A wants 6. Real
  finding from the layer hop. Either accept for a 1-2 A speaker load (owner call) or add vias: there
  is no room for 6 between L1 pad 2 (bottom 38.96) and OUTNL (top 39.688); via-in-pad on L1 pad 2
  plus a row below OUTNL (y ~40.85, x 42.0-44.0, above R4/C19 pads at 41.3) fits ~3+3.
- Warnings: 5 GND transition-via counts (advisory), 7 check_decoupling (C5/C8/C10/C12/C13 GND stubs
  and loops - pre-existing, not touched), 7 check_silk.
stitch_vias.py and route_cleanup.py were NOT run this pass (no time); run both before P8 for real.
Nothing committed, nothing ordered.

# 10:28-10:36Z: SPK_L_P layer hop fixed (12 vias); pour_neckdown is structural, not fixed

Live board == routing/wip-optionA5.kicad_pcb/.kicad_dru (dru unchanged). Op lists routing/optionA5_rip.json,
optionA5_route.json, optionA5_rip2.json, optionA5_route2.json (+ reports). Gates re-recorded: place PASS
0/0, drc_routed PASS 0/0 (full-severity DRC 0 violations, 0 unconnected, zones refilled).
- SPK_L_P: check_current counts vias per END of a transition (6 each at 3 A), so: 6 via-in-pad on
  L1 pad 2 (x 42.7/43.55/44.4 at y 37.75 and 38.6), B.Cu (43.55,38.6)->(43.55,43.5)->(44.0,43.95)->
  (49.55,43.95), 6 vias on the F.Cu y=43.95 run at x 45.3..49.55 (0.85 pitch). OUTNL's bottom run
  raised to y 39.9. The 2-via hop and the 40.75 bus are gone. insufficient_transition_vias: cleared.
- pour_neckdown GND F.Cu "(56.24,26.70)": NOT a real neck. pour_neck() erodes the whole F.Cu GND
  fill by 0.441 mm and wants every GND via in one eroded component; the F.Cu GND is 4 polygons
  (OUT rows cut the U1 pocket off, OUTNL's loop cuts two more), each with vias (U1 EP array, the
  stitch vias), so the width is 0 and the reported point is just parts[0]'s representative point
  (C20's GND pad). Two GND vias I added at (57.2,27.0)/(54.8,27.0) did nothing; left in (harmless).
  Fix is either a check that works per polygon, or a waiver alongside thermal_area. Do not chase it
  by moving SPK_L_N.
- verify_all preview (/tmp/a5verify.json): 8 errors = 2x +12V 0.343 (waiver), 4x OUT 0.300 stubs
  (waiver, same class), 1 pour_neckdown (above), 1 check_thermal thermal_area (waiver). 23 warnings
  (transition-via advisories incl. the new via rows, check_decoupling C5/C8/C10/C12/C13, check_silk).

# 10:36-10:38Z: SPK_L_P via field moved off L1 pad 2 (no via-in-pad)

Live board == routing/wip-optionA6.kicad_pcb/.kicad_dru (dru unchanged). Ops routing/optionA6_rip.json (11),
optionA6_route.json (13). The 6 vias are now under L1's body between its pads, x 39.6/40.45/41.3 at
y 36.9 and 37.75 (0.85 pitch; 0.6/0.3), fed from pad 2 by two 0.624 F.Cu rows (39.6..43.0) and joined
on B.Cu, then B.Cu (41.3,37.75)->(41.3,43.5)->(41.75,43.95)->(44.0,43.95) into the existing 6-via row
on the y=43.95 run. No via sits inside any SMD pad. Gates re-recorded: place PASS 0/0, drc_routed
PASS 0/0 (full-severity DRC 0/0). verify_all preview: 8 errors, the same 8 (2x +12V + 4x OUT
undersized pin-entry stubs, pour_neckdown structural, thermal_area); 23 warnings; no SPK_L_P
transition finding.

# 11:45-12:00Z: EP 4x4 array + C16/C17 bootstrap placement (hard stop 12:20Z)

Fallback = routing/pre-epfix.kicad_pcb/.kicad_dru (the live board before this pass). Live board now =
routing/epfix_post-ep.kicad_pcb (dru unchanged). Review items 2 and 4 of reports/review-verify.md.

## Fix 1 (done): U1 exposed-pad thermal vias 3x3 @1.0 -> 4x4 @0.9 mm
- 16 pad-"33" thru-holes at x,y in {-1.35,-0.45,0.45,1.35} (footprint-local), 0.61 pad / 0.30 drill,
  outer via edge 1.655 from centre inside the 3.81 x 3.71 EP. Library footprint and the board's U1
  instance (at (26,27) rot -90, all other pads/nets untouched) rewritten by routing/epfix_ep_pads.py;
  lib/EDITS.md has the entry. No track or via sat under the EP on either layer, so nothing was ripped.
- Refill + DRC: routing/epfix_ep_refill.drc.json = 0 violations. Both GND zones are connect_pads yes,
  so all 16 vias are solid-connected to the B.Cu pour and sit inside the F.Cu EP copper.
- Gates recorded (state.json + reports/gate-*.json; copies routing/epfix_gate-*.json): place PASS 0/0
  (attempt 27), drc_routed PASS 0/0 full severity, 0 unconnected (attempt 11), dfm PASS 0/0 (attempt 4).
- fp_verify (routing/epfix_fp_verify.json): pad_count 49 != 32 error is the checker counting the EP +
  thermal vias as copper pads (baseline gave 42 != 32 plus a pad_pitch error that is now gone);
  pad_size warning unchanged. Not a footprint fault.
- verify_all preview (routing/epfix_verify.json, checks in /tmp/epfix_checks): 8 errors, SAME set,
  same positions: +12V undersized 0.343 at (29.72,30.905) and (29.72,22.445); OUT 0.300 stubs at
  (30.31, 27.98/29.28/24.07/25.37) for OUTPL/OUTNL/OUTPR/OUTNR; pour_neckdown GND F.Cu at
  (56.2389,26.6984); check_thermal thermal_area U1 at (26.0,27.0). 23 warnings, unchanged.
  Note: check_thermal's thermal_vias warning still says "found 0 via(s), want >= 15" - it counts board
  vias only, not the footprint's pad-33 thru-holes, before and after; tooling gap, not a board fact.

## Fix 2 (NOT done, board unchanged for it): C16/C17 within ~4 mm of pins 24/26
C16 stays (38.4,31.65) rot -90 = 9.4 mm from pin 24 (29.72,27.33); C17 stays (38.4,27.7) rot 90 =
8.8 mm from pin 26 (29.72,26.02). Worked out and rejected in the 20 min available:
- The only free pocket within 4 mm of the pins is the slot between the OUTPR row (bottom edge 24.90)
  and C15's pad box top (28.695), 3.79 mm tall; a vertical 0805 needs 3.41 + 2x0.5 place margin, so
  only HORIZONTAL caps fit, and two of them need 0.2+1.35+0.5+1.35+0.5 = 3.9 mm (0.11 short; C7, C9,
  C15 down 0.2 would give it - their +12V track ends still land inside the 0.9 mm pads).
- But a horizontal cap forces the OUT net to pass the BS pad on F.Cu (OUT pad on the left: the
  onward OUT track to L1/L4 must pass the BS pad; on the right: the pin track must). Above is the
  OUTPR row, below is the other cap: no 0.624 + 2x0.2 corridor. The 3 A OUT nets cannot hop to B.Cu
  (check_current wants 6 vias per transition end).
- What would work (next pass, 45-60 min like the option-(a) passes): C15 horizontal too, three
  horizontal caps at x centre 33.0 (pads 32.0/34.0) stacked at y ~25.8 (C17, rot 180: OUTNR pad left),
  ~28.2 (C16, rot 180: OUTPL pad left) and ~30.6 (C15), each OUT net passing the cap above it in a
  0.624 corridor (cap pitch 2.375), BS rows at 0.2 threading between (BSPL row ~27.6 needs C17 bottom
  <= 27.28 and C16 top >= 27.9). Requires re-routing OUTNR/BSNR/OUTPL/BSPL/OUTNL/BSNL from the
  pins to the existing tracks east of x 38.4, moving the OUTNL x=35.5 drop, and re-doing C15's nets;
  L1-L4 stay. Distances would be ~2.3-3.0 mm to the BS pins.
Nothing committed, nothing ordered.

# 11:58-12:12Z: C16/C17 bootstrap placement - reverted, geometry re-worked (hard stop 12:27Z)

Live board = routing/pre-bsfix.kicad_pcb/.kicad_dru (== the 4x4-EP board from the pass above),
restored at 12:07Z; gate place PASS 0/0 and drc_routed PASS 0/0 re-run on it (reports/gate-*.json,
copies routing/bsfix_gate-*.json). C15/C16/C17 are where they were. Nothing committed, nothing ordered.
Geometry dump of the region: routing/bsfix_geometry.txt (routing/bsfix_dump.py, bundled pcbnew python:
~/.local/kicad10/bin/python3 - the venv has no pcbnew, the bundled python has no shapely).

## The plan above (three horizontal caps at x 33) cannot be routed on one layer
Pin order top to bottom on U1's east side: OUTPR 24.07, BSNR-pair: OUTNR 25.37 / BSNR 26.02;
BSPL 27.33 / OUTPL 27.98; OUTNL 29.28 / BSNL 29.93. For a horizontal 0805 both nets of a pair
arrive from the left; whichever pad is on the right, the net going to it fences the cap off from
the pin column, so the OTHER net's onward track (the OUT net must go on east to L1-L4) has to
pass on the far side of the cap. With the OUT pin ABOVE the BS pin (OUTNR/BSNR, OUTNL/BSNL) that
far side is the top: OUT pad left => OUT onward must go over the cap; BS pad left => OUT must
cross BS's direct pin-to-pad track. Above C17 sits the OUTPR row (bottom edge 24.90, and it cannot
rise: C18's pads end at 24.035), so there is no 0.624+2x0.2 corridor: C17 horizontal is dead in that
slot, and so is C15 horizontal below C16 (the corridor above it would be under the OUTPL row).
Only BS-above-OUT pairs (BSPR/OUTPR = C18 today, BSPL/OUTPL = C16) work horizontal with BS left.

## What does work: vertical caps, pads in pin order (nothing crosses)
- C17 VERTICAL at (33.0, 26.85) rot 90: pad 2 OUTNR top (33.0,25.85), pad 1 BSNR bottom (33.0,27.85);
  pad box x 32.325-33.675, y 25.145-28.555 (0.245 under the OUTPR row). 3.4 mm from pin 26.
  Applied and DRC'd in routing/wip-bsfix.kicad_pcb (ops bsfix_rip_c17 / bsfix_move_c17 /
  bsfix_route_c17 .json + reports; DRC routing/bsfix_c17.drc.json, 14 violations): all but one are
  the NOT-yet-ripped BSPL 26.53 row and OUTPL 27.98/28.4 row and C15 pad 2 hitting the new cap -
  expected, they go with C16/C15. The one real one: OUTNR (30.9,25.37)->(31.2,25.6) is 0.104 from
  the BSNR stub; start the diagonal later, e.g. (30.9,25.37)->(31.6,25.6)->(32.6,25.6), and enter the
  top pad from its left; onward east (33.4,25.85)->(35.0,25.85)->(36.28,26.7) joins the untouched
  OUTNR track to L4 (10 tracks ripped: BSNR east of x 30.95, OUTNR 31.2..36.28).
- C16 VERTICAL at (33.0, 30.76) rot 90 with pad 1 BSPL on TOP (29.76) and pad 2 OUTPL bottom
  (31.76): box 29.055-32.465 (0.5 under C17, 0.185 above C7's pad top 32.65 - place margin may want
  C16 at 30.7 and C17 at 26.8). 3.3 mm from pin 24. BSPL: (30.9,27.33)->(31.8,27.33)->(32.4,28.9)
  ->pad top; OUTPL: stub (30.9,27.98)->(31.15,28.3)->(31.15,31.3)->(31.7,31.76)->pad; onward east
  from the pad at 31.76 to x 36.33 then the existing 36.33 vertical (shorten it to 31.76-32.65).
  Rip BSPL east of 30.95, OUTPL 30.9..36.33 incl. the 36.33 vertical above 31.76.
- C15 is the open problem: OUTNL/BSNL (OUT above BS) also needs a vertical cap or an OUT-over-top
  corridor, and OUTNL's path east must pass under OUTPL's descent at x 31.15 and its 31.76 row,
  i.e. at y >= 32.98 - into C7 (33.1) / C9 (34.6) at x 31.1-33.3 and the +12V trunk at 33.1. Two
  ways: (1) move C7/C9 +12V decouplers 1 mm down or 1 mm west (they hang off the x 31.5 +12V
  drop; check what sits at y 35.5) and put C15 vertical at (34.9, 33.8) with the OUTNL drop moved
  from x 35.5 to 36.1 and OUTPL's vertical from 36.33 to 37.0 (BSPL's 37.0 vertical is gone);
  (2) leave C15 where it is (2.4 mm from pin 20 already, it is not in the review's list) and only
  move C16/C17 - then OUTPL's onward 31.76 row must stop before C15's pad 2 (32.8,29.4)... it
  does not: C16's bottom pad at 31.76 sits 1.4 mm right of C15's pad column. Simplest (3): swap
  roles - C15 vertical at (33.0,30.76) is the BSNL/OUTNL cap (OUTNL top 29.76, BSNL bottom 31.76:
  OUTNL (30.9,29.28)->(31.6,29.76)->pad, BSNL (30.9,29.93)->(31.4,30.9)->(32.4,31.76)->pad) and
  C16 goes where C15 is not: BSPL/OUTPL is a BS-above-OUT pair so it may be HORIZONTAL rot 0 (BS
  left) in the slot between C17 (bottom 28.555) and C15 (top 29.055)?? - no, 0.5 mm. Put C16
  horizontal at (36.9, 29.5) instead (pads 35.9 BSPL / 37.9 OUTPL, box 35.195-38.605 x
  28.825-30.175): OUTPL row (30.9,27.98)->(33.6,27.98)->(34.02,28.4) stays, continue (34.02,28.4)
  ->(35.2,28.4)?? that passes over the BS pad - fine, BS pad is LEFT and OUTPL enters the right
  pad from above at (37.9,28.4)->(37.9,29.5) then down from the pad to the existing (38.4,32.65)
  ->35.9 drop; BSPL: (30.9,27.33)->(31.7,26.53)->(33.5,26.53)->(34.72,27.75)->(35.3,27.75)->
  (35.9,28.8) - i.e. the existing BSPL row shortened, 0.2 clear of OUTPL's 28.4 row? 27.75+0.1 vs
  28.4-0.312=28.088: 0.24 ok. Needs the OUTNL x=35.5 drop moved east of 38.6 or west: OUTNL onward
  from C15's top pad (33.0,29.76) east at 29.76 hits C16's box (28.825-30.175) - so OUTNL drops at
  x 34.5 (34.188-34.812, 0.38 clear of C16's box) down to 39.9 and east: check L1's courtyard
  (36.8-44.2 x, ~34-40.8 y) - the present 35.5 drop passes it, 34.5 will too. 6.2 mm to pin 24
  is not within 4 - so (3) only fixes C17 and C15; (1) is the full fix and is the 45-60 min pass.
Next pass: resume from routing/wip-bsfix.kicad_pcb (C17 done bar the 0.104 nudge), rip BSPL/OUTPL/
OUTNL/BSNL east of the stubs, decide (1) vs (3), then drc --refill, gates place/drc_routed/dfm,
verify_all preview (8 known errors; the OUT stub positions (30.31, y) do not move).

## 12:08-12:14Z addendum (coordinator asked for a second go to 12:28Z): still reverted
Live board unchanged (== routing/pre-bsfix.*), gates as recorded at 12:07Z. Checked before editing:
- "C17-only" is NOT gate-cleanable on its own: with C17 vertical anywhere in x 32-35 the present
  BSPL 26.53 row and OUTPL 27.98/28.4 rows (to the far C16 at 38.4) run through its pad box, and
  the only way past it is under y 28.755 - which is C15's pad 2 / the OUTNL 29.25 row. So C17
  drags OUTPL, BSPL, and therefore C16 and C15, along. It is one coupled job, not three.
- The vertical-column plan tightened (all clearances 0.2 checked by hand, none by DRC yet):
  C17 vertical at (34.1, 26.85) rot 90 (box 33.425-34.775 x 25.145-28.555), OUTNR top / BSNR bottom;
  C16 vertical at (33.6, 30.96) rot 90 with BSPL on TOP (33.6,29.96) / OUTPL bottom (33.6,31.96),
  box 32.925-34.275 x 29.255-32.665; the gap 28.555-29.255 carries the BSPL row at y 28.855.
  Columns going down from the pin stubs (all F.Cu): BSNL x 30.9 (0.2 wide), OUTNL x 31.55 (0.624),
  OUTPL x 32.4 (0.624, from (30.9,27.98) east then down to 31.5, into the bottom pad at 31.96),
  BSPL x 33.05 (from (30.9,27.33) east at 27.33 to 33.05, down to 28.855, east to 33.6, into the
  top pad). OUTPL onward: bottom pad -> east at 31.96 -> x 36.33 -> the existing 36.33 vertical
  (shortened to 31.96-32.65). OUTNL onward: down x 31.55 to y 32.9, east at 32.9 under C16
  (0.235 clear of its bottom pad) to a new drop at x 35.5 (the present one, extended up from 39.9
  to 32.9 - rip the 29.25 row and the 35.5 drop above 32.9).
- The two things that block OUTNL at 32.9 and BSNL: C7 (33.1) / C9 (34.6) pads top 32.65 at
  x 31.1-33.3 -> move C7 to (32.2,34.1) and C9 to (32.2,35.6) (check what is at y 36.0-36.5
  first; L1's courtyard starts x 36.8 so it is clear) and re-hang their +12V: rip the +12V
  (30.084,33.1)-(31.5,33.1)-(31.5,34.6) pieces and add (29.72,32.736)->(29.72,33.7)->(30.12,34.1)
  ->(31.5,34.1)->(31.5,35.6) 0.882. Then BSNL: it is fenced by OUTNL (east) and +12V (south) on
  F.Cu, so it takes a via pair to B.Cu (BS nets carry mA; check_current only polices OUT/+12V):
  via at (30.9,31.9) down, under the OUTNL/OUTPL columns on B.Cu (the GND pour heals around two
  0.6 vias), up at (35.0,33.6) into C15. C15 then vertical at (35.0, 34.6)?? - that sits on the
  OUTNL 35.5 drop; use C15 vertical at (34.4,34.6) rot 90, OUTNL top pad (34.4,33.6) fed from the
  32.9 row at x 34.4 (the row then continues to the 35.5 drop from the pad's right side? no - a
  0.624 track cannot leave a 1.35-wide pad sideways without passing BSNL; so end the 32.9 row IN
  the top pad and start the drop from the pad's right edge (34.9,33.6)->(35.5,33.6)->(35.5,39.9),
  BSNL bottom pad (34.4,35.6) via at (34.4,36.5) from B.Cu). Distances: C16 3.7 mm from pin 24,
  C17 4.6 mm from pin 26 (x 34.1 is 0.6 further than the 4 mm target - use x 33.7 for C17 if
  BSPL's column moves to 32.95 and OUTPL's to 32.3; margins then 0.19-0.2, DRC decides).
- Estimated at 45-60 min of place_edit/route_edit/DRC loops; not startable in the 17 min left at 12:11Z,
  so nothing was applied. routing/wip-bsfix.kicad_pcb still holds the first C17 attempt at x 33.0.

# 12:24-12:34Z: third C16/C17 pass - not attempted (25 min window), board unchanged
Live board is still routing/pre-bsfix.* (4x4 EP, place/drc_routed/dfm PASS). Established:
- C17 at x 33.0 cannot work by arithmetic: its pad box starts at x 32.325, so OUTPL's F.Cu
  descent must sit at x <= 31.8 (edges 31.488-32.112). Between the pin-pad ends (30.585) and that
  column only 0.9 mm remains; OUTNL's 0.624 column plus BSNL's stub (edge 31.0) need ~1.4 mm.
  A BSNL via at the pin is impossible (a 0.6 via inside the 0.65 pitch hits pins 19/21).
  Execute the addendum's plan instead: C17 at x ~34.1, C16 at x ~33.6.
- B.Cu in x 30-36, y 25-36 is bare GND pour (no tracks; one GND via at (34.3,34.9)), so the BS
  nets can via there freely; that lets BSPL drop its F.Cu column and pulls C17 to about x 33.7.
- Pocket below C16: C6 (30.6,36.2), C11 (34.15,37.3), +12V trunk at x 29.9 y 35.1-37.8 and along
  y 38.089; the free slot for C7/C9 is x 32.2-33.0.
- The full coupled pass is estimated at 45-60 min: give it a whole iteration, started first.

# 12:36-12:56Z: C16/C17 bootstrap caps moved - DONE, live board changed, gates green (hard stop 13:18Z)

Live board = routing/post-bsfix2.kicad_pcb (dru unchanged; fallback routing/pre-bsfix.* kept).
Gates on it (state.json + reports/gate-*.json, copies routing/bsfix2_gate-*.json): place PASS 0/0,
drc_routed PASS 0/0 (parity + all track errors, 0 unconnected), dfm PASS 0/0. Final DRC
routing/bsfix2_g.drc.json = 0 violations, 0 warnings. Nothing committed, nothing ordered.

## Where things are now (all F.Cu parts, same side as before)
- C17 (33.9, 26.85) rot 90: OUTNR top pad (33.9,25.85), BSNR bottom pad (33.9,27.85).
  BSNR pad to pin 26 centre 4.56 mm, to the pin-pad end (30.585,26.02) 3.79 mm (was 8.8).
- C16 (33.7, 30.8) rot -90: BSPL top pad (33.7,29.8), OUTPL bottom pad (33.7,31.8).
  BSPL pad to pin 24 centre 4.68 mm, to the pad end 3.98 mm (was 9.4).
- C15 (32.4, 34.15) rot 0, horizontal: BSNL left pad (31.4,34.15), OUTNL right (33.4,34.15).
  It had to leave (32.8,30.4) because C16 sits there now. BSNL pad to pin 20 ~4.5 mm (was 2.4).
- C7 (28.2, 33.95) and C9 (27.85, 35.4) rot 0, moved from x 32.2 to the free area under U1's
  body (x 26.8-29.3, y 33.5-35.85): the pocket east of the pins is too small for C7, C9 and C15
  with check.place's 0.25 mm pad-field margin (pad boxes need 0.5 mm between parts). C11 stays.
- Refdes moved (silk over pad / silk overlap warnings): C6, C7, C9, C15, C16, C17, C18.
- GND stitch via (34.3,34.9) removed (sat under C15's OUTNL pad); a new one at (32.6,37.1)
  keeps the F.Cu GND pocket around C11's pad tied to B.Cu (without it DRC reports the island).

## Routing (routing/bsfix2_rip.json 29 rips, bsfix2_move.json, bsfix2_route.json + fix1..4)
- OUTNR: untouched - the existing 25.42 row now runs straight through C17's top pad.
- BSNR: (30.9,26.02)->(32.2,26.02)->(32.9,26.72)->(32.9,27.85)->pad, all F.Cu 0.2.
- BSPL: stub -> via (31.35,27.2) -> B.Cu diagonal -> via (34.9,29.8) -> F.Cu into the top pad.
  B.Cu there is bare GND pour; the pour heals around the two 0.6/0.3 vias.
- OUTPL (0.624 F.Cu): (30.9,27.98)->(31.9,27.98)->(32.55,28.63) column to 31.5 -> (32.85,31.8)
  -> bottom pad -> (35.48,31.8)->(36.33,32.65) -> the untouched 36.33/38.4 path to L1.
- OUTNL (0.624 F.Cu): (30.9,29.28)->(31.7,29.28) column to 33.0 -> row to (35.5,33.0) -> the
  35.5 drop to 39.9 (re-added from 33.0). Stub (33.4,33.0)->(33.4,34.15) into C15's pad.
- BSNL: all F.Cu now, no via: (30.9,29.93)->(30.85,30.3)->(30.85,34.15)->(31.4,34.15), running
  0.165 mm right of the +12V pin-pad ends (30.585). A via there is impossible: U1's pads are
  1.731 mm long along x (their ends are at 30.585, not 29.89).
- +12V: C7/C9 hang re-done: (29.72,32.736)->(29.9,32.916)->(29.9,35.109) feeds C6 as before;
  (27.5,32.736) drop off the west trunk to C7 pad 1, then (27.15,34.3)->(27.15,35.4) to C9.
- Clearance is 0.1524 (netclass default 0.152), not the 0.2 the earlier passes assumed - that
  is what made the two columns fit between the pad ends and C16.

## Left
- verify gate still FAIL with the 8 known errors (not re-run; OUT stub positions unchanged).
- check_current's "6 vias per transition" only polices OUT/+12V; the BS nets carry mA.
- The next order needs a fresh fab export (board changed after reports/fab_export.json).
