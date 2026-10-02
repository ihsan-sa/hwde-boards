# Rules added (PCB-0018-A, 2026-09-28)

- sig_branch_PHASE_A / _B / _C, sig_branch_LS_SRC_A / _C (.kicad_dru, appended last so they win):
  track_width min 0.2 mm for tracks of that net fully enclosed by a rule area of the same name.
  The areas are 0.35 mm buffers of the routed branch tracks only (0.25 mm wide): C431 Kelvin to Q401 source,
  R432, R434, C433, C435 (PHASE_x); NT401 and C432 (LS_SRC_A); R426 (LS_SRC_C).
  Reason: these are snubber, sense-divider and Kelvin branches carrying signal/gate-charge current only,
  so the 2.97 mm phase-current width does not apply. Coordinator's call (2026-09-28).
  Clearance rules untouched.
- .kicad_pro not changed: a net class cannot be scoped to an area, so the exception cannot be mirrored there
  without lowering the whole PHASE/LS_SRC net class width. Freerouting would need these branches fixed (locked) instead.

## 2026-09-28 — U301 moved +2.0 mm (Y), escapes rerouted
- No .kicad_dru change. Board-file rule areas only (existing `sig_branch_*` rule, same reason as above):
  - `sig_branch_PHASE_B` near U301 redrawn as a rectangle (63.1,36.9)-(64.7,44.35) to follow the moved
    U301 PHASE_B Kelvin/sense branch to R434.
  - New `sig_branch_PHASE_C` area around the R514 pin-1 → PHASE_C via (73.6,84.5) sense-divider link
    (0.25 mm, signal current only). It stops short of R514's courtyard so the placement gate stays clean;
    the pin-1 end is a small solid-connected PHASE_C zone `R514_link` instead of a track stub.
- R514 rotated 90° about pin 1 to clear the board edge; C408 moved to B.Cu under Q403's tab.

## 2026-09-28 — unconnected-net joins (13 → 10)
- No .kicad_dru or .kicad_pro change. Board-file copper zones only (solid pad connection, not rule areas):
  - `stub_U601_35`, `stub_U601_19` (GND, F.Cu, 0.25 mm, priority 6) + one 0.45/0.2 via each to the In1.Cu GND plane.
    Zones, not tracks, because the GND net class has a 4.26 mm track-width floor; these only return one logic pin each.
  - `hopstub_PHASE_B` (F.Cu, R512.1 → via 66.33,61.37) + `hop_PHASE_B_In1Cu_10` (In1.Cu, 0.3 mm, priority 10) to a via
    at 59.5,61.01 in the main PHASE_B pour. Joins the R512/R423 island (divider and gate-source resistor; signal current
    only) that GATE_HB cut off. On In1 it keeps 0.4 mm to the GND plane (net-class clearance). Vias are marked free so
    KiCad keeps their net.

## 2026-09-28 — inner-layer hops, round 2 (10 → 5 unconnected)
- No .kicad_dru or .kicad_pro change. Each hop is a free via pair, a 0.3–0.4 mm solid-connected zone strip on the inner
  layer, and short F.Cu zone stubs from the pad to the via. Hop clearances are the full HV net-class values (0.4 mm, or 0.5 mm for GH/BST); no
  same-phase relaxation was used.
  - `hop_GHA_In1Cu_12`: from the existing GHA via at U301 p19 (60.9,42.05) to a via at R411.1, 20 mm on In1.
  - `hop_PHASE_A_In1Cu_13`: from C301 p2 (U301 p18 Kelvin zone) to C431 p2. Kelvin only; it meets the power path at Q401's source through
    C431's existing Kelvin branch.
  - `hop_PHASE_C_In1Cu_14`: from R436.1 to R514.1 (sense divider, signal current).
  - `hop_PHASE_C_In1Cu_15`: from C303 p2 (U301 PHASE_C Kelvin zone) to a via at Q405 source pin 1 (73.3,55.3). Kelvin stays
    separate until the source.
  - `hop_VM_IN_In2Cu_16`: from C102 p2 to the existing VM_IN via (18.6,76.6), 4.5 mm on In2, with 0.5 mm local clearance so
    the VM plane clears it by 0.5 mm. VM_IN is the input before Q101, a separate net from VM.

