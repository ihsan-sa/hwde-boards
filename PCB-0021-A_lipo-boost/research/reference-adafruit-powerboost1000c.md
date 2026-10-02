# Reference: Adafruit PowerBoost 1000C (as published)

For a fair comparison later. Our board is designed from the brief; this file is NOT a source to copy from.
Sources: repo https://github.com/adafruit/Adafruit-PowerBoost-1000C (README.md, license.txt, Rev B .sch/.brd; note the repo is
named Adafruit-PowerBoost-1000C, the "-PCB" URL 404s); learn guide https://learn.adafruit.com/adafruit-powerboost-1000c-load-share-usb-charge-boost
(read via the PDF https://cdn-learn.adafruit.com/downloads/pdf/adafruit-powerboost-1000c-load-share-usb-charge-boost.pdf); product https://www.adafruit.com/product/2465.
Forum threads (not readable, HTTP 403, only titles seen): https://forums.adafruit.com/viewtopic.php?t=106731 (500C vs 1000C load sharing), ...?f=19&t=126203 (schematic questions), ...?t=87044 (2 A output).

## Licence (exact)
- README.md, section License: "Designed by Limor Fried/Ladyada for Adafruit Industries. Creative Commons Attribution/Share-Alike, all text above must be included in any redistribution. See license.txt for additional information." No version number in the README.
- license.txt is the full Creative Commons Legal Code **Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)**. GitHub's licence detector shows "Other" because the file is named license.txt.
- Consequence: any derivative (copying or adapting the schematic/board, not just the idea) needs attribution and must be released under CC BY-SA 3.0 or a compatible licence, with the README text kept. A from-scratch design from the brief that copies no file is not a derivative; compare, do not copy. This repo is private, which matters if we publish.
- Repo issues (titles only, via gh): "Does not indicate full charge" and "Where is license.txt?".

## Parts (from the Rev B schematic .sch, values as drawn; fp = footprint)
| Block | Part | Detail |
|---|---|---|
| Charger / power path | Microchip MCP73871 (T-2CCI/ML, QFN-20 4x4) | 1.8 A max input; guide says 1000 mA charge max |
| Boost | TI TPS61090RSAR (QFN-16 4x4) | 2 A switch (~2.5 A peak), sync, 700 kHz class, LBI/LBO built in |
| Inductor | 6.8 uH, TDK VLC5045 footprint | |
| Caps | 10 uF 0805 x3 (C1,C7,C8), 2.2 uF, 0.1 uF, 100 uF 1210 (C6, on output) | |
| Output set | FB divider 1.87 M / 200 k = 5.19 V (my arithmetic, vs 0.5 V ref) | guide: ~5.2 V, dips to 5.0 V past ~500 mA |
| LBO set | LBI divider 1.87 M / 340 k = ~3.25 V (inferred) | guide: LBO low under 3.2 V |
| Enable | EN pin on header, pulled high to VS | switch can be small; ground EN to turn off |
| LEDs | Red low-batt (on LBO), blue 5 V present, orange charging, green done (MCP73871 STAT outputs) | 1 k series resistors |
| Low-batt PNP | MMUN2133LT1G (SC-59, bias-resistor PNP) | drives the red LED |
| Charger input | micro-B jack, 1 A Apple D+/D- dividers (43k/49.9k and 75k/49.9k) | iOS 1 A charge recognition |
| Output | USB-A receptacle THT (CN1), 2-pin terminal block footprint, 8-pin header (USB, BAT, VS, GND, 5V, EN, LBO) | |
| Battery | JST 2-PH | polarity warning in guide |
| Thermistor | 15 k resistor in THERM position (value as drawn; no NTC) | |
| Board | 2 layers (.brd uses only layers 1 and 16, my read); size about 36 x 23 mm per product page (from memory, unverified); .brd dimension-layer bbox ~40 x 25 mm; 2 x 2.5 mm mounting holes | |

## How its load sharing works
- MCP73871 is the power-path charger: VS (system rail) = USB 5 V less a MOSFET drop when plugged, = BAT when not (guide: "When there's no USB charging, the Vs pin will be the same voltage as the Bat pin").
- Boost (TPS61090) input is VS. Guide example: 1 A supply, boost wants 750 mA, charger draws 1000 mA, 750 mA to load, 250 mA to the cell. Up to 1.8 A drawn in total.
- Consequence: with USB present the boost sees ~5 V in and 5.2 V out, so it is on the edge of pass-through; ours (4.4 V OUT) avoids this.

## Known quirks and reviewer notes
From the learn guide:
- Needs a battery attached; "won't work without a battery".
- Charger chip gets "too hot to touch" charging at 1 A, or charging while boosting at 1.8 A (guide calls it normal; thermal foldback).
- LBO cannot be tied to EN for auto shut-off; LBO is pulled up to BAT and is unsafe for direct 3.3 V GPIO.
- 3-pin slide switches that make-before-break can short VS to GND on EN.
- Third-party JST cables with swapped polarity damage the board (no reverse protection).
- Needs a high quality, 2 A, thick-wire supply or it droops.
- 5.2 V output intentional (headroom), sags toward 5.0 V over ~500 mA.
- Output "floating" when disabled; do not back-feed it.
- Repo issue "Does not indicate full charge" (title only, not read).
Not read (403): forum threads; do not cite their contents.

## Keep / change (for later comparison)
Keep: charge+load-share function, 1 A / 5 V / 1 A envelope, EN on a small-signal pin, red low-batt + charge + done LEDs, JST-PH, USB-A out.
Change: bq24074 (4.4 V OUT, 3x3, deeper stock) for MCP73871 (QFN-20, 112 in stock); TPS61023 (SOT-563, $0.27) for TPS61090 (QFN-16, $2.85), losing LBO so add a 3.2 V detector; 5.0 V out (USB spec) not 5.2 V; 1 uH inductor, not 6.8 uH; add cell NTC option, reverse-polarity and output-short protection; add `PCB-0021 REV A` silk; JLC-assembled, all on one side if possible.
