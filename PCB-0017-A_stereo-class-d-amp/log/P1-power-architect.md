# P1 research-power-architect - 2026-09-27
- Found: TPA3116D2 is DAD pad-up only (SLOS708G); PCB copper cannot sink it; the reference design's write-up admits a top heatsink is needed. Pin-compatible TPA3118D2DAPR (pad down, C46497 in stock) recommended -> OPEN 1.
- Found: input current 3.6 A at 12 V/4 ohm/10 % THD, 4.0 A at 13.2 V; +12V sized 4 A, outputs 3 A -> OPEN 2 (Q6 provisional 3 A too low for the input).
- Thermal RthJA values for 44x34 mm are estimates (+/-30 %), scaled from TI's 22 C/W EVM figure; not verified by simulation or measurement.
- 2 oz recommended; PLIMIT tied to GVDD; FAULTZ->SDZ suggested for auto-recovery.
- Next: orchestrator decides OPEN 1-3 at H1; component-scout sources the part, inductors and bulk caps.
