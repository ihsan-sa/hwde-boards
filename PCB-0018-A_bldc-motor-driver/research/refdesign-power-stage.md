# refdesign-power-stage — 3-phase power stage (6x half-bridge, bootstrap gate drive, low-side shunts)

Block: 6 N-FET half-bridges + bootstrap gate drive + 3 low-side shunts with Kelvin
sensing into CSAs. Board context: VM 10-28V (40V FET rating), 10A RMS/phase
continuous, 20A peak, 4-layer, no heatsink, single-sided SMD, 60mm-ish target.

Primary source used for cross-check on most decisions: TI **TIDA-010251**,
"18-V, 600-W BLDC Motor Inverter Reference Design" (design guide TIDUF36A,
DRV8328C driver + CSD18510Q5B FETs, 4-layer 2oz, 60x60mm, no heatsink,
20kHz, sensored trapezoidal) — closest available match to this block's
electrical class and thermal constraint (also no-heatsink). PDF:
https://www.ti.com/lit/ug/tiduf36a/tiduf36a.pdf

Secondary sources: TI **DRV8300 family datasheet/EVM guide** (SLVUBV6,
https://www.ti.com/lit/pdf/slvubv6 ; datasheet https://www.ti.com/lit/ds/symlink/drv8300.pdf),
ST **B-G431B-ESC1** (L6387 driver, community-derived values, no full schematic
PDF found — used only for divider/shunt cross-check), **VESC** power-stage
schematic (https://www.vesc-project.com/sites/default/files/imce/u6405/power%20stage.pdf,
DRV8305-based), and general gate-driver app notes for the pull-down rationale.

## Decisions

1. **Gate resistor: ~10 Ω series, single resistor (no separate turn-off diode
   needed for this driver class).** TIDA-010251 captured its switching
   waveforms "with a 10-Ω gate resistor for each FET" and reports clean
   switching, no overvoltage ringing (Sec 4.4.2). VESC-class designs
   independently converge on 5-10 Ω (calc: 10V/(10Ω+2Ω internal)=0.83A sink).
   TI's DRV8300 EVM guide notes a turn-off diode+resistor in parallel with
   the gate resistor is only needed *if stronger sink current is required*
   — not the default. Decision: single ~10 Ω gate resistor per FET gate as
   the default; a parallel turn-off diode is an option to hold in reserve if
   the schematic agent's loss/ringing budget needs faster turn-off, not a
   baseline requirement.
   Source: TIDA-010251 §3.1/§4.4.2 (TIDUF36A); DRV8300xxx-EVM guide (SLVUBV6).

2. **Bootstrap cap: 1 µF, ≥25-50 V X5R/X7R ceramic per phase, integrated
   bootstrap diode (no external boot diode) if the chosen driver has one.**
   TIDA-010251 uses 1 µF/50 V ceramic bootstrap caps (C4/C9/C13) with
   DRV8328's integrated bootstrap diode + trickle charge pump for 100% duty
   support. TI's DRV8329 datasheet independently recommends the same 1 µF/25V
   X5R/X7R value for its bootstrap caps. Decision: 1 µF ceramic per high-side
   bootstrap as the default; VESC's 2.2 µF + 220 pF split (higher-current,
   different driver) is a fallback only if the chosen driver's UVLO margin
   analysis calls for more charge reserve.
   Source: TIDA-010251 §3.2 Fig 3-2 (TIDUF36A); DRV8329 datasheet.

