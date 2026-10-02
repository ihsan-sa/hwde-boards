# P1 digest
- power (opus): RP high-side NFET + LM74500-class; TVS 28 V standoff (~45 V clamp); buck VM->5V, LDO 3V3, boost 12 V GVDD; 9x10uF 1210 + >=470uF bulk; ~3.5 W board loss.
- refdesign power stage: 10R gates, 1uF boot, Kelvin shunts 3-5 mOhm, 1:11 dividers, per-leg ceramics, TIDA-010251 thermal ~49 C at 10 A RMS.
- scouts (ran before power.md existed): DRV8320HRTVR driver (6-60 V, own charge pump -> the 12 V boost may be unnecessary),
  TDM3436 40 V FET, INA181A2 CSA, STM32G431CBT6, TPS54331 buck.
- CONFLICTS for P2 architect: FET must be 60 V (decision); buck/any IC on VM must take >= 45 V clamp (TPS54331 is 28 V - reject);
  DRV8320 charge pump vs power.md's 12 V boost - pick one.
- Decisions: 60 V FETs; external fuse, no hot-swap, no brake chopper (PROVISIONAL).
