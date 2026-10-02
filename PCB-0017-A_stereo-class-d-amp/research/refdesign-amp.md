# Reference design decisions - block "amp" (TPA3116D2 stereo class-D)

IC is fixed by the brief: TI TPA3116D2 (32-pin HTSSOP with PowerPAD, "DAD" package). No
shortlist to reconcile against.

Sources:
- [S1] TI datasheet SLOS708G, "TPA3116D2, TPA3118D2, TPA3130D2" -
  https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf
- [S2] TI EVM user's guide SLOU336B, "TPA3116D2EVM" -
  https://www.ti.com/lit/ug/slou336b/slou336b.pdf
- [S3] TI app report SLAA701B (current revision of the note historically numbered SLOA119),
  "Class-D LC Filter Design" - https://www.ti.com/lit/an/sloa119b/sloa119b.pdf
- [S4] TI app report SLMA002H, "PowerPAD Thermally Enhanced Package" -
  https://www.ti.com/lit/an/slma002h/slma002h.pdf
- [S5] JLCPCB blog, published write-up of a 44 x 34 mm TPA3116D2 reference design -
  https://jlcpcb.com/blog/gpt-6-astra-pcb-design-in-kicad

## Decisions

1. **Gain / GAIN-SLV divider.** GAIN/SLV pin (8) is an 8-level ADC input; Master mode, 20 dB
   gain = R-to-GND 5.6 kOhm, R-to-GVDD OPEN; input impedance 60 kOhm at that setting [S1 Table 1,
   Fig 27]. The reference design's reported "5.6k/100k" is **not** this divider - see decision 7. The reference design
   runs 20 dB gain, matching the requirements' default (Q12).
2. **Input AC-coupling cap.** With Zi=60 kOhm (20 dB), the datasheet's own recommended cap for a
   flat 20 Hz bass response is 1.5 uF (1.8 Hz corner) [S1 Table 2]; a 10x smaller cap (~0.15 uF)
   is the -3dB-at-20Hz alternative. The reference design's 2.2 uF (per requirements.md) gives f=1/(2*pi*60k*2.2u)
   ~= 1.2 Hz - deeper bass than the datasheet's own 20 dB recommendation, not undersized. Input
   cap should be a low-leakage type (ceramic X7R ok per S1 7.3.2), positive terminal toward the
   input pin if polarized.
3. **PLIMIT.** Resistor divider GVDD-to-GND sets a voltage limit; a 1 uF cap to GND at the pin is
   required for stability regardless of divider value; tie PLIMIT straight to GVDD (no divider) if
   no power limiting is wanted, which is the simplest default and is compatible with 1SPW mode
   [S1 7.3.4]. The reference write-up gives no PLIMIT value - open item for schematic (see
   OPEN).
4. **AM0/AM1/AM2 (switching-frequency select).** These are simple logic-level selects (not an ADC
   divider like GAIN/SLV) - tie each directly to GND or PVCC per Table 6 of S1 for the desired
   PWM frequency (376-1200 kHz across the 6 combinations); no resistor divider is needed on these
   three pins, unlike GAIN/SLV and PLIMIT.
5. **SDZ / FAULTZ pull-ups.** FAULTZ is open-drain; the datasheet's own VOL test condition uses
   RPULL-UP = 100 kOhm [S1 Elec Characteristics], and recommends "100 kOhm or more" for the
   GAIN/SLV- and PLIMIT-class dividers generally, for noise immunity [S1 7.3.4]. SDZ must not be
   left floating (unpredictable operation) [S1 7.3.3] - pull to PVCC/GVDD-referenced high through
   100 kOhm for always-on. This is what the reference design's "R1 and R3 at 100k" (its own designators) do per
   S5: pull up SDZ and FAULTZ, plus hold MUTE, not the gain divider. The EVM uses the same 100 kOhm
   value on 8 of its resistors (R1,R2,R7-R10,R21,R22) for this class of pull-up/pull-down [S2
   BOM].
6. **Bootstrap caps.** 220 nF, 25 V (or better), X5R, one per output (BSNL/BSPL/BSNR/BSPR), each
   returned to its own OUTxx pin, not shared [S1 8.2.2.5, pin table]. The reference design's "four 220 nF" [S5]
   matches this exactly - no deviation.
7. **Gain-divider naming vs the reference design's report - resolved, not a conflict.** S5 states "R2 at 5.6k
   selects 20 dB gain" and "R1 and R3 at 100k handle SDZ/FAULTZ pull-up and MUTE hold" using
   the reference design's own reference designators. Mapped onto the datasheet's pin function (decision 1) and
   pull-up requirement (decision 5), the reference design's 5.6k is the GAIN/SLV-to-GND leg (GVDD leg left open)
   and its 100k parts are unrelated SDZ/FAULTZ/MUTE pull-ups, not a second GAIN/SLV leg. Schematic
   phase should not read "5.6k/100k" as one divider.
