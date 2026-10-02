# PCB-0017-A stereo-class-d-amp vs a published reference design

Same brief as a published 44 x 34 mm reference design: TPA311x stereo class-D amp on one 12 V supply, stereo in and
out, SMD only, 2 layers, as small as possible. The reference design's numbers are from JLCPCB's write-up
(https://jlcpcb.com/blog/gpt-6-astra-pcb-design-in-kicad ; research/refdesign-amp.md, "the reference design's board as reported").

| | Reference (reported) | hwde, PCB-0017 rev A |
|---|---|---|
| Board size | 44 x 34 mm (1496 mm2) | 53.6 x 36.8 mm (1972 mm2, +32 %) |
| Layers | 2 | 2 (1.6 mm, 2 oz) |
| Footprints | 45 | 44 |
| Fitted (BOM) parts | 40 | 39 (J1-J4 and TP1 are bare wire pads, as in the reference design's) |
| Amplifier | TPA3116D2 | TPA3118D2 (same die family, thermal pad down) |
| ERC | 0 | 0 errors, 0 warnings |
| DRC | 0 violations, 0 unconnected | 0 violations, 0 unconnected (all severities) |
| JLCPCB DFM | not reported | pass, 0 findings |
| Deeper checks (current, return path, thermal) | not reported | 8 findings, all proposed as waivers for the owner (below) |
| Fabricated / measured | no | no (fab package only, nothing ordered) |

## Where we deviate, and why

- **Bigger board.** We put heat and decoupling first. The pad-down TPA3118D2 dumps its heat through
  the exposed pad into the copper around it, so I kept a clear 25 x 25 mm GND area around U1 on both
  layers and the PVCC decouplers tight to their pins. The 7.3 mm, 10 uH inductors need a 9.6 mm column
  pitch, and the 3 x 6 mm speaker wire pads take their own column. Closing the last ~9 mm would mean
  smaller inductors (lower saturation current) or smaller wire pads, so I left it.
- **TPA3118D2, not TPA3116D2.** The TPA3116D2 only ships pad-up (DAD), which needs a heatsink bolted
  on top. The TPA3118D2 is the pad-down (DAP) sibling and sinks into the board, which is what a
  small 2-layer SMD-only board needs.
- **Added D1, an SMBJ15A TVS across the 12 V input,** and rated the bulk caps at 35 V (polymer C13,
  low-ESR C14) for hot-plug ringing. The reference design's list has no input protection.
- **1 uF input caps** instead of 2.2 uF: against the chip's input impedance the high-pass corner
  stays at a few hertz, well below the audio band, and the part is a cheaper basic X7R.
- The reference design's damping branch (3.3 ohm + 10 nF per channel) and 680 nF filter caps are kept.

## What neither board has proven

Neither board has been built. The reference design's write-up reported DRC/ERC-clean and nothing more. Our verify pass goes further
and flags eight things: the thermal-copper check, whose 2-layer model can't show 1.5 W fitting under 85 C
on any pour, six pad-width links at U1's 0.65 mm pins that fall below the IPC-2152 current width, and one
GND pour neck on F.Cu. I think all eight are artefacts of the checks rather than defects, and each is
written up as a proposed waiver in reports/verify-waivers.proposed.json for the owner to accept or refuse.
The thermal case rests on TI's measured 22 C/W on its 2-layer EVM; a fresh-context review of our layout
put the first layout at 35-40 C/W, mostly because U1's pad had only nine thermal vias. U1 now has a
4 x 4 array of sixteen, which I estimate brings it to about 27-32 C/W, so the chip sits near 85 C at the
1.5 W design point and 40 C ambient, inside its 125 C limit. The review also asked for bootstrap caps C16 and C17 to sit closer to
U1, and they now sit about 4.7 mm from their pins instead of 9. To make room, C15 moved out to about
4.5 mm from its pin, and the 1 nF and 100 nF supply caps C7 and C9 moved just south of U1.
The real test of both boards is a sustained 4-ohm run on the bench.
