# PCB-0017-A stereo-class-d-amp - schematic review (P4, adversarial)

Reviewer: hwde schematic-reviewer, fresh context, 2026-09-27.
Under review: `kicad/PCB-0017-A_stereo-class-d-amp.kicad_sch` (digest sexpr_no_uuid:456dd1bf...),
rendered to `reports/schematic.pdf`, netlist exported to `reports/top.net`.
Ground truth: SLOS708G (`research/sources/tpa3116d2.pdf`), `parts/C46497.json`,
`architecture/*.md`, `kicad/constraints.json`, `kicad/decoupling.json`, `kicad/parts.json`,
the verified research records, and live LCSC attributes for C13/C14 (parts_search.py).
Build mode: none ("normal design, full scope"), so no scope tier excludes or requires a
feature class; the delegate's accepted defaults (Q1-Q12) are taken as decisions, not waivers
of rigor.

## Verdict

GATE: 0 errors / 5 warnings. Nothing here stops bring-up or damages hardware at the stated
operating point. The netlist is correct pin for pin against the datasheet tie table; the five
warnings are one supply-ring exposure the design itself recorded but did not close, one
mis-sourced bulk capacitor, one start-up pop / DC-detect margin, one destructive reverse-plug
that the checklist requires flagging even though it was accepted, and one dielectric drift.

## What was verified clean (so the fix loop does not re-check it)

- Every U1 pin lands on the net `architecture/sheets.md` prescribes; 117/117 pins connected,
  29 nets, SYNC (16) is the only no-connect and is an output in master mode (SLOS708 7.3.1).
- Gain/mode: R1 5.6k GAIN/SLV to GND, GVDD leg open = Table 1 row "Master, 20 dB, 60 kOhm".
  MODSEL = GND (BD), AM2/AM1/AM0 = 0/0/0 = 400 kHz (6.6 fOSC table). PLIMIT tied to GVDD with
  C5 1 uF = Fig 27 / 7.3.4 "no limit". MUTE low through 100k (outputs enabled), SDZ high through
  R2 100k to +12V with FAULTZ on the same node = Fig 37 R13/R14 and 7.3.11 self-clearing tie.
- Abs-max on every rail: PVCC/AVCC 13.2 V max vs 30 V abs / 26 V recommended; SDZ/MUTE pulled
  through 100k so the 10 V/ms slew rule (6.1 note 2) is met; inputs 3 V bias + 1.4 Vpk vs 6.3 V.
- Decoupling per pin vs `parts/C46497.json`: each PVCC pair has 1 nF C0G + 100 nF + 10 uF +
  100 uF; AVCC has C6 100 nF; GVDD has C5 1 uF; each BSxx has its own 220 nF to its own OUTxx.
  Bootstrap caps are 50 V X7R against the 16 V minimum (7.3.6) / 25 V design value (8.2.2.5) -
  watch item 3 is closed.
- Single-ended input per 7.3.7: source -> C1/C3 -> INP, INN AC-grounded through C2/C4 of equal
  value. LINP/LINN are capacitor-coupled, not DC-shorted, so PBTL detect (7.4.1) cannot fire.
- LC filter 10 uH + 680 nF per leg is the datasheet's own BTL pair for 4-8 ohm (Fig 35, 6.3
  RL(BTL) row); the 3.3R + 10 nF branch is Fig 37's "EMI C-RC snubber" (see info 4).
- Inductor: Isat 5.5 A vs 3.5 A peak; >= 1 uH at the 7.5 A OC trip is plausible for a 5.5 A
  shielded drum (typ. 30 % drop at Isat) - not measurable from the schematic.
- Bulk-cap polarity: both aiee footprints put the "+" silk mark and the bevelled base corners
  on pad 1, the same convention KiCad's own CP_Elec_6.3x5.4 uses; pad 1 is on +12V for C13 and
  C14. (Vendor drawings not checked - see OPEN.)
