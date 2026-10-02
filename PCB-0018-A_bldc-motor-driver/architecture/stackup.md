# stackup (P2)

**JLC04162H-7628A** - 4 layers, 1.6 mm, 2 oz outer / 0.5 oz inner, HASL (stackups.yaml, available: true).

Class: 4L (the brief states 4 layers; the design also needs it).

Why 4 layers: an unbroken GND plane directly under the power stage and the Kelvin/CSA routing (In1), a VM plane
(In2) that carries part of the bus current and gives the per-leg MLCCs a short commutation loop, and room for the
MCU fan-out without cutting the ground.

Why 2 oz outer over the 1 oz JLC04161H-1080B: phases carry 10 A RMS / 20 A peak and the bus 12 A; 2 oz halves the
track width for a given rise and doubles lateral heat spreading from the FETs, which is the thermal path on a
no-heatsink board. Cost: L1-L2 dielectric is 0.43 mm (vs 0.24), so the commutation loop's vertical part is a
little longer; nothing on this board needs controlled impedance (UART, SWD, Hall/encoder are all slow).
JLC 4layer_2oz rules: 0.1524 mm min trace, 0.1016 mm clearance, 0.2 mm drill - fine for LQFP-48 and VQFN-24
at 0.5 mm pitch.

Layer use:
- F.Cu: all parts; VM, PHASE and power-GND pours around the stage; signals.
- In1.Cu: GND, solid (never split; Kelvin sense pairs make their own return).
- In2.Cu: VM under the power stage and input; +5V / +3V3 islands may take the logic end if P7 finds it useful.
- B.Cu: GND pour + thermal spreading copper under the FETs; low-speed signal escapes.
