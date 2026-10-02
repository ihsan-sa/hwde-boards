# Reference video — research notes

## 1. Launch page and which board the clip shows

- OpenAI's launch page: https://openai.com/index/gpt-6-astra/ (published ~2026-09-03).
  WebFetch on this URL returned HTTP 403 (blocked), so its exact wording could not be
  pulled directly; content below is from search-result snippets that quote it.
- The launch post's own PCB example is described in search snippets as: the model
  "turning an electronic schematic into a manufacturable PCB by placing components and
  routing copper connections," shown as a short clip alongside unrelated examples (a
  city scene in Unity, a car transmission in FreeCAD/Blender, a Form 1040). SOURCED
  (search snippet citing openai.com/index/gpt-6-astra/).
- Quilter's write-up (https://www.quilter.ai/blog/llm-pcb-layout-gpt-6-astra, fetched)
  states plainly that "the launch post lists a 'Circuit board' example... It publishes
  no PCB-specific benchmark," and "the PCB result is a single video" — i.e. OpenAI
  itself gave no parts list, spec, or board name for the demo clip. SOURCED.
- The board shown in the reference frame (this repo's
  `brief/reference-video-frame.png`) is not an audio amplifier: it shows dual
  half-bridges (Q1-Q6) in three groups, three low-side shunts (SHUNT A/B/C), a VM rail
  feeding a large electrolytic, a QFP MCU, a buck stage (L1, BUCK_SW, V3V3), ten SOIC/
  TSSOP ICs (U1-U10), two switches (SW1/SW2), JST and FFC connectors, five test points
  (TP1-TP5), and ten mounting holes (H1-H10) — a three-phase motor driver layout, not
  an amplifier. This reading is INFERRED-FROM-FRAME (direct visual read of the
  screenshot in this repo), not confirmed by any fetched source.
- The JLCPCB post at https://jlcpcb.com/blog/gpt-6-astra-pcb-design-in-kicad (fetched)
  describes a **different, much smaller board**: a single-IC TPA3116D2 stereo
  amplifier, 44 x 34 mm, two copper layers, ~40-45 SMD parts, connectors J1-J4 and one
  test point TP1 — no MCU, no half-bridges, no shunts, no buck converter. That
  component list does not match the motor-driver frame at all, so either the JLCPCB
  post is illustrating its own reproduction/test board rather than the exact clip
  OpenAI published, or it is describing a different demo entirely. SOURCED (fetched
  directly) that JLCPCB's board is an amplifier; SOURCED that its BOM/size/connector
  list is incompatible with the frame in this repo.
- **Conclusion**: the frame in this repo shows a motor-driver-class board (three
  half-bridges, current shunts, MCU, buck regulator). The JLCPCB post's board is a
  small two-layer audio amplifier and does not match that frame on any dimension
  (part count, connectors, layer complexity). No fetched source ties the exact frame
  in this repo to a named board with a published spec.

## 2. Other public breakdowns found

- Quilter (https://www.quilter.ai/blog/llm-pcb-layout-gpt-6-astra, fetched): confirms
  no spec was published for the demo; notes "nothing in the demo, or in the launch
  post, speaks to whether the finished board behaves as intended" and that the model
  "has no way to evaluate" circuit function from geometry alone. SOURCED. No parts
  list given.
- KiCad forum thread "Open AI claims GPT 6 - ASTRA can make pcb boards"
  (https://forum.kicad.info/t/open-ai-claims-gpt-6-astra-can-make-pcb-boards/71487,
  fetched): general skepticism thread, no frame-by-frame teardown. Posters say the
  model is "very bad with high frequency signals," track sizing, coplanar waveguides,
  BGAs and HDI, and suggest training data skews toward hobby-level open-source
  designs. SOURCED for these general claims; NOT board-specific.
- Hackaday (https://hackaday.com/2026/09/05/can-ai-now-design-pcbs-that-just-work/,
  fetched): repeats the "schematic in, routed PCB out" framing and cites an EEBench
  score of "69.3% (+/- 10%)" for the model, but gives no board-specific detail.
  SOURCED for the benchmark number only.
- A WebSearch summary (not independently fetched) said the clip is a 15-second condensed
  playback of a longer run whose routing was done by Freerouting. A direct fetch of
  quilter.ai's page did not contain that sentence. UNCONFIRMED — flagged, not SOURCED.
- Searches for a frame-by-frame teardown identifying MCU family, gate driver part
  number, current-sense amp part number, MOSFET part number, or buck IC for the
  clip found **nothing**: no X/Reddit/YouTube/EEVblog post doing that analysis turned
  up in search results. Say so plainly: not found.
- NextPCB (https://www.nextpcb.com/blog/gpt-6-astra-kicad-pcb-routing-test) and
  bestpcbs.com posts appeared in search results but were not fetched (budget); their
  titles suggest routing-quality commentary, not a parts teardown of this frame.

## 3. General spec implications

- **Supply range**: frame shows a VM rail feeding a large electrolytic and a buck
  down to V3V3 — consistent with a single external DC input (motor supply) plus a
  regulated 3.3 V logic rail. FRAME-ONLY.
- **Phase current**: three low-side shunts (SHUNT A/B/C) plus three half-bridge pairs
  (Q1-Q6) indicate per-phase current sensing on a 3-phase (BLDC/PMSM-class) bridge.
  No current rating is stated anywhere. FRAME-ONLY.
- **Control interface**: QFP MCU plus two switches (SW1/SW2) and test points suggest
  onboard closed-loop commutation with local user input/test access; JST and FFC
  connectors suggest one power/motor connector and one ribbon connector (e.g. to a
  sensor or host board). FRAME-ONLY.
- **Sensing**: three shunt resistors imply per-phase current sense feeding
  current-sense amplifiers among the U1-U10 ICs; no amplifier part number is
  confirmed by any source. FRAME-ONLY.
- **Protection**: none of the fetched sources discuss protection features for this
  board; nothing to report beyond the physical presence of shunts (over-current
  sensing is plausible but unconfirmed).
- **Size class / layer count**: looks 4-layer per the brief's own read of the frame;
  no source confirms board dimensions or layer count for this specific frame.
  FRAME-ONLY. (For contrast, JLCPCB's unrelated amplifier board is confirmed
  44 x 34 mm, 2-layer — SOURCED, but for a different board.)

Nothing beyond this repo's own frame read supports the three-phase-motor-driver
identification; every part-level claim about *this* board is FRAME-ONLY. The only
SOURCED facts are: (a) OpenAI published no spec for its demo clip, (b) JLCPCB's own
article is about a small two-layer TPA3116D2 amplifier that does not match the frame,
and (c) no public teardown of the motor-driver-looking frame was found in search.