3. **Gate pull-down: ~10 kΩ gate-source resistor recommended as a safety
   default even when the driver has one internally**, to hold the FET off
   during MCU reset/power-up/fault when the driver output is high-Z —
   without it, Miller coupling from the switching node can pull the gate
   above Vth and cause shoot-through/thermal runaway. This is general
   gate-driver practice (not TIDA-specific — TIDA's schematic did not show
   a value I could read from the figure) — **marked as an opinion/common
   practice, not a single load-bearing citation**; cross-checked against two
   independent gate-driver design-note sources during research but not a
   vendor reference-design measurement.
   Source: general gate-driver design notes (opinion — confirm against the
   chosen driver IC's datasheet for whether one is already internal).

4. **Shunt + Kelvin sensing**: low-side shunt, Kelvin-routed (sense traces
   tapped directly at the resistor's own pads, not board GND). TI's DRV8300
   EVM guide is explicit: "the IN- input should be connected to GND at the
   low-side of the shunt resistor R3, not directly connected to GND" — a
   true 4-terminal Kelvin tap. Value: VESC-class designs at higher current
   (30A peak) use 10 mΩ/1W (1206); ST's B-G431B-ESC1 (comparable ~20-40A
   class) uses 3 mΩ with PGA gain 16. For this board's 10A RMS/20A peak,
   scale toward 3-5 mΩ, ≥1 W (2W preferred, no-heatsink board) to keep shunt
   dissipation and CSA input offset error both manageable — exact value is
   a P2/P3 part-selection call against the chosen CSA's input offset spec.
   Source: DRV8300xxx-EVM guide (SLVUBV6) for Kelvin routing; VESC power
   stage schematic and B-G431B-ESC1 community teardown for shunt value
   cross-check (two independent designs, same order of magnitude).

5. **CSA filter RC and placement**: small RC low-pass directly at the CSA's
   sense-input pins, placed as close to the shunt/CSA as possible — TIDA's
   schematic shows a filter resistor + ceramic cap (R29 + C40, low-hundreds
   of Ω / ~1 nF order, read off Fig 3-1) right at the op-amp's sense input,
   ahead of the ADC. Decision: RC filter belongs at the sense-amp input, not
   mid-trace, to reject switching-edge coupling without adding sense delay
   that matters at 20-30 kHz.
   Source: TIDA-010251 Fig 3-1 (TIDUF36A) — single-source for exact placement,
   consistent with standard CSA app-note guidance in general.

6. **Phase/bus voltage divider ratio ~1:10 to 1:11, with a small ceramic
   filter cap at the ADC tap.** TIDA-010251's bus-voltage divider is
   1.00 MΩ (top) / 100 kΩ (bottom) with a 0.1 µF filter cap at the tap
   (Fig 3-5) — ratio ≈1/11. ST's B-G431B-ESC1 bus-sense divider is
   18k/(18k+169k) ≈ 1/10.4. Two independent designs converge on ~1:10-11.
   For this board's 40 V max rail into a 3.3 V ADC, a ~1:11-1:13 divider
   with high-value (100k-1M range) resistors keeps quiescent loss low.
   Source: TIDA-010251 Fig 3-5 (TIDUF36A); B-G431B-ESC1 (community-derived
   gain figures — cross-checked, no full schematic PDF located).

7. **Bulk + per-leg ceramic bypass**: bulk cap(s) at the VM input; separate
   local ceramic decoupling directly across each half-bridge leg (VDC to
   the bottom FET's source), sized to damp ringing from the shunt's and
   power track's parasitic inductance — not just one bulk cap for the whole
   board. TIDA-010251 explicitly calls these out as C30/C31/C32, one per
   leg, describing their purpose as reducing supply-line ringing caused by
   parasitic inductance added by the sense resistor and power track.
   Source: TIDA-010251 §3.1 (TIDUF36A).

8. **Snubber is conditional, not universal.** TIDA-010251: an RC snubber
   footprint is provided across all FETs, but "a snubber is not necessarily
   required across all the FETs" — need depends on current direction, PWM
   strategy and diode reverse-recovery-driven VDS ringing (worse with
   bipolar/complementary switching than pure trapezoidal). Where used,
   snubber cap ≈ several x Coss (TIDA used ~832 pF), snubber resistor value
   tuned empirically on the bench, not calculated a priori.
   Source: TIDA-010251 §3.1 (TIDUF36A).

9. **Thermal: no-heatsink, 4-layer/2oz copper reference point directly
   applicable.** TIDA-010251 is also a no-heatsink, natural-convection,
   4-layer 2oz-copper, ~60x60mm design — same constraints as this block.
   Its measured data: at 10 A RMS/phase (this board's continuous rating),
   max FET temp was 49.3°C (15% duty cycle test, board ambient not stated
   but lab-room); at 33 A RMS, max FET temp reached 97.1°C. This is a
   directly load-bearing data point for the thermal-derating flag already
   raised in requirements.md §4/§8 (Q3): 10 A RMS with no heatsink on 2oz
   4-layer copper is plausible but runs FETs meaningfully warm, and should
   be re-checked once the actual FET Rds(on)/package is chosen (TIDA used
   a 0.79 mΩ SON5x6 FET — a comparably low-Rds(on) part is needed to hit
   similar numbers).
   Source: TIDA-010251 §4.4.1/§4.4.4, Fig 4-9..4-12 (TIDUF36A).

## Layout notes (flag for interface-spec)
- Kelvin-tap the shunt at its own pads, not at board GND (DRV8300 EVM
  guide) — this is a routing constraint, not just a schematic net.
- Per-leg local decoupling cap placed at the bottom FET's source/VDC,
  as close as possible, to minimize the shunt+track parasitic-inductance
  ringing loop (TIDA §3.1).
- CSA/op-amp RC filter placed at the amplifier's sense-input pins, not
  mid-trace between shunt and amplifier.

## Errata / footguns
- DRV8300 family: DRV8300D has an *integrated* bootstrap diode; the
  DRV8300N variant needs an *external* bootstrap diode — part-suffix
  dependent, worth checking explicitly at part-selection time if a DRV8300
  variant is chosen (source: TI DRV8300 datasheet, via search-result
  summary — not independently PDF-verified this run, flagged as lower
  confidence).
- Snubber footprint should be optional/populate-as-needed, not fixed —
  TIDA's own text says it isn't required on every leg; over-fitting a
  fixed RC across all six switches by default is not what the reference
  design does.

## Not resolved this run
- Exact gate pull-down value used by TIDA (figure resolution too low to
  read reliably) — item 3 above is marked opinion/general-practice, not a
  TIDA-cited number.
- No full schematic PDF was found for ST B-G431B-ESC1 or the VESC-project
  board within budget; values used from those are community-reported
  numbers, treated as secondary/cross-check only, not primary citations.
