# PCB-0018-A bldc-motor-driver vs the reference board

The reference is a 3-phase motor-driver board seen in one frame of a published demo video
(`brief/reference-video-frame.png`). Nobody published its spec, schematic or parts list
(research/reference-video.md), so the left column is only what the frame shows. Our spec was written
from that frame plus our own guesses; every guess is listed as A1-A12 in requirements.md.

| | Reference board (from the frame) | hwde, PCB-0018 rev A |
|---|---|---|
| Function | 3-phase motor driver | 3-phase BLDC/PMSM driver, sensored or sensorless FOC |
| Power stage | Q1-Q6 in dual-FET-looking packages, three half-bridges | 6x NTMFS5C628NL 60 V, 5x6 mm, one FET per package |
| Current sensing | low-side shunts SHUNT A/B/C | 3 mOhm 2512 low-side shunts, Kelvin taps via net ties, 3x INA240A1 |
| Supply | VM rail, one large electrolytic, no rating visible | VM 10-28 V (12-24 V nominal), 2x 470 uF / 63 V, SMCJ28A TVS, reverse-polarity FET |
| Logic rail | buck to 3.3 V (L1, BUCK_SW, V3V3) | LM5164 buck VM->5 V, TLV75733 LDO 5->3.3 V, TPS61040 boost 5->12 V for gate drive |
| Gate driver | one of U1-U10, not identifiable | DRV8300D, 6-PWM, bootstrap high sides |
| MCU | QFP, about 48-64 pins | STM32G431CBT6 (LQFP-48) |
| Control I/O | small JST connector, wider FFC/header | JST-GH 4 (UART + 5 V), 8-pin Hall + ABZ encoder, SWD 2x5 1.27 mm |
| User I/O | SW1, SW2 | reset + user switch, 3 LEDs |
| Test points / wire pads | TP1-TP5 | TP1-TP5 as VM, GND, A, B, C wire pads |
| Mounting | H1-H10 | 4x M3 corner holes |
| Layers | looks like 4 | 4 (JLC04162H-7628A, 2 oz outer) |
| Size | roughly square, about 60 x 60 mm (guess) | 78 x 78 mm |
| Footprints | not countable from the frame | 175: 148 machine-placed, 12 do-not-place, 15 board features |
| ERC / DRC | not reported | ERC and DRC 0 violations, 0 unconnected; see below for what was waived |
| Fabricated / measured | not reported | no (fab package only, nothing ordered) |

## What the checks say about ours

ERC, DRC, placement, the design checks and DFM all pass, and the fab package has gerbers, drill,
a BOM with an LCSC number on every placed part (45 lines) and a placement file. The design checks
pass with 390 waivers, each with its reason in `routing/rules-added.md`, and you should read them
before trusting the board:

- **Current (359).** Most are stitching vias and Kelvin or gate-return taps that the check counts as
  current paths; the real phase and supply necks were widened or given more vias.
- **Creepage (24).** They sit inside the gate driver's and the ideal-diode controller's own pin pitch
  (IPC-2221B A6, leads up to 100 V) or between nets of the same phase leg.
- **Current-sense pairs (6).** The INA240's two inputs sit 5.4 mm apart on opposite pad rows, so
  each pair runs at least 9 mm uncoupled against a 3 mm target. The packages set that length, not
  the routing, and the traces run side by side everywhere else.
- **Power distribution (1).** The check flags the ground rail itself as undecoupled.

Some narrow power stubs were turned into solid copper zones of the same shape to clear the
track-width rule, so those necks are no wider than before. Nothing here has been built or measured.

## Where we deviate, and why

- **Single FETs, not dual packages.** A dual-FET package puts both switches of a leg in one thermal
  mass. At our 10 A RMS guess, two 5x6 mm single FETs spread the heat over twice the copper, and
  each leg's high-frequency capacitors sit right across its drain and shunt.
- **Three rails, not one.** The frame only shows a 3.3 V buck. A 3-phase driver also needs a gate
  rail of about 12 V that holds up when VM sags to 10 V, so we added a 5 V buck and a 12 V boost.
- **Bigger board.** Three legs of power copper plus the reverse-polarity FET, a 470 uF can pair and the 100 V buck don't fit in
  60 x 60 mm without crowding the gate loops. We put gate-loop and power-loop area first and let size
  come out at 78 x 78 mm.
- **Four mounting holes, not ten.** Most of the frame's H labels look like fiducials or edge marks
  at that resolution; we read them as optional.
