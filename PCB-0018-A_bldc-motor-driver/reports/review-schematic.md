# PCB-0018-A schematic review (P4, adversarial)

Inputs: reports/top.net and reports/schematic.pdf (rendered from kicad/PCB-0018-A_bldc-motor-driver.kicad_sch),
parts/*.json and the DRV8300 / LM5164 / TPS61040 datasheet PDFs, architecture/constraints.json, checklists
power / mcu / connector. Build mode: none (default scope). Result: 2 errors, 6 warnings.

## Errors
1. **LM5164 has no ripple injection (U201, FB5V).** COT control needs >=20 mV in-phase ripple at FB
   (datasheet 6.3.1, Table 6-1). FB is a bare 33.2k/10k divider on an all-ceramic output (C202 22 uF,
   C205 10 uF, C207 1 uF), which gives ~1-2 mV at FB. Add Type 2 (RESR + CFF) or Type 3 (RA/CA/CB).
   The +5V rail feeds the boost, the LDO and both connectors, so this is the rail everything depends on.
2. **VM/GND input pads are test-point size (TP101, TP102).** 2.0 mm pad, 1.0 mm drill, carrying the whole bus
   (13 A continuous per constraints.json, ~25 A peak). The phase pads, which each carry less, are 4.0/2.0 mm.

## Warnings
3. DRV8300 GVDD: the datasheet asks for >=10 uF local. C304 (10 uF 25 V X5R 0805) keeps about 3-5 uF at 12 V.
   The 1 uF bootstrap caps also sit right at the >=1 uF minimum before derating.
4. TPS61040: the datasheet requires a feed-forward cap across R204. Without it the part double-pulses and ripple on GVDD rises.
5. Kelvin net ties NT401-406 are not in the leg placement groups. NT402/404/406 sit on global GND, so the N tap can
   land anywhere on GND rather than at R40x pad 2. At 3 mOhm, 1 mOhm of plane in the tap is a 33 % error.
6. Phase-voltage sense RC corner is ~170 Hz (9.4 k || 100 nF), which is too slow for BEMF or sensorless use.
7. The DC-link ripple is ~5-6 A RMS at 10 A/phase and the 470 uF electrolytic takes most of it. Check its ripple rating.
8. The encoder inputs have no pull-up (the Halls have 4.7 k). An open-collector encoder would need the internal ~40 k,
   which against the 2.2 nF filter gives edges of ~90 us.

## Checked and correct
- Power stage: HS D=VM, S=PHASE; LS D=PHASE, S=LS_SRC; shunt LS_SRC->GND; 10 R gate R, 10 k G-S pull-downs on
  both sides (HS to PHASE, LS to LS_SRC); DNP RC snubbers across each FET.
- DRV8300D: pinout matches the part JSON; the integrated boot diodes mean no external diode is needed; CBOOT BSTx-SHx per phase;
  MODE 10 k to GND = non-inverting (same as floating, 200 k internal pull-down); DT 40.2 k = ~200 ns; NC 7/8 to GND
  allowed; EP GND. Abs-max: BST 125 V, SHx 110 V, GHx-SHx 22 V vs 45 V clamp + 12 V: OK. MCU 3.3 V logic vs VIH 2.0 V: OK.
- TIM1 CH1-3 on PA8/9/10 and CH1N-3N on PB13/14/15, matching INHx/INLx.
- INA240A1: IN+ on the FET side, IN- on the GND side; REF1=VS, REF2=GND gives a 1.65 V midpoint; +/-27 A full scale vs 20 A peak;
  no input R (the datasheet says <=10 R); 100 R / 2.2 nF output filter; 100 nF each on VS. The outputs go to PA1/PA7/PB0
  (ADC1/ADC2 split, which allows simultaneous two-phase sampling, and COMP1/2/4 inputs).
- VBUS 150k/10k: 45 V -> 2.81 V.
- LM74500: Q101 S=VM_IN, D=VM (body diode forward-biased), VCAP 100 nF to SOURCE, EN tied to SOURCE, SOURCE bypass
  100 nF (>22 nF). The TVS SMCJ28A is placed with K on VM.
- LM5164: CBST 2.2 nF (range 1.5-2.5 nF), RON 31.6 k gives ~410 kHz, FB gives 5.18 V, EN on VM (100 V rated).
  TPS61040: FB gives 11.91 V, EN on VIN, D201 cathode on +12V. TLV75733: EN on IN, 1 uF out.
- Polarity: C101 + on VM (symbol + mark on pin 1). D201 pin 1 is the cathode (symbol bar) and sits on +12V. D101 is C=VM. The LEDs are
  A=pin 1, fed from the resistor, with K to GND.
- MCU: 3x VDD 100 nF + 4.7 uF; VDDA/VREF+ via ferrite with 1 uF+10 nF+1 uF+100 nF+100 nF; VBAT to 3V3; NRST
  100 nF + switch + SWD pin 10; BOOT0 10 k pull-down; SWD pinout is the standard Cortex 10-pin; the Hall/UART/encoder pins are FT.
- The 22 unconnected pins are all legitimate: connector mounting tabs (J701 5/6, J702 9/10), SWD 6/7/8, LM74500 NC 3/7/8,
  LM5164 PGOOD (OD output), TLV757 NC, and 10 unused MCU GPIO/OSC pins (set them to analog in firmware).

## Dispositions (track iteration 6, 2026-09-27)
- FIXED error, LM5164 ripple injection: Type 3 added on the regulators sheet, R206 100k (BUCK_SW to RIPPLE_INJ), C210 2.2nF (to +5V), C211 100nF (to FB5V). tau 220 us gives 28 mV at VM 10 V, 45 mV at 28 V and 49 mV at 45 V, all above the 20 mV floor.
- FIXED error, input pads: TP101/TP102 are now 4.0x4.0 mm pads with a 2.0 mm drill, the same as the phase pads.
- FIXED warning, GVDD: C304 is now 10uF 50V X7R 1210 (C2918502).
- OPEN, to do before P5: the TPS61040 feed-forward cap across R204 (the value needs the datasheet), the Kelvin net ties NT401-406 joining each leg's placement group (P6 constraint) and the encoder pull-ups (kept off by design: the encoders are 5 V push-pull; revisit if an open-collector encoder is in scope). FIXED warning, phase-sense RC: C521-C523 are now 2.2nF, a ~7.7 kHz corner. The C101 ripple rating and L202 Isat are still unverified because neither datasheet is in parts/.
