# interface - USB 2.0 full speed device (interface spec, P1)

START: reference/interfaces/usb-fs.{json,md} (canonical, sourced per number there).
Applicability re-verified for this board:

| constraint | value | source / delta |
|---|---|---|
| pair | /USB_DP (GPIO19, pin 27) / /USB_DM (GPIO18, pin 26) | ESP32-C3-MINI-1 DS v2.2 Table 3-1 |
| t_rise | 4.0 ns (FS fastest edge) | USB2.0 Table 7-9 via canonical |
| impedance | 90 ohm target DROPPED | 2-layer, FS < 100 mm: canonical note (NXP AN11392 3.2); Espressif guideline says 90 ohm +/-10% - unachievable as controlled impedance on 1.6 mm 2L; pair kept < 15 mm, coupled, over B.Cu GND |
| skew / uncoupled | 5 mm / 5 mm (tidiness bars) | canonical |
| D+ pull-up | none external - PHY embeds it | ESP32-C3 USB Serial/JTAG (DS 5.2.1.5) |
| series R | none fitted | Espressif HW guidelines "reserve space" - ASSUMED not needed for the internal PHY at FS; recorded as a P2 decision |
| ESD | USBLC6-2SC6 at the receptacle, in-line, VBUS pin to VBUS | canonical (AN4879 Table 11) |
| VBUS bulk | <= 10 uF total incl. VSYS (Schottky passes inrush) | USB2.0 7.2.4.1 |
| CC | 5.1k Rd on CC1 and CC2 separately | USB Type-C 4.5.1.2.1 via PCB-0015 research |
| shield | to GND directly (single-ground board) | canonical ASSUMED |

constraints_lint: see log (run at P1 exit).
