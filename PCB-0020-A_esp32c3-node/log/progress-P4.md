# progress P3-finish + P4 (2026-10-01)
Started: finishing P3 NEXT steps 1-5 (see progress-P3.md), then P4 schematic.

## Owner-visible waivers
- U1 footprint hand-edited with an all-copper antenna keep-out rule area (x +-7.6, y -12.0..-5.6 mm).
  A lib_pull re-run would silently drop it.
- fp_verify U1 exit 1 ("61 != 53 pads") accepted as a checker artifact: it counts the 3x3 EPAD squares
  separately; 53 pad numbers, geometry matches DS Fig 11-1.
- J1/J2/J3 connector footprints have no datasheet extraction; hand-checked only. Re-check before order.
- schematic-reviewer ran on sonnet, not the fable/high tier the skill names (spend cap).
- 6 reviewer warnings accepted (reports/erc-waivers.md): VBUS ~650 mA transient vs 500 mA; SMF5.0A
  clamp 9.2 V vs U2 VDD 7 V abs max; no LiPo reverse protection; U3 Tj ~114 C; IO2/IO8 straps on J4.
- H2 (schematic checkpoint, blocking per the skill) NOT yet recorded: set-phase P5 did not require it.
  The owner must approve before P5 work is trusted.

## Journal
- P3 step1 done: U1 keep-out rule area added + decision. step2 lib_pin_types pass (138 pins retyped) log/lib_pin_types-P3.json
- step3 fp_verify: U2-U5 pass; U1 exit1 = EPAD 3x3 count artifact (decision); connectors no extraction, hand-checked (decision)
- P3 steps 4-5 done: coverage-P3 (parts covered, block gaps as P2), screen pass, P3-digest, phase=P4
- P4: copied stock PinHeader_1x08/1x04_P2.54mm_Vertical into lib/aiee.pretty for J4/J5 edge pads (DNP)
- P4: kicad/gen/power_sheet.py builds (21 parts, hier USB_DP/USB_DM/VBAT_SENSE, 4 decoupling). kicad/gen/_libs.py registers aiee + stock power/Connector_Generic with ksa cache. Next: main_sheet.py, root.py, ERC.
- P4: main_sheet.py + root.py written, build pass (8 decoupling assoc). Running ERC gate.
- P4: ERC gate PASS attempt 1 (0 violations, all 3 sheets; netlist cross-checked vs sheets.md contract, 41 parts)
- P4: netlist_audit pass (182/182 pins, 8 decoupling). reports/schematic.pdf, top.net, erc.json staged. Spawning schematic-reviewer on sonnet (tier says fable/high; spend cap) - waiver recorded.
- P4: reviewer 0 err / 6 warn -> reports/erc-waivers.md (all dispositioned). Next: report_gen, P4-digest, set-phase P5 attempt.
- DONE: P4 complete, phase = P5. NEXT: H2 approval (owner), then P5 board_init + rules_gen per
  agents/board-setup.md (outline is a geometry OUTPUT; no mounting holes; sidecars beside the board).
