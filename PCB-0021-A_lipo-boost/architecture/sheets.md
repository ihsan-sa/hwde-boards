# Sheet plan - PCB-0021-A (one schematic agent, two sheets; PROVISIONAL)

## Sheet `charger` (root file lipo-boost.kicad_sch, local sheet)
Blocks: U1 BQ24074, J1 micro-B, J2 JST-PH, D1/D2/D3 LEDs, Q1, U3 detector, TS/ISET/ILIM/TMR/ITERM resistors, USB-in/BAT/SYS caps.
Refdes: U1,U3; Q1; D1-D3; J1,J2; R1-R19; C1-C9; #PWR 100+.
Nets: local /CHG, /PGOOD, /ISET, /ILIM, /TMR, /ITERM, /TS, /DONE_K, /LB_K; power VBUS, VBAT, +SYS, GND.
Interface (hier pins) to `boost`: +SYS (out), VBAT (out), GND, /LBO (out), /EN (in from header).

## Sheet `boost`
Blocks: U2 TPS61023, L1, FB divider, EN pull-up, Cin/Cout, J4 USB-A (+R_DCP 0 R), J3 header.
Refdes: U2; L1; R20-R39; C10-C29; J3,J4; #PWR 200+.
Nets: local /SW, /FB, /EN, /USB_DP, /USB_DM (joined by R_DCP); power +SYS, VBAT, +5V, GND.
Interface to `charger`: +SYS (in), VBAT (in), GND, /LBO (in, to header), /EN.
Placement groups at P6: cin_u2_l1 (C10, U2, L1 hot loop), cout (C11,C12), u1_thermal (U1 + C_out/C_in), fb (R_FB1,R_FB2 away from L1).