8. **PVCC/AVCC/GVDD decoupling, per-group.** At each PVCC pin group (two groups, one per side of
   the 32-pin package): one 100 uF+ low-ESR bulk cap near the group, plus a mid-frequency
   100 nF-1 uF cap and a small 220 pF-1 nF high-frequency cap, both placed as close to the PVCC
   pins as possible and returned to the IC GND pad directly [S1 10.1, 8.2.2.3/.4]. AVCC (pin 17)
   gets its own local decoupling, separate from the PVCC groups [S5: "AVCC on pin 17 gets a
   separate 100 nF"]. GVDD gets a 1 uF X5R/X7R cap to GND for the internal LDO plus to filter the
   GAIN/SLV and PLIMIT dividers [S1 7.3.4, Fig 27 shows C5=1uF at GVDD]. The reference design's "100 uF + 100 nF +
   1 nF at each PVCC group" [requirements.md, S5] matches the datasheet's recommended three-tier
   scheme value-for-value (100 uF bulk, 100 nF-1uF mid, 220pF-1nF high-freq).
9. **Output LC filter, BTL, 4-8 Ohm.** Datasheet's own BTL test condition is L=10 uH, C=680 nF
   [S1 Elec Char table, RL(BTL) row] - this is also the reference design's exact pair [S5, requirements.md].
   S3's own optimized pairing for a ~73 kHz Butterworth corner is 10 uH + 470 nF, or 7 uH +
   680 nF [S3 section "Capacitance", table]; the 10 uH+680 nF pair computes to f0 ~= 61 kHz
   (1/(2*pi*sqrt(10e-6*680e-9))) - a bit below S3's optimum, trading a little bandwidth for more
   switching-ripple margin. Not wrong, just not the app-note's tightest-tuned pair; flag as a
   choice, not an error, for the schematic phase to keep or retune.
   Damping/Q is load-dependent (Q = RL*sqrt(C/L)) [S3 eq 3] - a single fixed L/C is only
   critically damped at one RL, which is why a separate damping branch (decision 10) matters when
   the load can vary between 4 and 8 Ohm (requirements Q2).
   Inductor saturation: EVM uses a 10 uH/5.8 A-rated part (Toko 931BS-100M) [S2 BOM] - use this as
   the saturation-current floor for a ~3 A-class design (requirements Q6 default).
10. **Damping/Zobel branch.** The reference design and the EVM both carry a second small RC branch per output beyond the
    main LC filter: EVM's R15-R18 = 3.3 Ohm (0603) with C25-C28 = 10 nF/100V X7R [S2 BOM] - this
    matches the reference design's reported "3.3 Ohm + 10 nF" exactly [requirements.md, S5]. This is separate
    from the datasheet's own suggested EMI snubber at the switching node itself, 18 Ohm + 330 pF
    [S1 7.3.14] - the EVM actually implements a *third* value there, 10 Ohm (R11-R14, 0805 1/4W)
    with 330 pF (C11/C13/C15/C17, COG) [S2 BOM], i.e. lower than the datasheet's own suggested
    18 Ohm. Net: two distinct RC networks per channel are defensible (switch-node snubber near the
    IC pins, and a damping/Zobel branch at the filter output); the reference design's reported parts list only
    the second one. Snubber layout must be tight, returning directly to the IC's GND pins [S1
    7.3.14].
11. **PowerPAD thermal vias.** 0.33 mm (13 mil) drill diameter or smaller, plated (not left
    unplated), 1 oz copper, tented/capped from the component side (not the opposite side - tenting
    from the far side increases reflow voiding) [S4 2.4]. No thermal-relief ("wagon wheel") via
    connections under the pad - full continuous copper connection to the plane [S4 2.4]. Via count:
    5-9 vias is adequate for a small die on 2-4 layer boards, with diminishing returns beyond that
    [S4 2.4, Fig 8/9] - S4 does not give a numeric pitch, only the diameter and the "small die -
    5 to 9" count guidance; a grid within the exposed-pad footprint, evenly spaced, is implied by
    Fig 10 but not stated as a number. JLCPCB's board reports 51 vias total at 0.30 mm [S5] across
    the whole board (not all thermal) - close to but not identical to S4's 0.33 mm recommendation;
    treat 0.3-0.33 mm plated, tented, as the interface-spec range.
