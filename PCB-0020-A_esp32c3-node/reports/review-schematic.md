# Schematic review - PCB-0020-A esp32c3-node

Scope: product (requirements section 1, no build mode). Method: netlist (reports/top.net) parsed and walked net by net, against the part JSONs and the four checklists.

Result: 0 errors, 6 warnings. No bring-up-blocking defect found.

## Verified correct
- USB-C: CC1/CC2 each 5.1k to GND, SBU NC, D+/D- rows joined to IO19/IO18 (correct C3 USB pins), USBLC6 pins 1/6 on D+, 3/4 on D-, 2 GND, 5 VBUS; shell on GND; no D+ pull-up needed (native PHY).
- Power path: Q1 G=VBUS, S=VSYS, D=VBAT; D3 anode VBUS to cathode VSYS; body diode feeds VSYS from VBAT without USB, gate high blocks it with USB. R5 pulls gate low when VBUS absent. Correct load-sharing.
- U2: VDD on VBUS (4.5 V min for the 4.20 V part met), PROG 5.1k = 196 mA, 4.7 uF on VDD and VBAT, STAT drives LED to VBUS (tri-state part OK).
- U3: 1 uF in, 1 uF + 10 uF + 100 nF out (>= 1 uF effective), EN tied to VSYS, pin 4 NC, no SNS variant. Headroom fine on USB; on battery it simply tracks VSYS near 3.4 V.
- U1: 3V3 pin with 10 uF + 100 nF, EN 10k + 1 uF RC, IO9/IO8/IO2 each 10k pull-up (correct strap levels), LED on IO10 (not a strap), I2C on IO6/IO7, ADC on IO3 (ADC1), JTAG/USB pins unconflicted, NC pads left open.
- U5: CSB and VDD/VDDIO on 3V3 (I2C mode), SDO to GND (0x76), 100 nF per supply pin. J3 order GND/3V3/SDA/SCL matches Qwiic. 4.7k pull-ups to 3V3.
- Battery divider 1M/1M with 100 nF: 2.1 V at 4.2 V, within ADC range, 2 uA drain; the 100 nF covers the 500k source impedance.
- Polarity: TVS cathode to VBUS, D3 cathode to VSYS, LEDs anode towards the supply side.

## Warnings
1. usb-budget (VBUS): charger 196 mA plus up to ~450 mA system peak exceeds the 500 mA entitlement and the 100 mA pre-enumeration limit.
2. tvs-clamp-vs-absmax (D1/U2): SMF5.0A clamp (9.2 V at surge) exceeds U2 VDD abs max 7.0 V.
3. battery-reverse-polarity (J2): no protection; relies on silk and BOM pack polarity (accepted default 1e).
4. ldo-thermal (U3): Tj ~114 C worst sustained on USB.
5. strap-pins-on-edge-pads (J4): IO2/IO8 strapping pins exposed on pads.
6. tactile-switch-pairing (SW1/SW2): internal pin pairing of the TS-1187A not confirmable here.

## Not verifiable
Footprint pad mapping of LEDs, switches and the TVS (pin 1 = cathode assumed); silk legends; layout items (antenna keep-out, BME280 separation).
