"""LUM-PAR-A `thermal` sheet: NTC dividers, window comparator, FAULT driver.

Refdes range (architecture/sheets.md s1.4): 400-499, `#PWR` base 400.
Block B4 - the board's ONLY firmware-independent protection (PAR-REQ-12).

WHAT THIS SHEET IS
------------------
Two 10 k / NTC dividers feed one quad OPEN-DRAIN comparator (U401) whose four
outputs wire-OR onto `FAULT`.  `FAULT` low pulls `/EN_OK` low through U201 on
the `control` sheet, so every driver stage dies through exactly the node
ENABLE uses.  The same two divider nodes also leave the board as `ADC0` /
`ADC1` so the carrier can roll duty back long before FAULT asserts.

  emitter hot      (module RT_LED, 90 C target)   -> CMP on OUT pin 1
  emitter OPEN     (implausibly cold / broken harness) -> CMP on OUT pin 2
  emitter SHORT    (rail-pinned low)              -> CMP on OUT pin 13
  board hot        (RT401, 110 C target)          -> CMP on OUT pin 14

The open+short pair is the point of the whole block (D-T17, E-10): in either
divider orientation a broken harness conductor reads as *cold*, so a single
over-temperature threshold is FAIL-DANGEROUS against the most likely fault in
an off-board module.  The window converts it to fail-safe.

GROUND TRUTH (SPEC s5 - no wiring, no threshold, no value from memory)
----------------------------------------------------------------------
parts/C3658338.json (LM339LV extract), parts/parts.json (every value and
LCSC below), architecture/p4-wiring-notes.md s3 (BINDING errata), and the
library pin table printed by
  schlib.py --pins "aiee:LM339LVPWR" --lib ../lib/aiee.kicad_sym

  * DATASHEET ERRATUM - WIRE BY PIN NUMBER, NEVER BY CHANNEL NAME.  LM339LV
    Figure 5-3 and Table 5.2 transpose the OUT labels (Table 5.2 footnote 1
    admits it).  The pin-NUMBER groupings are identical in both and are what
    this file uses:
        OUT 1  <-> IN- 6  / IN+ 7
        OUT 2  <-> IN- 4  / IN+ 5
        OUT 13 <-> IN- 10 / IN+ 11
        OUT 14 <-> IN- 8  / IN+ 9
    The pulled symbol agrees pin-for-pin (its names follow the Figure 5-3
    convention, so pin 13 prints "OUT4" and pin 14 prints "OUT3" - that is
    the naming collision, not a wiring difference).  `expect=` below pins
    the symbol's own names so a library refresh cannot silently re-map them.
  * Outputs are OPEN-DRAIN, sinking only, explicitly wire-OR-able (four
    independent datasheet statements).  THE `FAULT` ARCHITECTURE IS SAFE.
  * Inputs are rail-to-rail (GND-100 mV to V+ +100 mV), which is exactly what
    disqualifies the classic LM339: the open/cold threshold sits at 3.05 V on
    a 3.3 V rail, above LM339's V+ - 1.5 V input common-mode ceiling.
  * INPUTS ARE DIODE-CLAMPED TO GND **ONLY** - "there is no ESD clamp from the
    inputs to V+" - abs max on an input pin is -0.3 to 6 V and the current
    into an input pin is limited to +-10 mA.  A series resistor ALONE cannot
    hold a high-impedance input below 6 V, because with no clamp no current
    flows and no drop develops: the pin simply follows the fault voltage.
    Section D2 below is the external clamp that makes the series resistor
    mean something.  TI's own words: "If an input is driven from a low
    impedance source, add a series current-limiting resistor to hold any
    clamp current to 10 mA or less; this can be part of the input divider."
  * INPUT BIAS CURRENT IS 5 pA.  This is the fact the whole D2 topology rests
    on: a 10 k series resistor in front of three inputs costs 15 pA x 10 k =
    0.15 uV of threshold error, so the protection resistor is electrically
    free at DC and can also be used as a hysteresis-scaling element.
  * NO INTERNAL HYSTERESIS.  See "HYSTERESIS" below - the answer is not the
    obvious one and three of the four channels cannot have reference-side
    hysteresis at all.
  * VOL is 150 mV typ / 300 mV max at 4 mA sink, i.e. an on-resistance of
    37.5-75 ohm.  Every number below was solved at both corners; the largest
    threshold difference between them is 0.1 K.
  * POR: the outputs are Hi-Z for up to 30 us after V+ crosses 1.5 V, so
    `FAULT` reads NO-FAULT for that window on every power-up.  This is a
    documented device characteristic, NOT a defect, and it is deliberately
    NOT fixed in hardware (p4-wiring-notes s3).  It is harmless here because
    /EN_OK also needs ENABLE from the carrier, which cannot be asserted
    30 us into the daughter's own power-up.
  * Total sink across all four outputs must stay < 200 mA.  Worst case here
    is the FAULT pull-ups: 3.3 V / (10 k carrier || 100 k R207) = 0.36 mA.

DIVIDER ORIENTATION - SETTLED, NOT ASSUMED
------------------------------------------
Both NTCs are the BOTTOM leg:  +3V3 -> 10 k -> node -> NTC -> GND, so
    V(node) = 3.3 x Rntc / (10k + Rntc)     hot -> LOW, cold -> HIGH
    broken harness / open NTC -> 3.30 V      shorted NTC -> 0.00 V
Two independent confirmations:
  1. J5 carries a "dedicated NTC sense return" joined to GND at the
     comparator reference point (blocks.md B6), so RT_LED's far end is GND.
  2. Only this orientation lets the R405-R408 ladder produce TWO distinct hot
     thresholds (89.7 C and 110.8 C).  Inverted, the same chain yields
     91.0 C / -20.1 C / -29.4 C - one hot tap, and the board-hot threshold
     becomes unreachable.  blocks.md B4's "CMP3 ... above ~3.1 V" is the
     INVERTED-orientation number for that row and does not apply; in this
     orientation "above ~3.1 V" is the OPEN case, which CMP on pin 2 owns.

INPUT PROTECTION - SECTION D2.  THE E-2 FIX.  DO NOT REMOVE EITHER PART.
-------------------------------------------------------------------------
`/NTC_LED` arrives on J5 pin 10 from an off-board 10-way harness it shares
with four LED anodes that sit at up to 6.8 V in normal operation and reach
the SMF15A clamp region (VBR 16.7 V, VC 24.4 V at 8.2 A) whenever a string
opens.  U401's inputs are abs-max 6 V with no clamp to V+.  One crimp error
therefore used to destroy the board's ONLY over-temperature protection -
the exact fault class this block exists to catch.  Two elements fix it and
neither works without the other:

  R413  10 k in series, NTC_LED -> CMP_LED (the three comparator pins).
  D401  1N4148W, anode CMP_LED, cathode +3V3 - the clamp the die does not
        have.  Silicon, NOT Schottky, on purpose: at 85 C a Schottky's
        reverse leakage would be tens of uA into a 10 k source impedance
        (hundreds of mV of error), while the 1N4148W's max is 25 nA at 20 V
        / 25 C and stays sub-uA here -> < 0.6 K of threshold error.

  harness at  6.8 V  -> 0.28 mA into D401, U401 input pin at 4.01 V
  harness at 16.7 V  -> 1.27 mA into D401, U401 input pin at 4.03 V
  harness at 24.4 V  -> 2.03 mA into D401, U401 input pin at 4.06 V
  (abs max 6 V; TI's own limit on input clamp current is 10 mA)

R413 IS NOT IN THE ADC PATH.  ADC0 still taps the RAW divider node through
R402, so the protection costs the ICD s3.3 source-impedance budget nothing
- see deviation 3.  Negative harness faults need no external part: the
inputs ARE clamped to GND internally and R413 bounds that current to
V/10 k (1.2 mA at -12 V, against a +-10 mA limit).

R415 does the same job on NTC_BRD.  RT401 is on-board and faces no harness,
so R415 is there for the OTHER reason the series element exists: it sets
the impedance the hysteresis network works against (see HYSTERESIS).

REFERENCE LADDER - the arithmetic a reviewer must be able to check
------------------------------------------------------------------
Ratiometric off `+3V3` (so every threshold tracks the carrier's ADC
reference), chain +3V3 -> R405 2.7k -> A -> R406 27k -> B -> R407 1.2k ->
C -> R408+R416 3.2k -> GND.  Sum 34.1 k, 96.8 uA - inside power_tree s4's
0.10 mA allowance.  R408 is TWO 1.6 k in series because 3.2 k has no single
part in `lib/aiee.kicad_sym` and an exhaustive search of the 11 stocked
0603 1% values found no four-resistor ladder that reaches tap C.

Solved tap voltages with FAULT RELEASED (R410 pulls the chain up - these are
not open-circuit ratios):   A 3.0545 V   B 0.4280 V   C 0.3113 V

THE TAPS ARE NOT THE DIVIDER VOLTAGES OF THE TARGET TEMPERATURES, and that
is a direct consequence of section D2, not an error.  The comparator sees

    V(CMP_LED) = g x V(NTC_LED) + (1-g) x V(FAULT),
    g = Rfb / (Rfb + R413 + Zdiv) = 0.95 at the hot taps

so each tap sits at the COMPARATOR-node voltage of its target temperature,
about 145 mV above the divider voltage.  The DC offset and the hysteresis
are the same quantity, (1-g) x the FAULT swing; you cannot have one without
the other, and every threshold below already contains it.

tap C is deliberately shared by two channels on two DIFFERENT sensors:
board-hot (110 C target on RT401) and emitter-rail-pinned-low (a shorted
RT_LED or a sense-to-return short reads 0 V, far below this tap).  The two
LED/BRD branches are built IDENTICALLY (10 k series, 200 k feedback) so the
shared tap means the same temperature on both.
Sensitivity at the comparator node: -7.63 mV/K (emitter hot), -4.20 mV/K
(hot no.2), -14.75 mV/K (cold).  Against Vos +-3 mV max over temperature
that is +-0.39 K / +-0.71 K / +-0.20 K of threshold error.

HYSTERESIS - WHY IT IS WIRED THE WAY IT IS.  DO NOT "TIDY" THIS.
-----------------------------------------------------------------
A comparator only gets POSITIVE feedback from OUT to IN+.  With an
active-low open-drain wire-OR, OUT is LOW on fault and can therefore only
ever pull a node DOWN.  That fixes the sign of everything:

  * A channel that trips when its sensor node goes HIGH (emitter OPEN) has
    the sensor on IN- and the ladder tap on IN+, so feedback into the TAP is
    positive, and feedback into its SENSOR node is NEGATIVE.
  * A channel that trips when its sensor node goes LOW (all three HOT/SHORT
    channels) has the sensor on IN+ and the tap on IN-, so it is the other
    way round: feedback into the SENSOR node is positive and feedback into
    the tap is negative.
  * CMP_LED is shared by THREE channels and is IN+ for two of them and IN-
    for the third, so ANY feedback there is positive for two channels and
    negative for the third.  There is no wiring that escapes this; the only
    question is which effect is BIGGER, and that is a sizing problem.

THE BUG THAT WAS HERE (review finding W-1, `hysteresis-on-sensor-node`) and
why the previous note in this file was wrong.  With 112 k straight onto the
divider node the emitter-open channel came out NET NEGATIVE: solved exactly,
it tripped at Rntc 109.6 k (-20.6 C) but only HELD above Rntc 200.9 k
(-30.1 C), so anywhere in that window it trips, self-releases and trips
again - a relaxation oscillator on the one channel the block exists for.
The old note was right that a DEAD open (Rntc = infinity) latches, and
wrong to conclude the channel was safe: a PROGRESSIVE harness failure -
a fracturing crimp, a carbon-tracked contact - passes THROUGH 110-200 k on
its way to open, and chatters FAULT, /EN_OK and all four drivers while it
does.  Both analyses were computing real things; the review's is the one
that matters.  Reproduced and re-solved by nodal analysis, not estimated.

THE FIX, and why the series resistors are what makes it work.  The three
feedback paths now land on the PROTECTED nodes, behind R413/R415:

  * The sensor-side step is now 155.9 mV at the hot end and 275.8 mV at the
    cold end - a 1.8:1 spread, where 112 k straight onto the divider gave
    20.7 mV and 241.7 mV, an 11.7:1 spread.  R413 (10 k), not Zdiv (0.86 k
    hot ... 10 k cold), sets the impedance the feedback works into.  That
    11.7:1 spread is exactly why one end of the old design could be right
    while the other end oscillated.
  * R410 is 10 k, not 56 k, so the reference-side step at tap A is 616.3 mV.
    That is the ONLY positive path the emitter-open channel has, and it now
    beats the 275.8 mV negative one 2.2:1, where the old design LOST
    126.2 : 241.7.
  * R410 also drags taps B and C down through the ladder (-86.4 mV,
    -62.8 mV), which is negative feedback for the three lower-bound
    channels; the 155.9 mV sensor-side step is what has to beat it, and
    does - 69 mV of net positive hysteresis on emitter-hot.

Solved DC network (nodal MNA: real FAULT pull-ups 10 k carrier || 100 k
R207, the open-drain sink as an on-resistance, every feedback path, both
dividers, and the ladder loaded by R410 - no linearised estimates):

  channel            trips      releases   band     target
  emitter hot         89.9 C     81.2 C    +8.6 K   90 / 75 C
  emitter short      110.2 C     92.9 C   +17.3 K   n/a (integrity rail)
  board hot          110.2 C     92.9 C   +17.3 K   110 / 95 C
  emitter open       -22.5 C     -3.8 C   +18.7 K   implausibly cold

  EVERY BAND IS POSITIVE.  Re-solved at Ron 37.5 and 75 ohm (VOL typ and
  max) - largest difference 0.1 K - and with J4 unmated, where the loss of
  the carrier's 10 k pull-up moves the trips by at most 1.5 K.
  Latching re-checked directly: a dead-open harness, a 150 k partial open
  (mid-window on the OLD design) and a dead-short harness all trip AND hold.

DEVIATIONS / RESIDUALS (the orchestrator must fold these back)
--------------------------------------------------------------
 1. Bands are 8.6-18.7 K against blocks.md B4's 15 K.  Board-hot lands on
    110.2 / 92.9 C against a 110 / 95 target; emitter-hot trips at 89.9 C
    against 90 but releases at 81.2 C, not 75.  Widening emitter-hot needs
    a bigger (1-g), i.e. a smaller feedback resistor, which trades against
    the emitter-open margin - it is a deliberate stop, not an oversight.
    There is a separate H2 human decision to change R207 100 k -> 10 k on
    `control`; this sheet no longer NEEDS it (see 1a) but would benefit.
 1a. The released FAULT level, which deviation 1 of the previous revision
    reported as falling to 1.80 V - BELOW U201's 2.0 V VIH - when hot and
    unmated, is now 2.81 V at 85 C unmated and 3.05 V mated, because the
    feedback network loads FAULT with 200 k + 200 k instead of 112 k + 56 k
    and R410 returns to a 3.05 V tap.  blocks.md's "defined when unmated"
    claim now survives at temperature.  That fix is a side effect of the
    W-1 sizing, not an independent change.
 2. The feedback no longer loads the divider nodes directly, so the ADC bias
    halves or better: ADC0 reads 0.93 K low at 25 C and 1.41 K low at 85 C
    (was 1.57 / 2.35); ADC1 reads 0.93 K low at 25 C and 1.29 K at 70 C
    (was 3.02 / 4.24).  Still exact, monotonic, ratiometric functions of the
    NTC that firmware can invert, but they DO shift the ADC transfer
    function the ICD documents, so the residual is reported, not hidden.
 3. ADC source impedance.  blocks.md/parts.json claim "5.0 kohm max at 25 C,
    falling monotonically as the NTC heats"; it falls going HOT and RISES
    going cold, because 10k||Rntc -> 10 k as the NTC opens.  R413/R415 are
    NOT in this path, so the protection costs nothing here.  R402/R404 are
    150 R (were 1 k) and the totals are now

        5.03 k at 25 C     1.00 k at 90 C     8.90 k at -20 C
        9.70 k at a broken harness   (was 10.18 k - over the ICD ceiling)

    i.e. the worst case is inside ICD s3.3's 10 kohm for the first time,
    and inside sheets.md s1.4's <= 6 kohm everywhere in the measuring range.
    The old design only reached 10.18 k because the 112 k feedback shunted
    the cold end - it was buying ICD margin with the W-1 defect.
 3a. C402/C403 are 4.7 uF 0805 (were 100 nF 0603) so that dropping R402 to
    150 R does not turn the ADC filter into a pulse filter: R402 x C402 is
    705 us, up from 100 us, and the corner falls from 1.6 kHz to 226 Hz, so
    rejection of the 9.766 kHz LEDC fundamental coupled onto the harness
    improves from -16 dB to -33 dB.  Still 7000x faster than the module's
    5 s thermal time constant, and the comparator taps AHEAD of R402, so
    the protection path is not filtered at all.

 4. TOOLING, not the design: LM339LVPWR is a FOUR-UNIT symbol - the only one
    in lib/aiee.kicad_sym - and kicad-sch-api places ONE unit per component
    while reporting every unit's pins on every instance.  Placing it the
    normal way silently produces a sheet whose units B/C/D pins are wired to
    dangling wire ends (measured: kicad-cli ERC `missing_unit` + 9 x
    `unconnected_wire_endpoint`, netlist pins 2/4/5/8/9/10/11/13/14 floating).
    `_place_unit` / `_merge_units` below are the workaround; anyone adding a
    multi-unit part to another sheet needs the same treatment.

NEW PARTS THIS REVISION (all already in parts/parts.json and lib/aiee.kicad_sym
- no new BOM line item, only more of parts this board already buys)
------------------------------------------------------------------------------
  R413, R415  10 k 0603 1%   C25804    series limiters into the comparators
  R414        100 k 0603 1%  C25803    2nd half of the NTC_BRD feedback
  R416        1.6 k 0603 1%  C22847    2nd half of R408 (tap C)
  D401        1N4148W SOD-123 C81598   the input clamp the LM339LV lacks
Refdes go past sheets.md s1.4's "R405-R412" allocation but stay inside this
sheet's 400-499 block.  R413-R416 and D401 belong in constraints.json's
`analog` placement group with R401-R412/C401-C403 (>= 10 mm from every
inductor); that file is NOT this generator's to edit - reported instead.

VERIFIED (this session, kicad-cli 10.0.3)
-----------------------------------------
Built standalone, then stitched into a throwaway single-sheet root that adds
what the real siblings provide (PWR_FLAG on +3V3/GND from `power`, one load
per interface net from `control`/`led_if`):
    ERC 0 errors / 0 warnings
    56/56 pins of the 22 components on this sheet land on a net, no
                   `unconnected-` singletons, C401 <-> U401.3 recorded
    U401 pins 1..14 land on exactly the nets in section D, 0 mismatches
The project ERC gate itself belongs to the root agent and was NOT run.

Rebuild (writes <out>/thermal.kicad_sch; the ROOT generator owns the project
file and the real kicad/ directory):
    .venv/Scripts/python boards/lumina-par/kicad/gen/thermal.py [out_dir]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import kicad_sch_api as ksa

HERE = Path(__file__).resolve()
BOARD = HERE.parents[2]
REPO = BOARD.parents[1]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "ai-ee" / "scripts"))

import schlib  # noqa: E402

# kicad-sch-api resolves lib_ids through its GLOBAL cache, which never reads
# kicad/sym-lib-table (LEARNINGS 2026-07-27) - register the pulled library.
ksa.get_symbol_cache().add_library_path(BOARD / "lib" / "aiee.kicad_sym")

FP = "aiee"

# ---------------------------------------------------------------- part table
# refdes -> LCSC, straight from parts/parts.json.  No deviations: this sheet
# uses every part sheets.md s1.4 allocates to it, at its allocated value.
LCSC = {
    "U401": "C3658338",    # LM339LVPWR quad open-drain comparator, TSSOP-14
    "RT401": "C49247666",  # 10k B3950 +-1% NTC, 0603
    "R401": "C25804", "R403": "C25804",     # 10k 1% - divider top legs
    "R402": "C22808", "R404": "C22808",     # 150R 1% - ADC series (see dev 3)
    "R405": "C13167",      # 2.7k 1% ladder top
    "R406": "C22967",      # 27k  1% ladder
    "R407": "C22765",      # 1.2k 1% ladder
    "R408": "C22847", "R416": "C22847",     # 2 x 1.6k 1% = tap C bottom leg
    "R409": "C25803", "R411": "C25803",     # 2 x 100k = NTC_LED feedback 200k
    "R412": "C25803", "R414": "C25803",     # 2 x 100k = NTC_BRD feedback 200k
    "R410": "C25804",      # 10k 1% - reference-side feedback into tap A
    "R413": "C25804", "R415": "C25804",     # 10k 1% - comparator series limit
    "D401": "C81598",      # 1N4148W - the input clamp the LM339LV lacks
    "C401": "C14663",      # 100nF - U401 V+ bypass
    "C402": "C354262", "C403": "C354262",   # 4.7uF 0805 - ADC filters
}

# ------------------------------------------------------------------- values
V_10K = "10k 0603 1%"
V_150R = "150R 0603 1%"
V_2K7 = "2.7k 0603 1%"
V_27K = "27k 0603 1%"
V_1K2 = "1.2k 0603 1%"
V_1K6 = "1.6k 0603 1%"
V_100K = "100k 0603 1%"
V_100N = "100nF 50V X7R 0603"
V_4U7 = "4.7uF 25V X7R 0805"
V_NTC = "10k B3950 +-1% NTC 0603"
V_D = "1N4148W switching diode, SOD-123"

# --------------------------------------------------------------- footprints
R0603 = f"{FP}:R0603"
C0603 = f"{FP}:C0603"
C0805 = f"{FP}:C0805"
SOD123F = f"{FP}:SOD-123F_L2.7-W1.6-LS3.8-RD"

# ------------------------------------------------------------------ symbols
SYM_10K = f"{FP}:0603WAF1002T5E"
SYM_150R = f"{FP}:0603WAF1500T5E"
SYM_2K7 = f"{FP}:0603WAF2701T5E"
SYM_27K = f"{FP}:0603WAF2702T5E"
SYM_1K2 = f"{FP}:0603WAF1201T5E"
SYM_1K6 = f"{FP}:0603WAF1601T5E"
SYM_100K = f"{FP}:0603WAF1003T5E"
SYM_100N = f"{FP}:CC0603KRX7R9BB104"
SYM_4U7 = f"{FP}:CC0805KKX7R8BB475"
SYM_NTC = f"{FP}:HNTC0603-103F3950FB"
SYM_D = f"{FP}:1N4148W_C81598"

# ------------------------------------------------------------------- nets
# Sheet-LOCAL label spellings.  The four interface nets are exposed as
# hierarchical pins with these bare names; the ROOT sheet places the local
# label that turns them into the canonical "/FAULT", "/NTC_LED", "/ADC0",
# "/ADC1" of sheets.md s2 (a child-only label would yield "/thermal/NAME").
# NTC_BRD is sheet-internal by design (sheets.md s2) and therefore becomes
# "/thermal/NTC_BRD" - nothing in constraints.json or P5-P8 keys off it.
# +3V3 and GND are bare GLOBAL power symbols, never hierarchical pins.
N_FAULT = "FAULT"
N_NTC_LED = "NTC_LED"
N_NTC_BRD = "NTC_BRD"
N_ADC0 = "ADC0"
N_ADC1 = "ADC1"
N_VREF_OPEN = "VREF_OPEN"      # ladder tap A, 3.055 V, -22.5 C equivalent
N_VREF_EHOT = "VREF_EHOT"      # ladder tap B, 0.428 V,  89.9 C equivalent
N_VREF_HOT2 = "VREF_HOT2"      # ladder tap C, 0.311 V, 110.2 C equivalent
N_HYS_LED = "HYS_LED"          # R409/R411 series midpoint (no other load)
N_HYS_BRD = "HYS_BRD"          # R412/R414 series midpoint (no other load)
N_LAD_D = "LAD_D"              # R408/R416 series midpoint (no other load)
# The PROTECTED comparator nodes (section D2).  Every U401 input pin sits
# here, never on the raw divider; ADC0/ADC1 and the dividers never see the
# feedback current.  Sheet-internal, so they become /thermal/CMP_*.
N_CMP_LED = "CMP_LED"
N_CMP_BRD = "CMP_BRD"


def _place_unit(sh: schlib.Sheet, tmp_ref: str, unit: int, at, pins: dict,
                expect: dict, lib_id: str, value: str, footprint: str):
    """Place ONE unit of a multi-unit symbol and wire that unit's pins.

    LM339LVPWR is the only 4-UNIT symbol in lib/aiee.kicad_sym (units 1-4 =
    the four comparators; unit 1 also carries V+ pin 3 and GND pin 12).
    Two things follow, and both are load-bearing:

      1. A single ksa component covers ONE unit.  Place only unit 1 and
         kicad-cli ERC raises `missing_unit` ("unplaced units [B, C, D]")
         plus an `unconnected_wire_endpoint` for every wire drawn at a
         units-2..4 pin - measured, not assumed.  All four must be placed.
      2. ksa reports EVERY pin of EVERY unit on any instance, each at its own
         sub-symbol offset from that instance's anchor.  With all four units
         stacked on one anchor the bodies overlap and the fan-outs collide -
         e.g. pin 7 (unit 1) sits 2.54 mm from pin 10 (unit 4) on the same
         horizontal line, so pin 7's standard stub would END ON pin 10 and
         short NTC_LED to VREF_HOT2.  Giving each unit its own anchor is what
         removes that hazard; only the pads listed in `pins` are wired.

    ksa refuses a duplicate reference in BOTH `components.add` and the
    `reference` property setter, so each unit is added under its KiCad unit
    letter as a temporary ref (U401B/C/D - which also keeps schlib's per-ref
    pin/anchor/net bookkeeping distinct while wiring) and renamed to the real
    one afterwards by `_merge_units`.
    """
    with schlib._quiet():
        c = sh.sch.components.add(lib_id, reference=tmp_ref, value=value,
                                  position=tuple(at[:2]), unit=unit)
    c.footprint = footprint
    sh._lib_ids[tmp_ref] = lib_id
    sh._rotations[tmp_ref] = 0
    sh._anchors[tmp_ref] = (at[0], at[1])
    names = {p.number: p.name for p in c.pins}
    for pad, want in expect.items():
        if want not in names.get(pad, "<missing>"):
            raise ValueError(f"{tmp_ref} unit {unit} pin {pad}: expected name "
                             f"~'{want}', got '{names.get(pad)}'")
    sh.wire_pins(tmp_ref, pins)
    return c


def _note(sh: schlib.Sheet, at, lines, dy=5.08):
    """A block of sheet text, ONE add_text per line - an embedded newline in
    a quoted s-expression is not a form kicad-sch-api is known to round-trip
    (same helper and same reason as the `power` sheet)."""
    x, y = at
    for i, line in enumerate(lines):
        sh.sch.add_text(line, position=(x, round(y + i * dy, 4)))


def _merge_units(comps: list, ref: str) -> None:
    """Rename temporary unit refs onto the real one (post-wiring)."""
    for c in comps:
        c._data.reference = ref        # bypasses ksa's duplicate guard
        c.set_property("Reference", ref)


def build() -> schlib.Sheet:
    sh = schlib.Sheet("thermal",
                      title="LUM-PAR-A: thermal (NTC dividers, window "
                            "comparator, FAULT)",
                      paper="A3", date="2026-08-07", company="ai-ee",
                      pwr_base=400)

    # =====================================================================
    # A.  Module (emitter) NTC divider  ->  NTC_LED  ->  ADC0
    # =====================================================================
    # RT_LED itself is MODULE BOM, not board BOM: it sits on an RGB package's
    # slug copper (the 1.035 W site, not the 0.383 W white site) and reaches
    # this sheet through two J5 harness conductors, which is why J5 is 10-way
    # (blocks.md B4/B6).  Only the 10 k top leg is on this board.
    #   V(NTC_LED) = 3.3 x Rntc/(10k + Rntc): 1.650 V at 25 C, 0.284 V at
    #   89.7 C, 3.300 V at a broken harness, 0.000 V at a shorted one.
    sh.add_component(SYM_10K, "R403", V_10K, at=(38.10, 38.10),
                     footprint=R0603)
    sh.wire_pins("R403", {"1": "+3V3", "2": N_NTC_LED})

    # R402 <= 1 k is a HARD requirement, not a preference (D-T16, L-11): the
    # divider's own Thevenin impedance is up to 10 k (see deviation 3), and
    # the ICD s3.3 ceiling on what the carrier ADC will accept is 10 k.
    # 150 R, not 1 k: with the feedback network moved off this node the cold
    # end would otherwise total 10.5 k, and 150 R brings the broken-harness
    # worst case to 9.70 k - inside the ICD ceiling for the first time.
    # R402 x C402 = 150 R x 4.7 uF = 705 us, LONGER than the 100 us it
    # replaces, so the filter moves further from a pulse filter, not toward
    # one (sheets.md s1.4).  The comparator inputs tap the RAW node, ahead of
    # R402, so the filter cannot delay the protection.
    sh.add_component(SYM_150R, "R402", V_150R, at=(38.10, 76.20),
                     footprint=R0603)
    sh.wire_pins("R402", {"1": N_NTC_LED, "2": N_ADC0})
    sh.add_component(SYM_4U7, "C402", V_4U7, at=(38.10, 114.30),
                     footprint=C0805)
    sh.wire_pins("C402", {"1": N_ADC0, "2": "GND"})

    # =====================================================================
    # B.  Board NTC divider  ->  NTC_BRD  ->  ADC1
    # =====================================================================
    # RT401's PLACEMENT is load-bearing and belongs to P6, not here (T-3):
    # ON the copper of the hottest driver stage, OUTSIDE the ICD s7.6 DC-DC
    # hot zone (2,46)-(36,68).  constraints.json already carries it as the
    # `ntc_brd` placement group anchored on U301.
    sh.add_component(SYM_10K, "R401", V_10K, at=(88.90, 38.10),
                     footprint=R0603)
    sh.wire_pins("R401", {"1": "+3V3", "2": N_NTC_BRD})
    rt = sh.add_component(SYM_NTC, "RT401", V_NTC, at=(88.90, 76.20),
                          footprint=R0603)
    sh.wire_pins("RT401", {"1": N_NTC_BRD, "2": "GND"})
    rt.set_property("Note", "P6: ON the hottest driver stage copper, "
                            "OUTSIDE the DC-DC hot zone (2,46)-(36,68)")
    sh.add_component(SYM_150R, "R404", V_150R, at=(88.90, 114.30),
                     footprint=R0603)
    sh.wire_pins("R404", {"1": N_NTC_BRD, "2": N_ADC1})
    sh.add_component(SYM_4U7, "C403", V_4U7, at=(88.90, 152.40),
                     footprint=C0805)
    sh.wire_pins("C403", {"1": N_ADC1, "2": "GND"})

    # =====================================================================
    # B2. Input protection / hysteresis-scaling series limiters (E-2 fix)
    # =====================================================================
    # Read "INPUT PROTECTION - SECTION D2" in the module docstring before
    # touching either resistor or the diode.  Two jobs in one part each:
    #   1. R413 bounds the current a 6.8-24.4 V harness fault can push into
    #      D401 (2.03 mA worst case, TI's limit is 10 mA), and D401 is what
    #      turns that current into a clamped 4.06 V at the input pin - the
    #      LM339LV has an internal clamp to GND but NONE to V+.
    #   2. Both resistors fix the impedance the hysteresis network works
    #      into at ~10 k, instead of the NTC's own 0.86 k (hot) to 10 k
    #      (cold).  That is what makes the band temperature-independent and
    #      is the other half of the W-1 fix.
    # Input bias current is 5 pA, so neither resistor costs any DC accuracy.
    sh.add_component(SYM_10K, "R413", V_10K, at=(38.10, 152.40),
                     footprint=R0603)
    sh.wire_pins("R413", {"1": N_NTC_LED, "2": N_CMP_LED})
    d401 = sh.add_component(SYM_D, "D401", V_D, at=(38.10, 190.50),
                            footprint=SOD123F, expect={"1": "K", "2": "A"})
    # Cathode (pin 1, the BANDED end) to +3V3, anode to the protected node:
    # reversed it is a forward diode at ~1 V and shorts the sense node to
    # the rail.  Silicon 1N4148W, not a Schottky - see the docstring.
    sh.wire_pins("D401", {"1": "+3V3", "2": N_CMP_LED})
    d401.set_property("Note", "E-2 clamp - band to +3V3, do not remove")
    sh.add_component(SYM_10K, "R415", V_10K, at=(88.90, 190.50),
                     footprint=R0603)
    sh.wire_pins("R415", {"1": N_NTC_BRD, "2": N_CMP_BRD})

    # =====================================================================
    # C.  Reference ladder - ratiometric off +3V3 (see the module docstring)
    # =====================================================================
    #   +3V3 -R405 2.7k- A -R406 27k- B -R407 1.2k- C -R408 1.6k- D
    #                                              -R416 1.6k- GND
    #   Loaded taps (FAULT released): A 3.0545 V, B 0.4280 V, C 0.3113 V.
    #   34.1 k total, 96.8 uA.  The taps sit at the COMPARATOR-node voltage
    #   of each target temperature, not the divider voltage - that offset is
    #   the same quantity as the hysteresis (docstring, REFERENCE LADDER).
    # Ratiometric matters: the carrier's ADC reference is the same +3V3, so a
    # rail error moves the thresholds and the ADC readings by the same factor
    # and the reported temperature does not shift.
    for ref, sym, val, y, top, bot in (
            ("R405", SYM_2K7, V_2K7, 38.10, "+3V3", N_VREF_OPEN),
            ("R406", SYM_27K, V_27K, 76.20, N_VREF_OPEN, N_VREF_EHOT),
            ("R407", SYM_1K2, V_1K2, 114.30, N_VREF_EHOT, N_VREF_HOT2),
            ("R408", SYM_1K6, V_1K6, 152.40, N_VREF_HOT2, N_LAD_D),
            ("R416", SYM_1K6, V_1K6, 190.50, N_LAD_D, "GND")):
        sh.add_component(sym, ref, val, at=(139.70, y), footprint=R0603)
        sh.wire_pins(ref, {"1": top, "2": bot})

    # =====================================================================
    # D.  U401 - the window comparator.  WIRED BY PIN NUMBER (erratum).
    # =====================================================================
    # Channel map, pin numbers only.  "trips" always means the output SINKS,
    # pulling FAULT low, which is the only thing an open drain can do.
    # EVERY INPUT PIN IS ON A **PROTECTED** NODE (CMP_LED / CMP_BRD), never
    # on the raw divider - that is the E-2 fix and it is not optional:
    #
    #   OUT 1  IN- 6 = tap B (0.428 V), IN+ 7 = CMP_LED
    #          -> sinks when CMP_LED < 0.428 V  = EMITTER HOT (89.9/81.2 C)
    #   OUT 2  IN- 4 = CMP_LED,        IN+ 5 = tap A (3.055 V)
    #          -> sinks when CMP_LED > 3.055 V  = EMITTER OPEN / IMPLAUSIBLY
    #             COLD (-22.5/-3.8 C; a broken harness parks it near 3.30 V)
    #   OUT 13 IN- 10 = tap C (0.311 V), IN+ 11 = CMP_LED
    #          -> sinks when CMP_LED < 0.311 V  = EMITTER SHORT / RAIL-PINNED
    #             LOW (110.2/92.9 C equivalent; a real short parks it at 0 V)
    #   OUT 14 IN- 8  = tap C (0.311 V), IN+ 9  = CMP_BRD
    #          -> sinks when CMP_BRD < 0.311 V  = BOARD HOT (110.2/92.9 C)
    #
    # THE RULE THAT MUST SURVIVE EVERY FIX LOOP:
    #   FAULT IS OPEN DRAIN AND MUST NEVER BE DRIVEN HIGH (ICD s3.3,
    #   sheets.md s4 note 2).  ERC will want a driving pin on this net; the
    #   four outputs above plus R207 (100 k pull-up, `control` sheet) plus the
    #   carrier's own 10 k are it.  DO NOT add a push-pull buffer, a logic
    #   gate, a totem-pole driver, or a second pull-up here.  The carrier's
    #   eFuse fault is wire-OR'd onto the same node from the other side.
    # No pin of U401 is unused, so there is no no-connect and no floating
    # input: the datasheet's "do NOT tie the two inputs of an unused channel
    # together" trap cannot arise on this board.
    #
    # The symbol has FOUR UNITS; each is placed on its own anchor and only
    # its own pads are wired.  See _place_unit for why both halves of that
    # sentence are mandatory.  Unit 1 carries V+ (3) and GND (12), so it is
    # the one that goes through place_ic_with_decoupling and owns C401.
    u1_lib = f"{FP}:LM339LVPWR"
    u1_val = "LM339LVPWR quad open-drain comparator TSSOP-14"
    u1_fp = f"{FP}:TSSOP-14_L5.0-W4.4-P0.65-LS6.4-BL"
    # Library pin NAMES follow the datasheet's Figure 5-3 convention, NOT the
    # extract's Table 5.2 names (that is the erratum: pin 13 prints "OUT4"
    # and pin 14 prints "OUT3").  The minus signs are U+2212, which is what
    # the pulled symbol stores.  These assertions are the wiring insurance.
    sh.place_ic_with_decoupling(
        "U401", u1_lib, u1_val,
        at=(215.90, 63.50),
        pins={"1": N_FAULT,        # OUT, emitter hot
              "3": "+3V3",         # V+, 1.65-5.5 V rec (6 V abs)
              "6": N_VREF_EHOT,    # IN-, emitter hot
              "7": N_CMP_LED,      # IN+, emitter hot   <- R411 lands here
              "12": "GND"},
        footprint=u1_fp,
        expect={"1": "1OUT", "3": "VCC", "6": "1IN\u2212", "7": "1IN+",
                "12": "GND"},
        decoupling=[
            # Sec 9: "Bypass the supply directly at each device with a low ESR
            # 0.1 uF ceramic bypass capacitor directly between VCC pin and
            # ground pins."  Critical here because the output edges are tens
            # of ns - an un-bypassed supply rings and false-triggers.
            {"cap": "C401", "pin": "3", "rail": "+3V3", "value": V_100N,
             "lib_id": SYM_100N, "footprint": C0603,
             "max_dist_mm": 3.0},
        ],
        caps_at=(165.10, 63.50))
    units = [
        _place_unit(sh, "U401B", 2, (215.90, 114.30),
                    {"2": N_FAULT,          # OUT, emitter open / cold
                     "4": N_CMP_LED,        # IN-, open channel
                     "5": N_VREF_OPEN},     # IN+, open   <- R410 lands here
                    {"2": "2OUT", "4": "2IN\u2212", "5": "2IN+"},
                    u1_lib, u1_val, u1_fp),
        _place_unit(sh, "U401C", 3, (215.90, 152.40),
                    {"8": N_VREF_HOT2,      # IN-, board hot
                     "9": N_CMP_BRD,        # IN+, board hot <- R414 lands here
                     "14": N_FAULT},        # OUT, board hot
                    {"8": "3IN\u2212", "9": "3IN+", "14": "OUT3"},
                    u1_lib, u1_val, u1_fp),
        _place_unit(sh, "U401D", 4, (215.90, 190.50),
                    {"10": N_VREF_HOT2,     # IN-, emitter short
                     "11": N_CMP_LED,       # IN+, emitter short
                     "13": N_FAULT},        # OUT, emitter short
                    {"10": "4IN\u2212", "11": "4IN+", "13": "OUT4"},
                    u1_lib, u1_val, u1_fp),
    ]

    # =====================================================================
    # E.  Hysteresis / positive feedback.  READ THE DOCSTRING BEFORE EDITING.
    # =====================================================================
    # The sensor-side paths land on the PROTECTED nodes, behind R413/R415 -
    # NOT on the divider nodes.  That single change is what fixes W-1, and
    # it does three things at once:
    #   - the step it produces is set by R413 (10 k), not by the NTC's own
    #     0.86 k...10 k, so the band no longer swings 11:1 with temperature;
    #   - the divider nodes, hence ADC0/ADC1, carry a much smaller share of
    #     the feedback current (bias halves: deviation 2);
    #   - the emitter-open channel's negative path shrinks from 244 mV to
    #     152 mV while R410's positive path grows to 616 mV.
    #
    # R409 + R411 IN SERIES = 200 k, FAULT -> CMP_LED, because 200 k is not
    # a stocked value and because Rfb must stay >> R413 or the comparator
    # node stops tracking the sensor (gain 0.95 here; at 100 k it would be
    # 0.90 and the thresholds would follow the FAULT level around).
    # HYS_LED is the midpoint and carries nothing else.
    sh.add_component(SYM_100K, "R409", V_100K, at=(292.10, 38.10),
                     footprint=R0603)
    sh.wire_pins("R409", {"1": N_FAULT, "2": N_HYS_LED})
    r411 = sh.add_component(SYM_100K, "R411", V_100K, at=(292.10, 76.20),
                            footprint=R0603)
    sh.wire_pins("R411", {"1": N_HYS_LED, "2": N_CMP_LED})
    r411.set_property("Note", "200k with R409 - lands on CMP_LED (W-1)")

    # R410, FAULT -> tap A (IN+ pin 5).  The one reference-side feedback the
    # topology allows: the open channel's sensor is on IN-, so pulling the
    # TAP down on fault reinforces the trip.  10 k, not 56 k: this is the
    # ONLY positive path the emitter-open channel has and it has to beat the
    # 152 mV negative one.  2.48 k tap against 10 k gives 3.0545 V released /
    # 2.4383 V asserted = 616 mV, a 4:1 win and an 18.7 K cold-side band.
    # Its coupling down the ladder (-86 mV at tap B, -63 mV at tap C) is
    # negative feedback for the other three channels and is already inside
    # every trip/release number in the docstring.
    sh.add_component(SYM_10K, "R410", V_10K, at=(292.10, 114.30),
                     footprint=R0603)
    sh.wire_pins("R410", {"1": N_FAULT, "2": N_VREF_OPEN})

    # R412 + R414 IN SERIES = 200 k, FAULT -> CMP_BRD (IN+ pin 9).  Built
    # IDENTICALLY to the LED branch on purpose: tap C is shared by board-hot
    # and emitter-short, so the two branches must have the same gain for the
    # shared tap to mean the same temperature on both sensors.
    sh.add_component(SYM_100K, "R412", V_100K, at=(292.10, 152.40),
                     footprint=R0603)
    sh.wire_pins("R412", {"1": N_FAULT, "2": N_HYS_BRD})
    r414 = sh.add_component(SYM_100K, "R414", V_100K, at=(292.10, 190.50),
                            footprint=R0603)
    sh.wire_pins("R414", {"1": N_HYS_BRD, "2": N_CMP_BRD})
    r414.set_property("Note", "200k with R412 - matches the LED branch")

    # =====================================================================
    # rails - CONSUMING power symbols only
    # =====================================================================
    # The `power` sheet owns the PWR_FLAG for every rail (each one enters the
    # board through J3's passive pins there).  A second flag on the same net
    # collides power_out <-> power_out at the project ERC, which is the same
    # trap p4-wiring-notes s2 documents for the driver VCC nodes - hence
    # flag=False on both.  A power SYMBOL is still required: without one, a
    # bare "GND"/"+3V3" label inside a child sheet names "/thermal/GND".
    sh.power_flag("GND", at=(330.20, 38.10), sym="power:GND", flag=False)
    sh.power_flag("+3V3", at=(330.20, 63.50), sym="power:+3V3", flag=False)

    # =====================================================================
    # sheet interface (sheets.md s2)
    # =====================================================================
    # Free-cluster variant: local label + hierarchical label on one stub, so
    # the hier label joins the net by wire geometry rather than by name.
    # Shapes are semantic (kicad-sch-api drops the shape on a CHILD's label -
    # LEARNINGS 2026-07-28 - but Project.add_sheet honours it on the ROOT's
    # sheet pin, which is where it is read).
    #   FAULT    output : driven HERE (open drain, sinking only)
    #   NTC_LED  input  : arrives from `led_if` (J5 harness pin)
    #   ADC0/1   output : sourced HERE, on to `control` -> J4
    for i, (net, shape) in enumerate([
            (N_FAULT, "output"),
            (N_NTC_LED, "input"),
            (N_ADC0, "output"),
            (N_ADC1, "output")]):
        sh.hier_pin(net, shape=shape, at=(330.20, 114.30 + i * 12.70))

    # =====================================================================
    # on-sheet notes - the two facts a future editor must not have to infer
    # =====================================================================
    _note(sh, (330.20, 177.80), [
        "U401 INPUT PROTECTION (R413/R415 + D401):",
        "LM339LV inputs are abs-max 6 V and are",
        "clamped to GND ONLY - there is no ESD",
        "clamp to V+. /NTC_LED shares the J5",
        "harness with LED anodes that reach the",
        "SMF15A 16.7-24.4 V clamp region. Series R",
        "alone does NOTHING without D401. DO NOT",
        "REMOVE EITHER, and keep D401's band",
        "toward +3V3.",
    ])
    # Clear of the A3 title block (which starts at ~x 290 / y 250) - a note
    # that lands under it is a note nobody reads.  kicad-sch-api CENTRES a
    # text object on its anchor, so x must leave half the block's width
    # inside the border too.
    _note(sh, (63.50, 228.60), [
        "HYSTERESIS RETURNS TO CMP_LED / CMP_BRD,",
        "NOT to the divider nodes. On the divider",
        "the emitter-OPEN channel gets NET NEGATIVE",
        "feedback and oscillates between Rntc 110k",
        "and 200k - a fracturing crimp passes",
        "through that window. R410 = 10k is the",
        "open channel's ONLY positive path.",
    ])

    for ref, code in LCSC.items():
        sh.sch.components.get(ref).set_property("LCSC", code)
    # Units 2-4 are still under their temporary refs, so the loop above missed
    # them: give every instance the same identity fields, then merge the refs.
    for c in units:
        c.set_property("LCSC", LCSC["U401"])
    _merge_units(units, "U401")
    return sh


def main(argv=None) -> int:
    # Default out dir is kicad/, and project=False: the ROOT generator owns
    # <root>.kicad_pro and this sheet must never write one.
    out_dir = Path(argv[0]) if argv else BOARD / "kicad"
    try:
        sh = build()
        path = sh.save(out_dir, project=False)
    except Exception as exc:  # noqa: BLE001  (SPEC 6: any error -> exit 2)
        print(json.dumps({"script": "gen.thermal", "status": "error",
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 2
    print(json.dumps({
        "script": "gen.thermal", "status": "pass",
        "sheet": str(path),
        "components": len(list(sh.sch.components)),
        "hier_pins": sorted(sh.hier_pins),
        "decoupling_associations": len(sh.decoupling),
        "place_report": sh.place_report,
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
