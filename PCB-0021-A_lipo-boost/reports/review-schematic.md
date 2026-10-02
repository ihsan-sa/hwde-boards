# Schematic review PCB-0021-A (critical, inline)
Errors: 0. Warnings: 4. Checked every U1/U2/U3 pin against parts/*.json.

- U1: EN2=+SYS, EN1=GND, CE=GND = ILIM mode, enabled. RILIM 1.2k -> 1.27 A (K 1525; in 1.1k-8k range). RISET 1k -> 0.89 A. TS 10k fixed (no NTC). TMR 51k ok (18-72k). ITERM open = 10 % default. PGOOD/CHG open-drain used correctly. Caps: C1/C4 on VBUS, C2 on OUT, C3 on BAT.
- U2: Vout = 0.595*(1+732k/100k) = 4.95 V (VREF 580-610 mV: 4.8-5.1 V). EN pulled to +SYS with 100k (always on, header can pull low). 22uF x2 + 100nF out, 10uF + 100nF in, L1 1 uH.
- U3: MSXC61CN3302 NMOS open-drain, VIN=VBAT, OUT low below 3.3 V lights D3 (anode via 1k to +SYS) and drives LBO.
- Q1: gate=CHG (pulled up by R8), source=PGOOD, drain=DONE_K: DONE LED lit only when USB good and not charging. Correct.
- D1/D2/D3 polarity checked against footprint pin1=K (D3 pin1=A as noted in generator).
- J4: D+/D- shorted by 0R (DCP) ok. J3 order GND,VBAT,+SYS,+5V,LBO,EN,GND.

No generator change needed.
