# P2 digest
- architect (opus) wrote architecture/{blocks,power_tree,stackup,sheets}.md + constraints.json (lint 0/0).
- DRV8300D + 12 V boost GVDD (DRV8320H rejected: 6.3 V VGS at VM=10 V). OC via INA240 -> G4 COMP -> TIM1 BKIN.
- 60 V NTMFS5C628NL x6, LM5164 100 V buck, LM74500 RP (23 in stock - recheck at P3), SMCJ28A, 1:16 dividers.
- Riskiest: 10 A RMS no heatsink (~3.4 W); P8 check_thermal confirms or derates.
- Coverage P2: 12/12 slots gap -> research not yet run.
