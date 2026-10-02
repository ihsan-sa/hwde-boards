# PCB-0018-A bldc-motor-driver — brief

Owner brief (2026-09-27): "also do a three phase motor driver". The reference is
a published demo board seen in a 15-second video; frame: `reference-video-frame.png` (owner's screenshot).
No spec was published, so the spec below is designed from a general brief and informed by that frame. Every
line marked (guess) is our own inference, not a published fact.

## What the frame shows
- Three half-bridges, Q1-Q6, in 5x6-class power packages; low-side shunts labelled SHUNT A/B/C.
- A VM power rail with one large electrolytic (C11 area), VM and GND pour islands, wire pads/test points TP1-TP5
  on the edges (large plated pads: we read them as VM, GND and the three phase outputs).
- A QFP MCU (~48-64 pins) in the middle, a buck to V3V3 (L1, BUCK_SW net), several SOIC/TSSOP ICs (U1-U10:
  gate driver, current-sense amps, regulators), two tactile switches SW1/SW2, a small JST-style connector and a
  wider white connector (FFC/header), mounting holes, many small diodes (D10-D23), roughly square, 4 layers.

## Spec (ours)
- Motor: 3-phase BLDC/PMSM, sensored or sensorless FOC. (guess)
- Supply VM: 12-24 V nominal, 10-28 V operating, 40 V-rated power stage, reverse-polarity and transient
  protection on VM (TVS). (guess)
- Current: 10 A RMS per phase continuous at 25 C ambient without a heatsink is the target, 20 A peak; derate
  shown by a thermal estimate. (guess)
- Power stage: 6 N-channel MOSFETs, 40 V, low Rds(on), 5x6 mm power packages; bootstrapped high side.
  PWM 20-30 kHz. Dead time set in hardware or the MCU.
- Gate drive: a 3-phase or 3x half-bridge gate driver with bootstrap, at >= 10 V VGS across the whole VM range
  (a gate-drive rail independent of VM if needed); gate resistors, turn-off path, and pull-downs so FETs stay
  off with the MCU in reset.
- Current sensing: three low-side shunts with Kelvin (4-wire) connections to differential current-sense
  amplifiers, filtered into the MCU's ADCs; overcurrent comparator/fault to the timer break input.
- Voltage sensing: VM divider and three phase-voltage dividers (BEMF) to MCU ADCs; an NTC at the power stage.
- MCU: STM32G4 (motor-control timers, fast ADCs), LQFP-48 or -64. (guess: G431/G474 class)
- Power: buck VM -> 3.3 V (and whatever the gate driver needs), rated for the MCU + sensors + headroom.
- I/O: a small JST connector for control (UART/CAN or PWM/step input, guess), a wider connector for Hall/encoder
  (5 V, GND, H1-H3 / A-B-Z), SWD programming, two buttons (reset + user), status LEDs.
- Motor and power: VM, GND, PHASE A/B/C on large plated pads (wire solder or screw lugs).
- 4-layer, SMD assembly at JLCPCB (THT only where a connector or the electrolytic needs it), silkscreen
  "PCB-0018 REV A".
- Correctness first: gate-drive loop, shunt Kelvin sensing, power commutation loop, thermal — then size. Size is an
  output: aim for about 60 x 60 mm or smaller, roughly square like the reference board.
- Stop at a DRC/ERC-clean fab package. Do NOT order. End with COMPARISON.md against what the video frame shows.