## 2026-09-28 — final joins (5 → 1 unconnected)
- No .kicad_dru or .kicad_pro change. Board-file moves, zones and a few signal reroutes:
  - C103 (100 nF VM_IN decoupler) moved from (33.24,52.23) to (17.55,78.45), rot 180, pad 1 on the edge of the main
    VM_IN pour beside Q101; its GND pad takes a 0.45/0.2 via at (16.85,79.0) that overlaps the pad. Old GND stub + via removed.
  - `stub_U101_2` (GND, F.Cu, priority 6) + via (15.55,74.3) under U101's body for pad 2. That via cut the under-body neck
    joining U101 pad 5 to the VM_IN pour, so `loop_VM_IN_U101_5` (VM_IN, F.Cu, priority 7, 0.4 mm clearance) now joins
    pad 5's pour to C102 p2 around the top of C102.
  - U601 pad 23: `stub_U601_23` (GND, F.Cu) + via (55.35,24.85) in the pocket right of the pad. To make room: LED_FAULT
    B.Cu rerouted (54.69,22.61→54.69,25.0→55.26,25.57→56.57,25.57), INHB B.Cu diagonal given a jog
    (51.0,20.66→53.5,23.16→53.5,24.5→57.14,28.14→58.48,28.14), VDDA feed to C608 p1 now (55.8,25.18→56.15,24.83).
  - `hop_PHASE_B_In1Cu_17`: from the existing PHASE_B Kelvin via (63.65,42.95) to a via at (59.5,58.51) in the main
    PHASE_B pour, 18 mm on In1, 0.3 mm, 0.4 mm clearance. Kelvin/signal current only, same as the A and C hops.

## 2026-09-28 — round 2 (1 → 0 unconnected)
- The saved board now carries filled zones, so DRC with and without --refill-zones agree. The PHASE_B split seen without
  refill came from the stale fill, not from missing copper.
- LS_SRC_C: GATE_LC, GLC and VBUS_SENSE no longer cross the Q406-source → R403 strip on F.Cu. Each crosses on In1
  (0.25 mm, priority 18/19/20, 0.2 mm plane clearance): `hop_GATE_LC_In1Cu_18` R426.1 → R416.2 (9 mm),
  `hop_GLC_In1Cu_19` (68.02,63.9) → R416.1 (26.6 mm, detours around the other two), `hop_VBUS_SENSE_In1Cu_20`
  existing via (68.95,64.42) → via (80.5,68.7) (13.3 mm). LS_SRC_C now fills as one piece.
- UART_RX via moved (49.79,27.00) → (49.59,26.90) to clear hole-to-hole with the ENC_A via.

