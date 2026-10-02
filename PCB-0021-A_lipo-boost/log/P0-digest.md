# P0 digest
- requirements.md by requirements-analyst (sonnet); check_requirements pass.
- 1S LiPo JST-PH, micro-B in, 1 A CC/CV charge to 4.2 V, power-path load sharing, sync boost 5 V/1 A to USB-A.
- EN active-high pulled up (on by default); charge/done/low-batt LEDs; low-batt ~3.2 V.
- 2L JLC PCBA single-sided, outline relaxable, no mounting holes.
- 10 OPEN answered as PROVISIONAL delegate (unattended run): cell protected, NTC absent, no eFuse, D+/D- policy left to P2.
- Risks: boost peak input ~2-3 A at low cell; power-path part; JST-PH polarity silk.
