# PCB-0017-A stereo-class-d-amp - requirements

Source: `brief/brief.md` (owner brief). No mode token: normal design,
full scope. Run is unattended; every open question in section 9 carries a default the orchestrator
may take as the owner's delegate.

## 1. Function

A stereo class-D audio amplifier board around the TI TPA3116D2, fed from a single 12 V supply,
with stereo line-level input and stereo speaker output on wire pads. It reproduces a published
44 x 34 mm reference design (JLCPCB blog post, link in the brief) so we can compare our result
against the reference design's: a 2-layer board, SMD parts only, as small as
possible, with correctness and the TPA3116D2's thermal pad and heat-sinking taking priority over
size. Work stops at a DRC/ERC-clean fab package (no order) plus a `COMPARISON.md` giving our size,
layer count, part count and DRC result against the reference design's reported 44 x 34 mm, 2 layers, about 40 SMD
parts and 45 footprints. Where we deviate from the reference design we say where and why.

## 2. Interfaces

- Audio input, stereo, line level, single-ended: two channels plus ground, AC-coupled into the
  TPA3116D2 through 2.2 uF X7R capacitors (the reference design's value). Connector: wire pads (the reference design's J1-J4
  are wire pads, not connectors). Input impedance and level are the amplifier's defaults
  (gain set by the 5.6k / 100k resistors the reference design reports). Which of J1-J4 is input vs output vs
  power is not stated - see section 9 Q1.