## 2026-09-28 — P8 DRC cleanup (kicad-cli DRC 0/0, drc_routed PASS)
- `.kicad_dru`: `hv_scope_u101_courtyard` — clearance 0.13 mm when both items touch U101's courtyard (SOT-23-8,
  0.65 mm pitch, 0.29 mm pad gap). Same form as `hv_scope_u301_courtyard`; IPC-2221B Table 6-1 A6 (component leads,
  up to 100 V), VM_IN is a 60 V-class rail and U101 is rated for it. Cleared U101 p1-p2 and p5-p6. Not mirrored in
  .kicad_pro (the U301 rule isn't either). Cited in requirements.md.
- `.kicad_pro`: `lib_footprint_mismatch` severity warning → ignore, hwde's default (board_init.py). Needed because
  `silk_clear` removed the body-outline silk of 17 packed passives (C301 C303 C304 C402 C404 C405 C406 C410 C412 C433
  C502 C705 R421 R423 R435 R512 R601), whose outlines overlapped neighbours' silk and pads.
- No track-width exception. The 109 under-width stubs (GND/VM/PHASE_*/LS_SRC_* pad exits) became same-shape solid
  zones `neck_<net>_<n>` (solid pad connection, priority 61-169, islands kept), per remediations/track_width.md step 4.
  The copper is the same shape as before; only the width rule no longer applies.
- Board: INHA via (51.51,24.00) → (51.51,24.30) with a B.Cu jog to its diagonal, clearing hole-to-hole with the INLA
  via. 11 dangling vias and their orphaned track chains (LED_D603_A, INLC, GLC remnants) removed.
- Silk: silk_place moved 165 refdes; C401 and J702 moved by hand-checked search; 10 refdes with no free spot in the
  power stage hidden (U101 C402 C405 Q405 R513 R424 Q403 R421 R510 Q401). 'PCB-0018 REV A' is on F.SilkS (two copies).
- Zones refilled with kicad-cli (`kc.py drc --refill --save-board`) so saved fills match DRC.

## 2026-09-28 — verify pass attempt (place 15 → 14, verify 382 → 23)
- No rule change. Board fixes (DRC 0/0/0 after refill + parity):
  - C213 and its GND via moved 0.45 mm up (y 33.40 → 32.95); its padded outline no longer touches L202's pad. Place gate 14.
  - VM via fields in the high-side drain pads: Q401 +15, Q403 +12, Q405 +13, Q101 +16 (0.6/0.3 mm). The 10 A legs
    and the 13 A input previously dropped from the In2 VM plane through 1-3 vias each.
  - GND via fields at the shunt returns: F.Cu zones `lobe_R401_2`, `lobe_R402_2`, `lobe_R403_2` (priority 60, solid)
    with +8/+8/+2 vias → 12/12/6. R403 is boxed in by GHC and VBUS_SENSE; it stays at 6.
- Waivers added (reports/verify-waivers.json, per finding with pos, 352 entries):
  - creepage, PHASE_C↔GLA/GND inside U301's courtyard (3): owner's scoped gate-driver rule, IPC-2221B A6 down to 0.13 mm.
  - pdn GND "no decoupling": GND is the return, not a supply.
  - GND single/small via clusters: leaf taps into the one-piece In1 plane; they carry only their part's return.
  - VM single vias: capacitor, snubber, TVS, divider and buck-supply taps; the leg currents use the drain fields.
  - VM_IN sense via and the In2 sliver; VM_IN F.Cu/B.Cu necks (parallel pours, 3.8 + 3.95 mm against 4.26 mm needed).
  - PHASE/LS_SRC 0.25 mm tracks and single vias: Kelvin, gate-return, sense, snubber and In1-hop taps.
  - PHASE_A vias at TP401: parallel stitches, because the B.Cu pour lands directly on the THT pad.
  - Necks: webs inside the shunt via fields, and the plane edges above Q405 (y < 49), which are off the power path.
- Not waived, because they are real and still open (23 left):
  - GHC's B.Cu run (U301 → y 76.8 → x 80) cuts right across the PHASE_C B.Cu output pour at y 76.8, and with
    ISNS_B_N it necks PHASE_B to 0.49 mm at y 75.5. The phase B and C outputs detour through F.Cu necks and via
    clusters to TP402/TP403. GHC needs a new route (an In2 hop across the PHASE_C band); a straight In2 line hit the Q406 via field.
  - PHASE_A B.Cu output pour is 2.86 mm at y 78, where GND vias at (43.72/45.28, 77.84) sit inside it; 2.97 mm is needed.
  - R403 GND return has 6 vias.
  - BUCK_SW (4 vias) and +5V (2 vias): single vias at 0.65-0.9 A against 0.5 A/via. Each needs a companion via.
  - ISNS_A/B/C pairs: skew 8-15 mm and uncoupled N legs. These need coupled rerouting and are not waived.

## 2026-09-28 — phase output paths (verify 23 → 8)
- GHC: the whole B.Cu run (U301 via (61.58,45.45) → y 76.8 → (81.5,65.9)) is replaced by one In2 track above the FET
  row: (61.58,45.45)→(63.63,47.5)→(81.41,47.5)→(82.41,48.5)→(82.41,58.5), plus a new via at (82.41,58.5). The F.Cu stub
  up to R415 pad 1 ends there. The PHASE_C B.Cu pour is one piece again.
- GLC: the B.Cu stretch across PHASE_B at y 64.03 now crosses on In1 from (59.17,64.03) to a new via at (54.5,64.03).
- `widen_PHASE_{A,B,C}_{L,R}`: B.Cu strips, priority 2, 1.9 mm wide, y 75-81, on both sides of each output pour. They
  make up for the INA240 GND vias at y 77.84. Each B.Cu output pour now measures at least 3.48 mm across from y 62 to 82
  (2.97 mm is needed for 10 A).
- A second via (0.75-0.9 mm off, stubs on F.Cu and B.Cu) on +5V ×2 and BUCK_SW ×3. BUCK_SW at (37.01,22.09) has no room.
- Waivers regenerated (383 entries). The PHASE_B/C test-pad stitches and the local B.Cu neck slivers are now waived with
  the measured widths. The VM In2 neck waiver cites the measured plane cross-sections (≥27 mm).
- Open: R403 GND return (6 vias), BUCK_SW (37.01,22.09), and ISNS_A/B/C diff pairs (not waived). The INA240's IN+ (pin 8)
  and IN− (pin 1) sit on opposite pad rows, 5.4 mm apart, and the shunt's net ties are 3.46 mm apart. That leaves about
  9 mm uncoupled at best, against the 3 mm limit, so a reroute can't pass. The lever is the pair constraint, or a waiver
  the owner approves.

## 2026-09-28 — verify/place to recorded PASS, DFM clean
- R403 GND return 6 → 16 vias (fixed, not waived). New F.Cu GND zone `lobe_R403_2_ext` (priority 61, solid,
  (80.6,63.95)-(85.3,63.1)-(85.3,69.3)-(81.9,69.3)-(81.2,68.25)) joins R403 pad 2's lobe, plus 8 GND vias 0.6/0.3:
  (81.5,65.8), (83.4, 64.2/65.2/66.2/67.2), (84.45, 64.1/65.15/66.2). The column at x ≥ 83.4 lands in the main In1 plane
  outside the GLC/VBUS_SENSE In1 hops that box R403 in; it also absorbs the two stitch vias at (84.45, 63.03/67.32).
- DFM (JLC 4-layer, clearance ≥ 0.1016 mm): GND via (46.86,18.68) 0.6 → (46.86,18.65) 0.66 so it merges with
  C705 pad 2 instead of leaving a 0.03 mm same-net slot. Two B.Cu no-pour rule areas (pour only; tracks/vias/pads/footprints
  allowed) remove GND fill pinches of 0.099 and 0.029 mm: `dfm_nopour_B_52_41` (51.98,40.84)-(52.32,41.10) between the INLC
  via and ENC_A, `dfm_nopour_B_63_13` (63.02,13.02)-(63.48,13.40) between the ENC_Z_RAW and SWCLK vias.
- Waivers added to reports/verify-waivers.json (7, pos-bound):
  - ISNS_A/B/C diffpair_skew + diffpair_uncoupled (6), owner-approved: the INA240's IN+ (pin 8) and IN− (pin 1) sit on
    opposite pad rows 5.4 mm apart and the shunt's Kelvin taps (net ties) are 3.46 mm apart, so ~9 mm uncoupled is set by
    the packages, not routing; the INA240 has its own PWM rejection and the signal is low-frequency sense. Not rerouted:
    the A/C N legs loop round C511/C513 (N 17.4/17.8 mm); a B.Cu underpass like phase B's would cut that to ~10.5 mm but
    adds two vias and still fails the 3 mm limit, and P stays 2.4 mm, so no stretch can be coupled.
  - BUCK_SW via (37.01,22.09): it is on the bootstrap branch only (L201 → B.Cu → C201, 2.2 nF BST-SW). Inductor current
    uses the U201 pin 8 → L201 path (two vias per transition). Bootstrap recharge ≤ 2.2 nF × 5 V × 400 kHz = 4.4 mA
    average, about 1% of the 0.5 A per-via rating. No room for a second via at the 0.4 mm BUCK_SW/BST5V clearance.
- Place gate waivers, new file reports/place-waivers.json (14, pos-bound; run gate.py --gate place --waivers it):
  - 12 keepout_violation: the `sig_branch_*` areas are track-width scopes with every keepout flag 'allowed';
    place_metrics treats any copper rule area as forbidden regardless of flags.
  - courtyard_overlap C301/U301: C301 pad 1 (BSTA) is 0.225 mm from U301 pad 19 (GHA); place_metrics grows pads 0.25 mm.
    Legal under hv_scope_u301_courtyard; moving C301 up hits the ENC_A via (0.5 mm HV57 clearance).
  - courtyard_overlap C302/C303: PHASE_B/PHASE_C pads 0.42 mm apart (≥ 0.4 mm HV class). Moving C303 0.12 mm down
    cut the PHASE_C strip to U301 pin 12, so it stays.
- The existing leaf-GND waiver at (46.44,18.315) moved to (46.4425,18.3): the cluster centroid shifted 0.015 mm with the via
  move above (waiver pos tolerance is 0.01 mm). Same reason, no new exception.