- J1-J4 and TP1 carry `exclude_from_bom` on the symbol and their footprints carry
  `exclude_from_pos_files exclude_from_bom`; all 38 fitted parts carry an LCSC field - watch
  item 5 is closed.
- ERC 0/0 and netlist_audit pass are genuine for connectivity, but see info 1 on how little
  ERC can see through the retyped library.

## Warnings

### W1. Hot-plug ring exceeds C13's 25 V rating, and C14 cannot damp it (refs C13, C14, J1; net +12V)

The design records `hotplug_ring_v_max` 26 V (constraints.json B1) and chose C14 as a 35 V
electrolytic "whose ~0.2 ohm ESR damps the hot-plug resonance" (blocks.md B1, power_tree.md 4).
Two things are wrong with that closure:

1. A higher-ESR branch in parallel with a 30 mOhm polymer does not damp the polymer's own
   resonance with the lead inductance. With L_lead 1 uH and 200 uF the ring sits at ~11 kHz,
   where the bank's effective series resistance is the parallel combination of the two
   branches: about 45-50 mOhm whether C14's ESR is 0.25 ohm or 1 ohm (the polymer branch
   dominates). SLUAAL8's criterion needs R_lead + R_bank > 2*sqrt(L/C) = 0.14 ohm, so the bank
   supplies a third of it and the rest has to come from the adapter and its cord. A 1 m 20 AWG
   cord (~0.07 ohm loop) plus adapter output impedance typically gets there, giving a 1.3-1.6x
   peak (17-21 V at 13.2 V); a stiff, short-lead bench supply switched live gets close to the
   recorded 2x figure.
2. Under the design's own 26 V ceiling, C13 (MA25V100M6x6, 25 V polymer) is over its rating.
   U1 (30 V abs max, 27 V OVLO self-clearing) and C14 (35 V) are inside it. Polymer surge
   ratings are typically ~1.15x rated (28.75 V) for milliseconds, but no datasheet exists for
   this MPN (parts.json says so), so that cannot be confirmed.

Why it matters: a live connect at the adapter plug can put one ring peak above C13's rating on
every plug-in; polymers fail short, which then takes the adapter's current limit as the only
protection (Q7). Not a first-power-on killer, but a field reliability hole the design already
half-knew about.

Fix (one of): (a) make C13 a 35 V part - a 35 V low-ESR electrolytic or a 35 V polymer-hybrid
in the same D6.3 footprint keeps the ripple duty; (b) keep C13 and add the one part Q7 allowed
in principle, an avalanche TVS across J1 whose clamp sits under 25 V at the ring current (an
SMBJ13A-class part, not a 16 V one that clamps above 26 V); (c) keep the board as is and
record the acceptance explicitly at H1 with the 26 V vs 25 V number - and in all cases correct
blocks.md/power_tree.md so they stop claiming C14's ESR does the damping.

### W2. C14 is not the low-ESR electrolytic the architecture specifies (ref C14)

Live LCSC attributes for RVT100UF35V167RV0082 (C5138965): "100 uF 35 V, 150 mA @ 120 Hz ripple,
2000 h @ 105 C", no ESR figure, no 100 kHz ripple rating. That is a general-purpose grade, not
the "low-ESR aluminium electrolytic (RVT class)" sheets.md's value table and parts.json's role
text describe. In this schematic its consequence is small - the polymer C13 takes almost all of
the ripple current because its ESR is 10-30x lower - but the recorded reason for the part
("damps the ring", "low-ESR") is fiction on both counts (see W1), and 150 mA at 120 Hz is a
thin margin for the audio-envelope current it does see if the +12V trunk between the two PVCC
pairs is long.

Fix: either source a part with a stated 100 kHz ripple >= 0.5 A and ESR <= 0.3 ohm at 35 V in
D6.3 (there are many at JLC; the polymer's own datasheet-less status argues for one with a
datasheet), or accept the GP part and rewrite its role as "second 100 uF reservoir at the left
bridge, 35 V for ring margin". Merge with W1 if C13 is changed to a 35 V type - then C14 can
become the same MPN and the board has one bulk part number.

