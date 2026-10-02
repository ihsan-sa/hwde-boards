# PCB-0018-A bldc-motor-driver — requirements

## 1. Function

A three-phase BLDC/PMSM motor driver board, designed from a general spec and
informed by one frame of a published 3-phase motor-driver demo board (no spec was
published). It drives a 3-phase motor via six N-channel MOSFET half-bridges
with a gate driver, senses per-phase current via low-side shunts and phase/
bus voltage via dividers, and closes the control loop on an onboard MCU
(sensored or sensorless FOC). It exposes control I/O (UART/CAN or step/PWM),
a Hall/encoder connector, SWD programming, two buttons, and status LEDs. No
mode token is present in the brief; this is a normal (non-mode) run, scope
and binding are the default P5 board_init flow, size is stated as a target
with an explicit "size is an output" note (see Section 5).

## 2. Interfaces

- **Motor phase outputs**: PHASE A/B/C, large plated pads (wire solder or
  screw lugs), rated to the 20 A peak power spec. ASSUMED: pad-only, no
  connector shell (frame shows bare pads, not a housed connector).
- **Power input**: VM + GND, large plated pads (same pad group as phase
  outputs going by the frame's TP1-TP5 layout). ASSUMED: pad-only, no
  connector shell.
- **Control connector**: small JST-style connector. ASSUMED signal set:
  UART (TX/RX) or CAN, plus a power/GND pair — exact protocol is an open
  question (Q1).
- **Hall/encoder connector**: wider white connector (FFC or header).
  ASSUMED pinout: 5V, GND, H1-H3 (or A/B/Z quadrature) — exact pin count/
  pitch is an open question (Q2).
- **Programming**: SWD (2-4 pin header or pads), not visible as a distinct
  connector in the frame — ASSUMED present per brief text.
- **User I/O**: two tactile switches (SW1 reset, SW2 user), status LED(s)
  (not clearly resolved in the frame; ASSUMED at least 1 status LED near
  the MCU).
- **Test points**: TP1-TP5, large plated pads read as VM, GND, and the
  three phase outputs (test/probe access, not a load-bearing connector).

## 3. Power

- **Input rail VM**: PROVISIONAL 12-24 V nominal, 10-28 V operating range,
  power stage rated to 40 V. These current/voltage figures are the
  orchestrator's provisional answers, not this analyst's guesses — see
  Section 8 (safety flags) and Q3/Q4 for confirmation.
- **Protection**: reverse-polarity and transient (TVS) protection on VM.
  ASSUMED needed given "motor supply, external wiring" context; not
  confirmed by the frame.
- **Onboard rails**: buck VM -> 3.3V (L1/BUCK_SW net visible in frame) for
  MCU + digital sensors. A separate gate-drive rail (>=10V VGS, independent
  of VM if VM can sag below 10V) is required — GUESS: rail voltage and
  whether it's a dedicated regulator or bootstrap-only is an open question
  (Q5).
- **Rail budget**: not computed at this stage (P0); flagged for P2/P3
  power-tree design. GUESS budget only: MCU + gate driver + sense amps +
  LEDs, low tens of mA on 3V3, gate-drive rail sized to switching losses
  at 20-30 kHz.
- **Battery/charging**: none. This is a bench/system supply-fed motor
  driver, not a battery-powered device (frame shows no charge IC or
  battery connector).

## 4. Environment

Not stated in the brief or resolvable from the frame. ASSUMED (low risk,
default): indoor/lab use, 0-40C ambient, no enclosure, no IP rating, no
vibration spec — this is a demo/prototype driver board, not a certified
product. Thermal: no heatsink assumed per brief ("without a heatsink" is
the stated target condition), so thermal derating from the 6 power FETs
and shunts is a P2/P6 design concern, not a requirement input here.

## 5. Size & mounting

- Target outline: approximately 60mm x 60mm or smaller, roughly square,
  matching the frame's proportions. Per the brief, **size is explicitly an
  output, not an input**: "Correctness first ... then size." This is a
  RELAXABLE preference, not a HARD cap — no HARD cap is set. The frame's
  own board is a plausible upper bound but is not to be treated as binding;
  placement should optimize for the electrical/thermal correctness items
  first (gate-drive loop, Kelvin shunt sensing, commutation loop, thermal)
  and let final size follow.
- Mounting holes: 8 holes visible in the frame (H1-H10 labels seen, several
  are likely test points not holes — frame shows large filled circles at
  roughly the 4 corners plus 4 edge-midpoints = up to 8 mounting holes).
  ASSUMED: standard M3 mounting holes, corner + edge pattern, exact count
  and diameter TBD at layout (P5) — not a hard requirement to pin down at
  P0.
- Height limit: none stated; no enclosure implied. The single large
  electrolytic capacitor is the tallest component visible; no clearance
  constraint given.
- Layer count: 4 layers, stated directly in the brief (HARD — this is a
  stated spec, not geometry-under-optimization).

## 6. Quantity & budget

Not stated in the brief. ASSUMED (default, low risk): prototype quantity,
1-5 boards, no target unit cost set — this is a reverse-engineering/demo
exercise, not a cost-optimized production run. Open question Q6 offers a
default.

## 7. Assembly

JLC PCBA, SMD assembly, THT only where a connector or the electrolytic
capacitor needs it (stated directly in the brief). Single-sided placement
of fine-pitch parts assumed typical (double-sided PCBA not called out;
ASSUMED single-sided SMD placement, with THT parts on the primary side)
— open question Q7 offers a default.

## 8. Compliance/safety flags

This board triggers multiple safety-relevant flags. Per the pipeline rule,
none of these are guessed — they are recorded as open questions or as
PROVISIONAL values pending orchestrator/owner confirmation:

- **Motor drive**: yes — 3-phase BLDC/PMSM motor driver, spinning mass
  hazard under fault or miswiring.
- **High current (>3 A)**: yes — PROVISIONAL 10 A RMS per phase continuous,
  20 A peak (orchestrator-provided, not this analyst's guess). This is a
  hard-confirm item: see Q3.
  Bulk-cap derating (P4, 2026-09-27): bus-cap RMS ripple is ~0.5-0.6x phase
  RMS, so 10 A/phase puts 5-6 A into the bus caps and most of it into the
  electrolytics at 20 kHz. Two 470 uF/63 V cans (C101, C104) share it, but
  each is rated about 1-2 A (a guess: the part's datasheet was not
  available), so 10 A continuous is above what they are rated for. Raising
  PWM toward 40 kHz moves ripple into the MLCC bank. The P8 thermal check
  must state the continuous rating the caps allow.
- **Voltage up to 28 V**: yes — PROVISIONAL VM 10-28 V operating, 40 V
  power-stage rating (orchestrator-provided). Not mains voltage (<50V), so
  no mains isolation/creepage-for-mains requirement applies, but 28 V at
  20 A peak still needs reverse-polarity, TVS, and fusing/PTC
  consideration. See Q4.
- **Batteries**: no battery on this board (see Section 3).
- **RF transmit**: none identified in the frame or brief.
- **Mains voltage**: no — confirmed not applicable (VM is a low-voltage DC
  supply rail, not mains-connected).

## Assumptions inferred from the reference frame

Every item here comes from one frame of the reference video or is our own guess, not a published spec.
Research with a source overrides a frame guess (see research/reference-video.md); the comparison is
judged against this list.

- A1 Topology: three half-bridges of N-FETs (Q1-Q6), low-side shunts per phase (SHUNT A/B/C). Frame.
- A2 Supply: one VM rail with a large electrolytic; 12-24 V nominal, 10-28 V operating. Guess (no rating visible).
- A3 Power stage rating: 60 V FETs (ours; the frame suggested 40 V class, raised for TVS clamp margin). Guess.
- A4 Phase current: 10 A RMS continuous, 20 A peak, no heatsink. Guess, from the FET package size.
- A5 Logic rail: a buck to 3.3 V (L1, BUCK_SW, V3V3 are visible). Frame; our tree adds 5 V and a gate rail.
- A6 MCU: a QFP of about 48-64 pins; we chose STM32G4. Frame (package) + guess (family).
- A7 Gate driver and current-sense amps: some of U1-U10 (SOIC/TSSOP). Frame (packages) + guess (roles).
- A8 Control I/O: a small JST connector (we made it UART) and a wider connector (we made it Hall + ABZ). Guess.
- A9 Power/motor connections: TP1-TP5 read as VM, GND, A, B, C wire pads. Guess.
- A10 User I/O: two tactile switches (SW1/SW2, we made them reset + user), status LEDs. Frame + guess.
- A11 Stack-up: 4 layers. Frame (inner-plane look), unconfirmed.
- A12 Size: roughly square, about 60 x 60 mm; mounting holes H1-H10 visible, we use four M3. Frame + guess.

## 9. Open questions

1. What protocol does the small JST-style control connector carry — UART,
   CAN, or step/direction + PWM/enable? DEFAULT: UART (simplest, matches a
   single small connector with few pins) at 3.3V logic levels.
2. What is the Hall/encoder connector's exact pinout and pin count — 5V,
   GND, H1-H3 (3 Hall sensors) vs. A/B/Z quadrature encoder? DEFAULT: 5-pin,
   5V + GND + H1-H3 (three Hall-effect sensor inputs), matching "sensored"
   BLDC commutation, the simpler and more common case for a demo board.
3. Confirm the PROVISIONAL current rating: 10 A RMS per phase continuous
   (no heatsink, 25C ambient), 20 A peak. DEFAULT: accept as stated
   (orchestrator-provided); flagged here only because Section 8 requires
   every safety-relevant value to be explicitly confirmed, not assumed.
4. Confirm the PROVISIONAL voltage rating: VM 10-28 V operating (12-24 V
   nominal), 40 V-rated power stage. DEFAULT: accept as stated
   (orchestrator-provided); same confirm-not-guess reasoning as Q3.
5. Does the gate-drive rail need its own regulator (independent of VM), or
   is bootstrap-only sufficient across the full 10-28 V VM range? DEFAULT:
   bootstrap-only for the high sides (standard for this VM range with a
   modern 3-phase gate driver IC), with the driver's own internal VCC/VGS
   rail generated from VM or 3V3 as the driver IC requires — final choice
   deferred to P2 part selection, not a P0 blocker.
6. Build quantity and target unit cost? DEFAULT: prototype run, 3-5 boards,
   no target unit cost (this is a reverse-engineering exercise, not a
   cost-optimized product).
7. Single-sided or double-sided SMD placement? DEFAULT: single-sided SMD
   (all fine-pitch parts on top), THT (electrolytic, connectors) also on
   top — simplest and cheapest JLCPCB PCBA option, matches "SMD assembly
   at JLCPCB" in the brief with no double-sided call-out.
8. Exact mounting hole count, pattern, and size? DEFAULT: 4 corner holes,
   M3, matching the frame's visible corner pads — remaining edge marks in
   the frame (H5-H10-style labels) are read as test points/silkscreen
   refs, not additional mounting holes, pending layout-stage (P5)
   confirmation.

## Answers (orchestrator as delegate, unattended run, 2026-09-27)
1. Control connector: UART (3.3 V logic) on a 4-pin JST-GH: GND, 5V out(fused/limited), TX, RX. Accepted default.
2. Sensor connector: the wider connector is 8-pin: 5V, GND, HA, HB, HC, ENC_A, ENC_B, ENC_Z (Hall and ABZ both
   supported, 5 V-tolerant inputs with pull-ups). Changed from the 5-pin default so both sensor types work.
3. Current 10 A RMS/phase continuous, 20 A peak: PROVISIONAL; the thermal estimate at P2/P8 may derate it and must say so.
4. VM 10-28 V operating (12-24 V nominal), 40 V FETs: PROVISIONAL.
5. Gate drive: the architect picks it, but the requirement is VGS >= 8 V at VM = 10 V and within the driver's and
   FETs' absolute max at VM = 28 V + transient; a separate gate-drive rail if the driver cannot take VM directly.
6. Quantity 5, prototype, no unit-cost target (owner: "it needs to be good").
7. Single-sided SMD on top; THT only for the electrolytic/connectors if unavoidable.
8. Four M3 corner holes. SWD on a 1.27 mm 2x5 (or Tag-Connect footprint) header; the architect chooses.

## High-voltage clearance scope (owner, 2026-09-28)
The gate, boot, phase and VM nets keep 0.4 mm (up to 45-50 V) or 0.5 mm (57 V boot/gate) to other copper, with two exceptions,
written into the `.kicad_dru` as `hv_scope_*` rules:
1. Nets of one phase leg (GHx, BSTx, PHASE_x, GLx, LS_SRC_x and the gate-resistor nets of that leg) use the normal 0.13 mm
   between each other. Tracks sit under solder mask, and IPC-2221B Table 6-1 B4 (coated external conductors) allows 0.13 mm up to 100 V.
2. Inside the gate driver's (U301) courtyard, pad-to-pad and pad-to-track drop to the package's own pitch, floor 0.13 mm:
   IPC-2221B A6 (external component terminations) allows 0.13 mm for 31-100 V, and the DRV8300 is rated for these pins at this pitch.
   The same rule covers the VM_IN ideal-diode controller's (U101, SOT-23-8, 0.65 mm pitch) courtyard: IPC-2221B Table 6-1 A6
   (component leads, up to 100 V) applies, VM_IN is a 60 V-class rail, and U101 is rated for it at this pitch.
The routers take one clearance per net, so they keep the full value; the gate-driver escapes are hand-routed.
