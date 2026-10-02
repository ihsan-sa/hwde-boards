# Requirements - lipo-boost (PCB-0021-A)

## 1. Function
A small 2-layer board that runs a 5 V / 1 A USB gadget from a single-cell LiPo and charges that cell from USB. USB input charges the cell through a linear charger, a power-path (load sharing) keeps the 5 V output running while USB is present, and a synchronous boost converter makes 5 V from the cell otherwise. Recreation of the open-hardware PowerBoost 1000C class of design, built from this brief. No mode token: normal scope, geometry is an output of design within the soft limits below.

## 2. Interfaces
- USB input: USB micro-B receptacle (see Answers Q1), 5 V charge input only, no data.
- Battery: JST-PH 2-pin, 1S LiPo, polarity per Adafruit/JST-PH convention (see Answers Q3).
- Output: USB-A receptacle, 5 V / 1 A, power only (D+/D- left unconnected or shorted per Answers Q9).
- EN input: 2-pin header or pad; pulling low turns the 5 V output off.
- LEDs: charge (CHG), done (DONE), low-battery (LBO).

## 3. Power
- Input: USB 5 V (4.5-5.5 V), up to ~1.5 A draw (1 A charge plus load).
- Cell: 1S LiPo 3.0-4.2 V, assumed protected (own protection circuit).
- Charge current: 1 A default (Answers Q2), CC/CV 4.2 V, termination ~10% of set current.
- Output: 5 V at 1 A continuous from a synchronous boost; at 3.2 V cell that is ~2 A input, GUESS peak switch current ~3 A.
- Load sharing: output stays up when USB present (ideal-diode / power-path, Answers Q4).
- Low-battery threshold ~3.2 V (Answers Q5). Rail budget guesses: LED current ~1-2 mA each.

## 4. Environment
Indoor, 0-40 C, no enclosure specified, no ingress or vibration requirement. ASSUMED.

## 5. Size & mounting
- Outline: RELAXABLE (no HARD cap); target roughly 40 x 30 mm or smaller.
- Mounting: none required; 2 bare M2.5 holes optional (ASSUMED none, Answers Q10).
- Height: no limit; USB-A and JST dominate.

## 6. Quantity & budget
Quantity 5 boards (ASSUMED, prototype). Target unit cost under about USD 8 assembled, 2 layers.

## 7. Assembly
JLCPCB PCBA, single-sided assembly preferred (top), prefer basic/preferred library parts; through-hole USB-A and JST may be hand-fitted or JLC THT.

## 8. Compliance/safety flags
- Battery: 1S LiPo, 4.2 V charge, up to 1 A charge current: YES. Cell assumed protected; board gives no cell protection beyond charger limits.
- High current: boost input ~2-3 A peak: below the 3 A flag in steady state but near it; layout must use wide power traces.
- NTC thermistor: absent (Answers Q6).
- No mains, no motors, no >30 V, no RF.
- Charging a LiPo unattended carries fire risk; board is a prototype, not certified.

## 9. Open questions
All answered below as PROVISIONAL delegate answers (owner delegated all choices, unattended run). No question remains for the owner:
1. Micro-B or USB-C input? 2. Charge current? 3. Cell protected / polarity? 4. Power-path type? 5. Low-battery threshold? 6. NTC? 7. EN polarity/default? 8. Output USB-A data lines? 9. Output current limit? 10. Mounting holes?

## Answers
All PROVISIONAL (delegate answers, owner not asked).
1. Input connector: micro-B, cheaper and reference-like; no CC resistors needed. PROVISIONAL.
2. Charge current: 1 A default, set by a programming resistor on the charger. PROVISIONAL.
3. Cell: assumed to have its own protection circuit (PCM); JST-PH polarity per Adafruit convention (pin 1 +, to be stated in the design and silk-marked). PROVISIONAL.
4. Load sharing: ideal-diode/power-path via a P-MOSFET or Schottky from the charger/cell node, choice left to architecture. PROVISIONAL.
5. Low-battery LED lights at about 3.2 V cell. PROVISIONAL.
6. NTC: optional and absent (charger temperature pin tied to a fixed resistor/divider as in the reference). PROVISIONAL.
7. EN: active-high, pulled up on board so output is on by default; pull to GND turns it off. PROVISIONAL.
8. USB-A D+/D-: left floating, power only. PROVISIONAL.
9. Output current: 1 A rated; boost limit about 2 A; no extra eFuse. PROVISIONAL.
10. Mounting holes: none. PROVISIONAL.