12. **Thermal land / copper area.** Solder-mask-defined pad sized to the datasheet's maximum
    exposed-pad dimension [S4 2.3, note under Fig 10]; the land should be maximized within layout
    constraints and connected to as much internal/bottom copper as the 2-layer stackup allows [S4
    2.3]. S4's headline RthetaJA numbers do not apply as-is: S1's own thermal table lists
    RthetaJA=14 C/W for the TPA3116D2 DAD package, but its footnote says this was measured *with
    the EVM's attached 14x50x25 mm aluminum heat sink* [S1 6.4, footnote 4] - not copper-pour
    alone. The EVM itself also ships with that same aluminum heat sink [S2 BOM, item 29] and is
    therefore not a copper-only precedent. **Flag for schematic/layout: neither cited source
    demonstrates copper-alone cooling for this exact part; requirements.md Q8 assumes copper alone
    suffices at 8 Ohm and may not suffice at 4 Ohm continuous - this needs a thermal calc or margin
    check at H-gate, not just a via-count copy.**
13. **Layout symmetry / grounding.** OUTP/OUTN and their LC filter parts should be routed
    symmetrically with the tightest possible current loop from each output through its filter and
    back to GND, since loop area sets antenna effectiveness/EMI [S1 10.1]. Single star-ground point
    at the IC's GND pad/pins; all PVCC decoupling returns there directly [S1 10.1]. Bulk PVCC caps
    near the device on the PVCC supply; local high-frequency bypass right at the pins [S1 10.1,
    8.2.2.3].

## The reference design's board as reported

- JLCPCB's own writeup [S5] is a first-party account of the design run and is the source for
  the reference design's board specifics: 44 x 34 mm, 2 layers, 45 total footprints / 40 fitted parts (J1-J4 and
  TP1 excluded from BOM), 120 SMD pads, 51 plated 0.30 mm vias.
- Component values reported [S5]: two 100 uF/25V bulk caps; 100 nF per PVCC pair + 1 nF per PVCC
  pair + a separate 100 nF at AVCC (pin 17); four 2.2 uF X7R input caps; R(2)=5.6k for 20 dB gain,
  R1/R3=100k for SDZ/FAULTZ pull-up and MUTE hold (see decision 7 for how this maps onto the
  datasheet's own pin functions); per-channel output filter of 10 uH + 680 nF with a 3.3 Ohm +
  10 nF damping branch; four 220 nF bootstrap caps; 4 Ohm per-channel speaker load assumed.
- Process/correctness notes from S5: the first KiCad parity check found 46 issues, "mainly missing
  Manufacturer and Rating fields" plus one intentionally unconnected SYNC pin; after fixing source
  data (no exclusions added) the design reached "0 ERC and 0 DRC violations, 0 unconnected items,
  0 parity issues." S5 is explicit that **the board was never fabricated, assembled, or measured**
  - DRC/ERC-clean is a netlist/ruleset claim, not a functional or thermal claim. No reviewer
    critique of specific component choices, gain-resistor correctness, or thermal adequacy is
    reported in S5 itself.

## Layout notes (flag for interface-spec)

- Thermal land/vias: 0.30-0.33 mm plated drill, tented/capped from the component side, no
  thermal-relief connections, land sized to the datasheet max exposed-pad dimension, 5-9+ vias for
  this die size [S1, S4]. Copper-alone thermal adequacy is unverified by any cited source (see
  decision 12) - carry a margin check into schematic/layout, don't just copy a via count.
- OUTP/OUTN + LC filter: symmetric routing, minimum loop area, filter caps grounded close to the
  IC's GND pad (star point) [S1 10.1].
- Bootstrap loop: each BSTxx cap tight to its own BST pin and OUTxx pin; don't share/cross
  bootstrap return paths between channels [S1 7.3.10/pin table].
- PVCC decoupling: bulk caps per side of the package, high-freq caps at the pins themselves, all
  grounded to the IC GND directly, not through a long trace [S1 10.1].

## Errata / footguns

- SDZ must never be left floating - unpredictable operation [S1 7.3.3].
- Gain and PBTL/BTL/Master-Slave mode latch at the end of the startup cycle and cannot change
  while powered [S1 7.3.1, 7.3.3] - the divider must be right before first power-up, not
  field-adjustable.
- FAULTZ is open-drain and needs an external pull-up (not internal) [S1 pin table] - don't forget
  it or FAULTZ reads permanently low/floating.
- Thermal vias with thermal-relief (wagon-wheel) connections defeat the PowerPAD's purpose - a
  common PCB-tool default that must be turned off for this footprint [S4 2.4].
- The datasheet's headline RthetaJA=14 C/W for this exact package is heat-sink-assisted, not
  copper-pour-only [S1 6.4 footnote] - don't carry that number into a copper-only thermal claim.