### W3. Input RC of 132 ms puts the unplugged-input start-up past the DC-detect window at tolerance corners (refs C1, C2, C3, C4, U1; nets /LINP /LINN /RINP /RINN)

Numbers from the datasheet: Zi 60 kOhm +/-20 % (7.3.2), DC-detect trips when the output
offset exceeds 2.6 V at PVCC 12 V for more than 420 ms (7.3.9, Table 5); at 20 dB that is a
0.26 V input differential. SDZ is a plain pull-up, so the part enables ~10 ms after power.

- Source connected: both input caps charge from 0 to the 3 V bias through equal Zi; the
  differential is only the tau mismatch (caps are M = +/-20 %). A 20 % mismatch peaks near
  0.2 V, i.e. a ~2 V, ~150 ms thump in the speaker, under the DC-detect threshold. Audible,
  not a fault.
- Source unplugged (a normal first power-on on the bench): C1's far end floats, so LINP sits
  at 3 V from t = 0 while LINN ramps through Zi*C2. The differential is 3 V * exp(-t/tau);
  the output is rail-clipped and stays above 2.6 V for tau * ln(3/0.26) = 2.45 tau. Nominal
  tau = 60k * 2.2 uF = 132 ms -> 323 ms, 77 % of the 420 ms window. Worst case (+20 % cap,
  +20 % Zi) tau = 190 ms -> 465 ms: DC-detect trips, FAULTZ pulls SDZ low, the latch clears
  through the tie, the part restarts and repeats until the caps are charged.

It self-recovers, so bring-up proceeds, but a board that faults on power-up with no source is
the first thing a bench will report, and the same 2.2 uF gives a rail-clipped ~0.3 s thump
whenever the source is unplugged. TI's own values (1 uF in Fig 37, 1.5 uF in Table 2) are at
147 ms / 220 ms nominal and 212 ms / 318 ms worst case - inside the window either way. The
2.2 uF is the reference design's value, kept for like-for-like comparison (Q12), and the research record
`audio-line-in-cap-corner-vs-popup-settle` already names the trade; the new fact here is that
the unplugged case reaches the fault threshold at the corners, not just "some pop".

Fix: C1-C4 -> 1.5 uF (Table 2, 1.8 Hz corner) or 1 uF (Fig 37, 2.7 Hz), K tolerance
(parts.json lists TCC0805X7R225K500FT as the K-tolerance sibling; the 1.5 uF/1 uF equivalents
exist as Basic parts), and record it as a deviation from the reference design in COMPARISON.md. If the
comparison must keep 2.2 uF, keep it but write the unplugged-input fault cycle into the
bring-up notes so nobody debugs a healthy board.

### W4. Reverse-plug at J1 is destructive and unprotected (refs J1, U1, C13, C14; net +12V)

Q7 was accepted (no reverse-polarity element, like-for-like with the reference design), and power_tree.md 5
records the risk. The connector checklist still requires the reviewer to flag a destructive
reverse-plug: a reversed 12 V forward-biases U1's body diodes and reverse-biases two
polarised capacitors with only the adapter's current limit in the path. On bare wire pads
there is no keying at all - the only defence is the silk legend.

Fix: at minimum, a "+12V" / "GND" legend at J1 that survives assembly, and a note in
COMPARISON.md that the reference design's board has the same hole. Zero-cost option worth taking: a DNP SMB
footprint across J1 (TVS or Schottky), which does not change the fitted part count the
comparison is measured on. This is a decision already made; the finding exists so the record
shows it was seen at P4.

### W5. C11/C12 are X5R against the recorded X7R (refs C11, C12; net +12V)

CL21A106KAYNNNE is 10 uF 25 V X5R (parts.json says so and flagged it for H1). At 12 V DC bias
a 0805 25 V X5R 10 uF is down roughly 50-60 %, so the "10 uF" mid tier is ~4-5 uF, and it
walks further with temperature (+/-22 % to 85 C). Functionally fine - it sits between the
100 nF and the 100 uF and nothing depends on its exact value - but sheets.md's value table
says X7R and the part was a named P1 decision, so the record contradicts itself.

