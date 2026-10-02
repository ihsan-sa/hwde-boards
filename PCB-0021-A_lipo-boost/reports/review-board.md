### Reference design and licence

This board is a from-scratch recreation of Adafruit's PowerBoost 1000C (designed by Limor Fried / Ladyada for Adafruit Industries; repository github.com/adafruit/Adafruit-PowerBoost-1000C). The original is published under Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0). This design was made from the short brief and the datasheets; no Adafruit schematic or board file was copied, so it is not a derivative of those files. The original is credited here as the reference. If any file of the original is ever adopted, the result must carry attribution and be released under CC BY-SA 3.0 or a compatible licence.

### What is the same as the PowerBoost 1000C

- A load-sharing charger: USB 5 V charges a 1S LiPo at about 1 A, and the output keeps running while USB is plugged in.
- A 5 V / 1 A synchronous boost from the cell.
- An EN pin on a header that turns the output off when pulled low.
- A low-battery LED (LBO), plus charge and done LEDs.
- USB-A output socket, JST-PH 2-pin battery connector (pin 1 = +, as on the original), micro-B USB input, a 7-pin 2.54 mm header (GND, BAT, VS, 5V, LBO, EN, spare GND).
- Two copper layers.

### What differs, and why

- Charger: TI BQ24074RGTR (QFN-16 3x3, about 1,066 in stock, $1.23 each) instead of Microchip MCP73871 (QFN-20 4x4, about 112 in stock, $2.79). The BQ24074 holds the system rail at a fixed 4.4 V, so the boost always boosts and never passes USB through to the USB-A socket.
- Boost: TI TPS61023DRLR (SOT-563, about 41,700 in stock, $0.27 at 5) instead of TI TPS61090RSAR (QFN-16 4x4, $2.85). It is about a tenth of the price. It has no low-battery comparator, so a separate 3.2 V voltage detector (U3, MSXC61CN3302MR) drives the LBO output.
- Output voltage: about 4.95 V (732 k / 100 k feedback divider), inside the USB-A limit. Adafruit's is about 5.2 V by design, sagging toward 5.0 V.
- Inductor: 1 uH (4 A or better saturation) instead of 6.8 uH.
- Cell temperature input: a fixed 10 k resistor, since a JST-PH pack has no thermistor. The original has a fixed 15 k as drawn. No cell over-temperature cutoff on either.
- No reverse-battery FET and no PTC / eFuse on the 5 V output; a silk warning instead. A third-party JST pack wired backwards can still damage the board. Both choices are provisional (see the waivers below).
- Size: 53.9 x 38.8 mm, against about 36 x 23 mm for the original (the original's size is from the product page and is not verified here). Ours is above the roughly 40 x 30 mm soft target in the requirements (a relaxable target, not a hard cap); the outline was fitted to the placed parts and not shrunk further.
- Assembly: all 33 parts are JLCPCB-assembled, and every IC is a JLC Extended part.
- Charging while full load is drawn: about 0.25 A reaches the cell inside the 1.5 A input limit (the boost draws about 1.24 A at 4.4 V). The original behaves the same way with its 1.8 A cap.

### Open items for the owner (provisional waivers)

Every item below was proposed by the agent on 2026-10-01 and is PROVISIONAL until the owner approves it. The verify gate passes only with these waivers.

- U1 thermal (check_thermal): 1.1 W worst case gives a modelled rise of about 81 C against 40 C declared. The 2-layer model floor is about 55 C/W and the GND copper is already saturated. The BQ24074 folds charge current back at 125 C junction, so the cost is slower charging when hot, at 5 V in with a deeply discharged cell.
- U1 ground vias, 4 where the check wants 5: the exposed pad only fits 4. Risk: slightly higher pad-to-plane thermal resistance.
- +SYS pour neck and a 2-via transition near R6: this is the DONE-LED branch carrying a few mA; the 2.2 A budget is net-wide. No risk to the rail.
- GND neck on F.Cu near the USB-A socket J4 (63.5, 51.3): J4's return runs through its through-hole pads into the B.Cu ground plane. If the owner wants F.Cu return continuity at 1 A, add stitching vias there.
- Left as advisory warnings, not waived: C11, C12 and C13 ground pads 6.6 to 8.2 mm from a ground via (C13 loop about 11.4 nH); the U2 and R10 reference designators read as their neighbours' labels; 16 two-terminal parts and J3, J4, Q1 have no datasheet extraction for the ratings check.
- The earlier provisional P2 decisions also wait on the owner: no fuse or TVS at the input, no reverse-battery FET, no 5 V limiter, and the default 1 A charge current (1C only for a 1000 mAh cell; use a lower ISET resistor for a smaller cell).

### Route style

The route style check (reports/route_style.json) found 108 track segments, 0 arcs and 0 off-angle segments. It raised two warnings, both "needless jog": one 0.6 mm sidestep on +5V (F.Cu, near 57.5, 35.3), and a group of twelve sidesteps of 0.05 to 0.11 mm on the LBO net. Style score 0.88. Neither affects electrical function.
