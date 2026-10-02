# P1 refdesign-amp digest
- TPA3116D2 fixed by brief; cross-checked datasheet SLOS708G, TPA3116D2EVM guide SLOU336B, LC
  filter app note SLAA701B/SLOA119, PowerPAD app note SLMA002H against the reference design's reported parts.
- The reference design's values (gain divider, bootstrap caps, PVCC decoupling tiers, 10uH/680nF output filter,
  3.3R/10nF damping branch) all check out against the datasheet/EVM, value-for-value.
- Flagged: the datasheet's own RthetaJA=14 C/W and the EVM both assume an attached aluminum heat
  sink, not copper-pour alone - copper-only cooling (requirements Q8) is unverified by any cited
  source and needs a thermal margin check, not a via-count copy.
- Quilter's blog has no board-specific content on this design (confirmed by two fetches); only
  general, part-agnostic skepticism about LLM PCB layout.
