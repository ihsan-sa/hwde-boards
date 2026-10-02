# P1 digest
- Roster: component-scout (sonnet), reference-design (sonnet, incl. both reference-design sources), power-architect (opus).
- DEVIATION: TPA3116D2 is pad-UP only (DAD); swapped to pin-compatible pad-down TPA3118D2DAPR (C46497) so the board copper sinks it.
- +12V 4 A (3.6 A at 10% THD, 4 ohm); outputs 3 A; chip loss ~3 W (4 ohm 1%), ~1.2 W (8 ohm), ~0.8 W music.
- 44x34 mm holds 8 ohm full power and 4 ohm music; sustained 4 ohm full sine needs ~50x50 mm (not required).
- L = SLO0630H100MTT 7.3x6.6 mm (Isat 5.5 A) - the size driver; 680 nF filter caps; 3.3R+10nF damping; 2x100 uF (polymer+electrolytic).
- 2 oz copper preferred; PLIMIT->GVDD, FAULTZ->SDZ, 20 dB gain (5.6k), 100k pull-ups.
- Quilter source had no board-specific content; JLC source: 44x34, 2L, 45 fp / 40 fitted, 0 ERC/DRC, never fabricated.
