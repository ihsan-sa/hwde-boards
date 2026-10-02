# progress P3 (2026-10-01) - stopped at the spend bound, P3 half done
Done: P2 complete (architecture/*, coverage-P2 1 provisional / 5 gap, each recorded as a
"designing under coverage gap" decision; H1 checkpoint 1 approved by delegate with the provisional
list; P2-digest; phase = P3).
P3 done so far:
- parts/parts.json: 24 LCSC parts + J4/J5 edge pads (no LCSC, footprint only). Stock/price via
  parts_search 2026-10-01; red LED is KT-0603R C2286 (Basic) instead of an 0805.
- lib_pull --parts: overall status pass, 24 parts -> lib/ (aiee.kicad_sym, aiee.pretty 17 fps),
  report log/lib_pull-P3.json (per-part status key is not "ok"; check the per-part fields).
- Extractions validated exit 0: C2838502 (U1, 53 pads), C424093 (U2), C841192 (U3), C7519 (U4),
  C92489 (U5). Open in them: U1 pad pitch not dimensioned, no numeric base-board keep-out (DS defers
  to HW design guidelines); U3 has no land pattern in its DS; BME280 DS silent on no-copper-under
  and heat keep-away (our isolation rule is a design choice, not a DS rule).
- Decision recorded: U1 antenna area (13.2 x 5.4 mm, DS p38) overhangs the board edge; U1 footprint
  must carry a keep-out rule area over antenna + 1 mm, all copper.
NEXT (in order):
1. Add the keep-out rule area to the pulled U1 footprint in lib/aiee.pretty (antenna end = the end
   beyond pads 36-48 per DS p10 Fig 3-1), state.py decision noting the hand edit.
2. lib_pin_types.py --lib lib/aiee.kicad_sym --datasheet-json parts/C*.json (not grounding files).
3. fp_verify.py per IC/connector against parts/<lcsc>.json (J1 C165948, J2 C295747, J3 C160404 have
   no extraction - reuse PCB-0015 parts for C165948/C160404 only if they exist there, else pull-check).
4. knowledge.py --coverage --phase P3; datasheet_extract.py --screen <ws>; fix to exit 0.
5. log/P3-digest.md, state.py set-phase --workspace <ws> --phase P4.
Gotcha: never `pgrep -f "lib_pull.py --parts"` in a wait loop - it matches the loop itself.
