# requirements - esp32c3-node

P0 requirements distilled from `brief/brief.md` (2026-10-01, unattended track run).
One agent played the P0-P3 roles in sequence (spend cap); see state.json decisions.

## 1. Function

Mode declaration: the brief carries NO mode token, so mode = none - design
normally. Scope = product, per the brief's own words ("product scope ... meant to
go to JLCPCB as-is"): protection, filtering and enclosure-free robustness are in
scope and their absence is a reviewer finding. Binding: the "roughly XIAO-sized"
size is a SOFT preference (no HARD cap, section 5). Stage under study: none.

A tiny 2-layer WiFi + Bluetooth LE sensor node built around an Espressif
ESP32-C3-MINI-1 module (PCB antenna). USB-C supplies 5 V and carries the C3's
native USB (USB-Serial-JTAG on GPIO18/GPIO19) for flashing and console - no
USB-UART bridge. A single-cell LiPo on a JST-PH 2-pin connector is charged from
USB by a charger with power path, so the board runs from USB with or without a
battery and from the battery alone. One 3.3 V LDO feeds everything. The battery
voltage is divided down into an ADC pin. A BME280-class T/RH/P sensor and a
Qwiic/STEMMA QT connector share one I2C bus. BOOT and RESET buttons, one status
LED, spare GPIOs on 0.1 in edge pads. Quantity 5, JLC economy PCBA.

## 2. Interfaces

- USB-C receptacle, USB 2.0 full-speed device (12 Mb/s), D+/D- to the module's
  GPIO19/GPIO18 (USB_D+/USB_D-), ESD protection on D+/D-/VBUS, 5.1 k Rd on CC1
  and CC2 independently (default-USB sink, <= 500 mA).
- Battery: JST-PH 2.0 mm 2-pin, 1S LiPo (see section 3 and section 8).
- Qwiic / STEMMA QT: JST-SH 1.0 mm 4-pin, GND / 3V3 / SDA / SCL (Qwiic order),
  same I2C bus as the sensor, on-board pull-ups.
- BOOT button on GPIO9 (low at reset = download mode); RESET button on EN with
  the RC delay the module datasheet requires.
- Status LED on a GPIO that is not a boot-breaking strap pin.
- Spare GPIOs on 0.1 in (2.54 mm) plated edge pads. ASSUMED: plain plated
  through-holes at the board edge, not castellations (castellation is a paid
  JLC option; see open question 6).
- Antenna: the module's PCB antenna at a board edge with the datasheet keep-out
  free of copper (all layers) and parts.

## 3. Power

- Input 1: USB-C VBUS 5 V nominal (4.75-5.25 V), default-USB current
  (<= 500 mA) - no PD.
- Input 2: 1S LiPo, 3.0-4.2 V (3.7 V nominal). PROVISIONAL (section 8): cell
  class ~400 mAh with its own protection PCB; charge to 4.20 V.
- Charger with power path: system load is served from VBUS when present, the
  battery charges with what is left; without VBUS the system runs from the
  battery. Charge current PROVISIONAL <= 200 mA (0.5C of a 400 mAh cell).
- 3.3 V rail: one LDO, >= 500 mA, low dropout (runs from the battery down to
  ~3.5 V cell), low Iq for battery life.
- Battery sense: divider from VBAT into an ADC1 pin (ESP32-C3 ADC1, GPIO0-4).
- Rail budget (GUESSES, architect replaces them): ESP32-C3 WiFi TX peaks
  ~350 mA (module datasheet), BME280 < 1 mA, LED ~2 mA, Qwiic reserve 100 mA
  (open question 3). Peak 3V3 ~ 450 mA.

## 4. Environment

Not stated. ASSUMED: indoor, 0-40 C ambient, bare board, no ingress or
vibration requirement (open question 2). LiPo charging allowed only 0-45 C;
without an NTC the board relies on the cell's protection PCB and the charger's
die-temperature regulation (section 8).

## 5. Size & mounting

- Outline: "roughly XIAO-sized (21 x 17.8 mm) if an honest layout allows" -
  a SOFT preference, no HARD cap. The module alone is 13.2 x 16.6 mm and the
  antenna keep-out must sit at an edge, so the layout earns the outline at
  P5/P6 (open question 5).
- Mounting holes: none stated. ASSUMED: none (XIAO-class boards mount by the
  edge pads); board_init must not add default M3 holes on a board this small.
- Height: no limit stated.

## 6. Quantity & budget

- Quantity: 5 assembled boards (prototype run). ASSUMED (open question 4).
- Unit cost: no target stated. Posture: JLC economy PCBA, Basic/Preferred
  parts where they exist, Extended only where the function needs it (module,
  sensor, charger, connectors).

## 7. Assembly

- JLC economy PCBA, single-sided SMD (top). ASSUMED.
- The JST-PH battery connector, USB-C and JST-SH are SMD variants so they ride
  the PCBA run. Edge pads ship bare (no header).
- 2 layers, 1.6 mm FR-4 (open question 7 on thickness), HASL lead-free, green.

## 8. Compliance/safety flags

- Mains voltage: NOT APPLICABLE - USB 5 V input only.
- Battery: APPLIES. Single-cell lithium-polymer charging. Safety unknowns
  (chemistry confirmation, cell capacity, charge current, temperature sensing,
  reverse-insertion) are questions 1a-1e below; the unattended run answers them
  PROVISIONALLY and conservatively, re-confirmed at H1.
- Motors: NOT APPLICABLE.
- >30 V: NOT APPLICABLE (highest voltage 5.25 V VBUS).
- High current (>3 A): NOT APPLICABLE (< 0.6 A anywhere).
- RF transmit: APPLIES - 2.4 GHz WiFi/BLE through a pre-certified module
  (ESP32-C3-MINI-1 carries FCC/CE/IC module grants). The board must not
  modify the RF path; the module's antenna keep-out is a hard layout rule.

## 9. Open questions

Unattended run: the orchestrator answers these on the owner's behalf
(delegated, "decide for yourself") and records each as PROVISIONAL.

1. Battery (safety):
   1a. Is the cell a 1S lithium-polymer / Li-ion, 4.20 V full charge?
       Recommended default: YES, 4.20 V termination.
   1b. Cell capacity class? Recommended default: ~400 mAh (300-1000 mAh cells
       still safe at the chosen current).
   1c. Charge current? Recommended default: <= 200 mA (0.5C of 400 mAh).
   1d. Battery temperature sensing (NTC)? Recommended default: NO NTC fitted;
       require a protected cell; charger IC with thermal regulation.
   1e. Reverse battery insertion protection? Recommended default: no active
       element; polarity marked on silk (JST-PH pin 1 = +, the Adafruit/
       SparkFun convention).
2. Environment indoor 0-40 C, bare board? Recommended default: YES.
3. Qwiic 3.3 V budget for external devices? Recommended default: 100 mA.
4. Quantity 5 assembled? Recommended default: YES.
5. Size: is XIAO-size a soft preference the honest layout may exceed?
   Recommended default: SOFT.
6. Edge pads: plain plated 0.1 in through-holes rather than castellations?
   Recommended default: plated through-holes (no castellation fee).
7. Board thickness 1.6 mm? Recommended default: 1.6 mm (JLC default stackup).