- Audio output, stereo, bridge-tied load (BTL) speaker outputs, one 10 uH LC output filter per
  channel with a damping branch (the reference design's parts). Wire pads. Speaker impedance not stated - Q2.
- Power input, 12 V DC, wire pads. Q3 covers a screw terminal or barrel jack instead.
- TP1: one test point (the reference design's list). Purpose not stated; ASSUMED: a ground or supply probe pad.
- Configuration: gain / mode set by fixed resistors (the reference design's 5.6k / 100k). No switches, no LEDs,
  no buttons stated. Fault / shutdown / mute pins: pull-up resistors only (the reference design's list), no user
  control - Q4 asks whether a mute or fault indicator is wanted.
- No USB, no RF, no digital interface.

## 3. Power

- Input: single 12 V DC supply (brief). Range not stated; ASSUMED 12 V nominal, tolerate roughly
  10.8 to 13.2 V (a regulated 12 V adapter). The TPA3116D2 accepts a wide range, but the input
  connector, bulk capacitor voltage rating and reverse-polarity choice hinge on the range - Q5.
- Rails: PVCC = 12 V direct to the amplifier. The TPA3116D2 generates its own internal analog and
  gate-drive rails; no external regulator is expected. GUESS: no other rail on the board.
- Supply bypass per the reference design: 100 uF bulk + 100 nF + 1 nF at each PVCC group (the reference design reports one set;
  the datasheet-driven count per pin group is P1's to settle).
- Supply current GUESS (not researched, from the part's class): at 12 V the TPA3116D2 delivers on
  the order of 15 W per channel into 4 ohm or about 8 W per channel into 8 ohm at the onset of
  clipping. Both channels driven at full output into 4 ohm draws about 2.5 to 3 A from 12 V;
  typical music program is well under 1 A. Whether this is treated as >3 A is a section 8 flag - Q6.
- No battery, no charging.
- Reverse-polarity or overvoltage protection at the input: not stated - Q7.

## 4. Environment

Not stated. ASSUMED: indoor bench / hobby use, 0 to 40 C ambient, no enclosure specified, no
ingress rating, no vibration requirement. The TPA3116D2 dissipates a few watts at full output, so
thermal design assumes free air and relies on the PCB copper (thermal pad vias to a bottom copper
pour) rather than an attached heatsink - Q8 confirms no clip-on heatsink is required.

## 5. Size & mounting

- Outline: as small as possible; target to match or beat the reference design's 44 x 34 mm on 2 layers. This is a
  soft target, no HARD cap: correctness and the thermal pad / heat-sinking area come first, and the
  brief asks us to state where we deviate. If the thermal copper needs more area than 44 x 34 mm
  allows, the board grows and COMPARISON.md says so.
- Layers: 2 (brief). Treated as a firm design choice, not a physical cap; P1 may argue for more only
  with a stated reason and the deviation recorded.
- Mounting holes: not stated. The reference design's board is not reported to have any. ASSUMED none (bare module
  with wire pads), see Q9.
- Height limit: none stated. The 100 uF bulk capacitor is the tallest part; SMD only per the brief.
- SMD parts only (brief). Wire pads J1-J4 and TP1 are copper pads, no through-hole connectors.

## 6. Quantity & budget

Not stated. Nothing is ordered in this run (brief: stop at the fab package). ASSUMED for costing
and DFM: 5 boards, hobby budget, no unit-cost target - Q10.

## 7. Assembly

Not stated. ASSUMED: JLC PCBA, all parts on the top side (single-sided assembly) where the layout
allows; the bottom side kept for the thermal copper pour and vias only. A double-sided assembly
is allowed if it is the only way to hit the size target, and COMPARISON.md then says so - Q11.
Parts should be JLC-stocked (basic / preferred where a choice exists) so the package is orderable
as-is even though we do not order.

## 8. Compliance/safety flags

- Mains voltage: no. The board takes 12 V DC from an external supply.
- Batteries: no.
- Motors: no.
- >30 V: no (12 V supply; the TPA3116D2's own switching stays under 30 V).
- High current (>3 A): borderline - flagged. The 12 V input and the BTL speaker outputs carry
  amplifier current. At 12 V into 4 ohm, both channels at clipping, the supply draw is estimated
  near 3 A (section 3 GUESS); the output filter inductors and traces carry a few amps peak per
  channel. Q6 asks how to treat it. Not a guess to proceed on: the trace widths, inductor
  saturation rating and pad sizing depend on the answer.
- RF transmit: no. Class-D switching (about 400 kHz to 1.2 MHz) radiates; the LC output filter
  and layout handle EMI but no intentional transmitter is present.
- Speaker output is a bridge-tied load: neither output terminal is ground. Note for the wire pad
  labelling and for anyone wiring it; not a safety hazard at these voltages.

## 9. Open questions

1. Which of the wire pads J1-J4 carry what? Default: J1 = 12 V power in (V+ and GND), J2 = stereo
   line input (L, R, GND), J3 = left speaker out (+/-), J4 = right speaker out (+/-). Each "pad"
   is a small group of copper pads.
2. Speaker impedance the amplifier should be designed for? Default: 4 ohm minimum, 8 ohm typical
   (the LC output filter values are tuned for this; 10 uH per the reference design suits both).
3. Should the power input stay as bare wire pads like the reference design's, or be a real connector (screw
   terminal or barrel jack)? Default: wire pads, to match the reference design and the SMD-only rule.
4. Do you want a mute/standby control or a fault indicator LED? Default: no - fixed pull-ups so the
   amp is always on, matching the reference design's parts list.
5. Supply voltage range the board must accept? Default: 12 V nominal, 10.8 to 13.2 V (a regulated
   12 V adapter); capacitors rated 25 V or better.
6. Current handling (safety flag, section 8): design the 12 V input path and speaker outputs for how
   much continuous current? Default: 3 A continuous on the 12 V input, 3 A per speaker output,
   which covers both channels driven fully into 4 ohm at 12 V. Answering "yes to the default"
   accepts that the board is sized for up to 3 A; a higher figure widens traces and grows the board.
7. Reverse-polarity protection on the 12 V input? Default: none (matches the reference design's about-40-part
   count); the user must wire polarity correctly.
8. Is PCB copper alone acceptable for heat-sinking (thermal pad vias to a bottom copper pour), with
   no attached heatsink? Default: yes - the TPA3116D2 at 12 V into 8 ohm runs cool on copper
   alone; into 4 ohm continuously it may need more copper area than 44 x 34 mm, and we would then
   grow the board and record the deviation.
9. Mounting holes? Default: none (bare module, like the reference design's).
10. Quantity and budget for the DFM / cost sanity check? Default: 5 boards, no unit-cost target,
    JLC-stocked parts.
11. Assembly: JLC PCBA, top side only? Default: yes, single-sided top; allow bottom-side parts only
    if that is the sole way to meet the size target, and say so in COMPARISON.md.
12. Input level and gain: line level (about 1 Vrms) with the gain the reference design's 5.6k/100k resistors
    set? Default: yes, keep the reference design's gain setting so the comparison is like-for-like.

### Answers to section 9 (orchestrator as owner's delegate, 2026-09-27; recorded as state.json decisions)
All twelve defaults above are ACCEPTED as written. Q6 (current) is PROVISIONAL: 3 A continuous on
the 12 V input and 3 A per speaker output; re-confirmed at H1 against the P1 power research.