Fix: record the X5R choice as the decision (cheapest, Basic part), or swap to a 10 uF 25 V
X7R (1206 is the common package for that spec; 0805 X7R 10 uF 25 V parts exist but are
Extended). Not worth a size hit; recording it is enough.

## Info (no action required; noted for the record)

1. Pin types. `lib_pin_types.py` retyped every U1 pin to `passive` except GVDD (`power_out`,
   correct: internal LDO output) and GND/EP/PVCC/AVCC (`power_in`, correct). The datasheet
   types are I / DO / PO / DIO / BST; flattening them means ERC cannot see an OUTxx shorted to
   a rail or to its neighbour, a missing FAULTZ pull-up, or an undriven logic input. Nothing is
   typed wrong for this netlist (watch item 6), but the 0/0 ERC is a connectivity pass, not an
   electrical one. If the librarian wants ERC teeth: OUTxx -> output, FAULTZ ->
   open_collector, SDZ/MUTE/MODSEL/AMx -> input (then the resistor-only drives need the
   usual ERC exclusions).
2. Decoupling roles (watch item 4). `check_decoupling.py` uses `reg_input` only to require at
   least one <= 1 uF ceramic within 7.5 mm of the tagged pin, grouped per (ic, pin, rail); it
   does not tighten the bulk caps' own limits. For a class-D bridge PVCC that is exactly
   SLOS708 10.1 ("as close to the PVCC pins as possible"), so the eight tags are right, not too
   strict. The per-value defaults (1 nF 5/7.5 mm, 100 nF 10/15 mm, 10 uF declared 15 mm,
   100 uF 20/30 mm) match the tier intent.
3. TI Fig 37's R10 3.3R + C58 100 nF across PVCC (watch item 1's "damper") is an HF
   lead-resonance snubber: 100 nF is ~145 ohm at the 11 kHz hot-plug ring, so it does nothing
   for that case. Its absence here is not a finding; the ring question is answered in W1.
4. The 3.3R + 10 nF branches (R4-R7, C23-C26) are Fig 37's EMI C-RC snubber, corner 4.8 MHz;
   at 61 kHz the 10 nF is ~260 ohm, so blocks.md's "keeps the filter damped from 4 to 8 ohm" is
   not what they do (the record `lc-output-filter-q-tracks-load` already says so). Filter Q is
   0.52 at 4 ohm and 1.04 at 8 ohm from the L/C pair itself; +1.5 dB near 45 kHz at 8 ohm is
   above the audio band. Fig 37 also fits a 1 nF per leg to GND after the filter; omitted here
   (EMI is not a requirement). Dissipation in R4-R7 is milliwatts.
5. Speaker outputs are BTL; neither J3/J4 terminal is ground. Silkscreen must say so and carry
   `PCB-0017 REV A` (requirements 8, boards CLAUDE.md) - a layout deliverable, listed so P6
   does not lose it.
6. Schematic readability: the sheet is label-only (no wires), and several labels overprint pin
   names on the wire-pad symbols in the PDF. Not a finding under this contract; the netlist is
   the interface and it is correct.

## OPEN (could not verify)

- Vendor drawings for C13 (no datasheet at LCSC) and C14 (PDF not fetched): pad 1 = anode is
  consistent with KiCad's CP_Elec convention and the library's own "+" mark, but not checked
  against the manufacturer outline.
- C13's surge-voltage rating (no datasheet), which decides whether W1 is a reliability hole or
  a margin note.
- L1-L4 inductance at the 7.5 A OC trip (>= 1 uH required, 6.3); the Sunltech datasheet's
  L-vs-I curve was not read.
- The +12V trunk length between the two PVCC pairs (sets how much of the left bridge's
  envelope current C14 really sees, W2) - a layout quantity.
