# Bring-up procedure: PCB-0018-A_bldc-motor-driver

Generated 2026-09-30T19:48:24Z by npie from the design inputs below; regenerate it after any design or firmware change.

| Input | sha256 |
|---|---|
| netlist: `kicad/PCB-0018-A_bldc-motor-driver.net` | `31d0f8db9afd` |
| constraints: `kicad/constraints.json` | `0780106a0c9d` |
| bom: `fab/BOM.csv` | `f914bf2c5610` |
| requirements: `requirements.md` | `acc5ff8498c6` |
| manifest: `firmware/fwe-manifest.json` | `197c37c8064d` |

Instruments: console, dmm, logic, probe, psu, scope.

Not in this procedure:

- full-function: firmware has no spin command yet (manifest stage sixstep)
- limits:ov: over-voltage trip at 30 V is above the rated input max 28 V; not applied

## Visual inspection (unpowered)

| Step | Action | Limit | From |
|---|---|---|---|
| visual.01 | PERSON: Check the board for damage, solder bridges on fine-pitch ICs (U101, U201, U202, U203, U301, U501, U502, U503, U601) and missing parts against fab/BOM.csv. |  |  |
| visual.02 | PERSON: Check orientation of polarised parts: D101 SMCJ28A, D201 MBR0520L, D601 LED green (power), D602 LED yellow (status), D603 LED red (fault), D701 PESD5V0S1BA-ES, D702 PESD5V0S1BA-ES, D703 PESD5V0S1BA-ES, D704 PESD5V0S1BA-ES, D705 PESD5V0S1BA-ES, D709 PESD5V0S1BA-ES, D710 PESD5V0S1BA-ES, D711 PESD5V0S1BA-ES, U101 LM74500-Q1, U201 LM5164, U202 TPS61040, U203 TLV75733, U301 DRV8300DRGER, U501 INA240A1, U502 INA240A1, U503 INA240A1, U601 STM32G431CBT6, Q101 NTMFS5C628NL, Q401 NTMFS5C628NL, Q402 NTMFS5C628NL, Q403 NTMFS5C628NL, Q404 NTMFS5C628NL, Q405 NTMFS5C628NL, Q406 NTMFS5C628NL, C101 470uF 63V, C104 470uF 63V. |  |  |

## Unpowered resistance and diode checks

| Step | Action | Limit | From |
|---|---|---|---|
| unpowered.01 | PERSON: Board unpowered, every cable off. Discharge the input capacitors. |  |  |
| unpowered.02 | PERSON: DMM on resistance: red (+) on TP101 (VM_IN), black (-) on TP102 (GND). |  |  |
| unpowered.03 | Measure resistance: VM_IN to GND is not a short | >= 1000 ohm | short check VM_IN-GND: floor power net 1000 ohm |
| unpowered.04 | PERSON: DMM on resistance: red (+) on C101 pin 1 (VM), black (-) on TP102 (GND). |  |  |
| unpowered.05 | Measure resistance: VM to GND is not a short | >= 1000 ohm | short check VM-GND: floor power net 1000 ohm |
| unpowered.06 | PERSON: DMM on resistance: red (+) on C206 pin 1 (+12V), black (-) on TP102 (GND). |  |  |
| unpowered.07 | Measure resistance: +12V to GND is not a short | >= 100 ohm | short check +12V-GND: floor logic rail 100 ohm |
| unpowered.08 | PERSON: DMM on resistance: red (+) on C202 pin 1 (+5V), black (-) on TP102 (GND). |  |  |
| unpowered.09 | Measure resistance: +5V to GND is not a short | >= 100 ohm | short check +5V-GND: floor logic rail 100 ohm |
| unpowered.10 | PERSON: DMM on resistance: red (+) on C208 pin 1 (+3V3), black (-) on TP102 (GND). |  |  |
| unpowered.11 | Measure resistance: +3V3 to GND is not a short | >= 100 ohm | short check +3V3-GND: floor logic rail 100 ohm |
| unpowered.12 | PERSON: DMM on resistance: red (+) on C209 pin 1 (VDDA), black (-) on TP102 (GND). |  |  |
| unpowered.13 | Measure resistance: VDDA to GND is not a short | >= 100 ohm | short check VDDA-GND: floor logic rail 100 ohm |
| unpowered.14 | PERSON: DMM on resistance: red (+) on TP401 (PHASE_A), black (-) on TP102 (GND). |  |  |
| unpowered.15 | Measure resistance: PHASE_A to GND is not a short | >= 1000 ohm | short check PHASE_A-GND: floor power net 1000 ohm |
| unpowered.16 | PERSON: DMM on resistance: red (+) on TP402 (PHASE_B), black (-) on TP102 (GND). |  |  |
| unpowered.17 | Measure resistance: PHASE_B to GND is not a short | >= 1000 ohm | short check PHASE_B-GND: floor power net 1000 ohm |
| unpowered.18 | PERSON: DMM on resistance: red (+) on TP403 (PHASE_C), black (-) on TP102 (GND). |  |  |
| unpowered.19 | Measure resistance: PHASE_C to GND is not a short | >= 1000 ohm | short check PHASE_C-GND: floor power net 1000 ohm |
| unpowered.20 | PERSON: DMM on diode: red (+) on TP401 (PHASE_A), black (-) on C101 pin 1 (VM). |  |  |
| unpowered.21 | Measure diode: Q401 body diode conducts one way | 0.3 .. 0.8 V (nominal 0.5) | Q401 body diode (netlist S=PHASE_A, D=VM) |
| unpowered.22 | PERSON: DMM on diode: red (+) on C432 pin 2 (LS_SRC_A), black (-) on TP401 (PHASE_A). |  |  |
| unpowered.23 | Measure diode: Q402 body diode conducts one way | 0.3 .. 0.8 V (nominal 0.5) | Q402 body diode (netlist S=LS_SRC_A, D=PHASE_A) |
| unpowered.24 | PERSON: DMM on diode: red (+) on TP402 (PHASE_B), black (-) on C101 pin 1 (VM). |  |  |
| unpowered.25 | Measure diode: Q403 body diode conducts one way | 0.3 .. 0.8 V (nominal 0.5) | Q403 body diode (netlist S=PHASE_B, D=VM) |
| unpowered.26 | PERSON: DMM on diode: red (+) on C434 pin 2 (LS_SRC_B), black (-) on TP402 (PHASE_B). |  |  |
| unpowered.27 | Measure diode: Q404 body diode conducts one way | 0.3 .. 0.8 V (nominal 0.5) | Q404 body diode (netlist S=LS_SRC_B, D=PHASE_B) |
| unpowered.28 | PERSON: DMM on diode: red (+) on TP403 (PHASE_C), black (-) on C101 pin 1 (VM). |  |  |
| unpowered.29 | Measure diode: Q405 body diode conducts one way | 0.3 .. 0.8 V (nominal 0.5) | Q405 body diode (netlist S=PHASE_C, D=VM) |
| unpowered.30 | PERSON: DMM on diode: red (+) on C436 pin 2 (LS_SRC_C), black (-) on TP403 (PHASE_C). |  |  |
| unpowered.31 | Measure diode: Q406 body diode conducts one way | 0.3 .. 0.8 V (nominal 0.5) | Q406 body diode (netlist S=LS_SRC_C, D=PHASE_C) |

## Current-limited power-up

| Step | Action | Limit | From |
|---|---|---|---|
| power-up.01 | Supply 12 V, limit 0.2 A, output off |  | requirements VIN 10-28 V: min + 2 V; limit min(0.2 A, 2x full load 0.339 A) |
| power-up.02 | PERSON: Connect the supply: + to TP101 (VM_IN), - to TP102 (GND). Supply set to 12 V / 0.2 A, output still off. |  |  |
| power-up.03 | PERSON: About to switch the supply on at 12 V with a 0.2 A limit. Hands clear; watch for smoke or a hot part. |  |  |
| power-up.04 | Supply 12 V, limit 0.2 A, output ON |  |  |
| power-up.05 | Wait 1 s |  |  |
| power-up.06 | Measure current: idle input current | 0.002 .. 0.18 A | alive floor; below 90 % of the limit (not in CC) |
| power-up.07 | PERSON: Touch-test: no part is hot a few seconds after power-up. |  |  |

## Rail voltages and ripple

| Step | Action | Limit | From |
|---|---|---|---|
| rails.01 | PERSON: DMM on DC volts: red (+) on C101 pin 1 (VM), black (-) on TP102 (GND). |  |  |
| rails.02 | Measure voltage: VM voltage | 11.4 .. 12.12 V (nominal 12) | follows the input (rated like VM_IN): setpoint -5 %/+1 % |
| rails.03 | PERSON: DMM on DC volts: red (+) on C206 pin 1 (+12V), black (-) on TP102 (GND). |  |  |
| rails.04 | Measure voltage: +12V voltage | 11.04 .. 12.96 V (nominal 12) | constraints voltages[+12V]=12 V, +/-8 % (catch-diode converter) |
| rails.05 | PERSON: DMM on DC volts: red (+) on C202 pin 1 (+5V), black (-) on TP102 (GND). |  |  |
| rails.06 | Measure voltage: +5V voltage | 4.75 .. 5.25 V (nominal 5) | constraints voltages[+5V]=5 V, +/-5 % |
| rails.07 | PERSON: DMM on DC volts: red (+) on C208 pin 1 (+3V3), black (-) on TP102 (GND). |  |  |
| rails.08 | Measure voltage: +3V3 voltage | 3.135 .. 3.465 V (nominal 3.3) | constraints voltages[+3V3]=3.3 V, +/-5 % |
| rails.09 | PERSON: DMM on DC volts: red (+) on C209 pin 1 (VDDA), black (-) on TP102 (GND). |  |  |
| rails.10 | Measure voltage: VDDA voltage | 3.135 .. 3.465 V (nominal 3.3) | constraints voltages[VDDA]=3.3 V, +/-5 % |
| rails.11 | PERSON: Scope channel 1 on C206 pin 1 (+12V), ground spring to the nearest GND pad, AC coupled, 20 MHz bandwidth limit. |  |  |
| rails.12 | Scope ch1 vpp: +12V ripple | <= 0.24 V | switched rail ripple <= 2 % of 12 V |
| rails.13 | PERSON: Scope channel 1 on C202 pin 1 (+5V), ground spring to the nearest GND pad, AC coupled, 20 MHz bandwidth limit. |  |  |
| rails.14 | Scope ch1 vpp: +5V ripple | <= 0.1 V | switched rail ripple <= 2 % of 5 V |

## Programming and first boot

| Step | Action | Limit | From |
|---|---|---|---|
| programming.01 | PERSON: Connect the SWD probe to J601; the board stays powered from the supply. |  |  |
| programming.02 | Flash the firmware (elf) with the bench's SWD probe |  | manifest flash.commands, firmware 0.1.0+g6a564231 |
| programming.03 | PERSON: Connect the USB-UART (3V3, 115200 8N1) to J701: adapter RX to pin 3 (board TX), adapter TX to pin 4 (board RX), GND to GND. Then press reset. |  |  |
| programming.04 | Console read, expect `^fwe PCB-0018-A ` within 5 s |  | manifest uart.banner_regex |
| programming.05 | Console send `version`, expect `^OK ` within 2 s |  | manifest commands[version] |

## Per-block tests

| Step | Action | Limit | From |
|---|---|---|---|
| blocks.01 | Console send `version`, expect `^OK \{"board":"PCB-0018-A"` within 5 s |  | manifest test_hooks[version] |
| blocks.02 | Console send `status`, expect `^OK ` within 5 s |  | manifest test_hooks[status] |
| blocks.03 | Console send `selftest`, expect `^OK ` within 5 s |  | manifest test_hooks[selftest] |
| blocks.04 | Console send `adc`, expect `^OK ` within 5 s |  | manifest test_hooks[adc] |
| blocks.05 | Console send `status`, expect `^OK ` within 2 s |  | manifest commands[status].reply_fields vbus_v vs the supply setting +/-5% |
| blocks.06 | PERSON: DMM on DC volts: red (+) on R501 pin 1 (CSA_A_OUT), black (-) on TP102 (GND). |  |  |
| blocks.07 | Measure voltage: U501 sense-amp offset | 1.6 .. 1.7 V (nominal 1.65) | U501 INA240A1 REF1=+3V3, REF2=GND: zero-current output at their mean +/-3 % |
| blocks.08 | PERSON: DMM on DC volts: red (+) on R502 pin 1 (CSA_B_OUT), black (-) on TP102 (GND). |  |  |
| blocks.09 | Measure voltage: U502 sense-amp offset | 1.6 .. 1.7 V (nominal 1.65) | U502 INA240A1 REF1=+3V3, REF2=GND: zero-current output at their mean +/-3 % |
| blocks.10 | PERSON: DMM on DC volts: red (+) on R503 pin 1 (CSA_C_OUT), black (-) on TP102 (GND). |  |  |
| blocks.11 | Measure voltage: U503 sense-amp offset | 1.6 .. 1.7 V (nominal 1.65) | U503 INA240A1 REF1=+3V3, REF2=GND: zero-current output at their mean +/-3 % |
| blocks.12 | PERSON: Note which LEDs are lit: D601 LED green (power), D602 LED yellow (status), D603 LED red (fault). |  |  |
| blocks.13 | PERSON: Press and release SW601 (Reset switch SMD). |  |  |
| blocks.14 | Console read, expect `^fwe PCB-0018-A ` within 5 s |  | netlist SW601 on NRST |
| blocks.15 | PERSON: Press and release SW602 (User switch SMD). |  |  |
| blocks.16 | Console read, expect `^EVT ` within 5 s |  | netlist SW602 on USER_SW |
| blocks.17 | PERSON: Connect the logic analyser to the Hall inputs (HALL_A, HALL_B, HALL_C) at J702 pins 3, 4, 5; plug in the Hall sensor and turn the motor slowly by hand during the capture. |  |  |
| blocks.18 | Logic capture HALL_A, HALL_B, HALL_C for 3 s | >= 2 edges per channel | netlist HALL_* nets |
| blocks.19 | PERSON: Motor DISCONNECTED. The next steps switch the bridge with no load at 12 V. Confirm the phase outputs are free. |  |  |
| blocks.20 | Console send `arm`, expect `^OK ` within 2 s |  | manifest commands[arm] safe:false |
| blocks.21 | Console send `duty 0.5 0 0`, expect `^OK ` within 2 s |  | manifest commands[duty] |
| blocks.22 | PERSON: Scope channel 1 on TP401 (PHASE_A), DC coupled, 10x probe. |  |  |
| blocks.23 | Scope ch1 duty: PHASE_A switches (Q401/Q402) | 0.45 .. 0.55  (nominal 0.5) | commanded duty 0.5 +/-0.05 |
| blocks.24 | Scope ch1 freq: PHASE_A PWM frequency | 19600 .. 20400 Hz (nominal 20000) | manifest safety.pwm_hz +/-2% |
| blocks.25 | Console send `duty 0 0.5 0`, expect `^OK ` within 2 s |  | manifest commands[duty] |
| blocks.26 | PERSON: Scope channel 1 on TP402 (PHASE_B), DC coupled, 10x probe. |  |  |
| blocks.27 | Scope ch1 duty: PHASE_B switches (Q403/Q404) | 0.45 .. 0.55  (nominal 0.5) | commanded duty 0.5 +/-0.05 |
| blocks.28 | Scope ch1 freq: PHASE_B PWM frequency | 19600 .. 20400 Hz (nominal 20000) | manifest safety.pwm_hz +/-2% |
| blocks.29 | Console send `duty 0 0 0.5`, expect `^OK ` within 2 s |  | manifest commands[duty] |
| blocks.30 | PERSON: Scope channel 1 on TP403 (PHASE_C), DC coupled, 10x probe. |  |  |
| blocks.31 | Scope ch1 duty: PHASE_C switches (Q405/Q406) | 0.45 .. 0.55  (nominal 0.5) | commanded duty 0.5 +/-0.05 |
| blocks.32 | Scope ch1 freq: PHASE_C PWM frequency | 19600 .. 20400 Hz (nominal 20000) | manifest safety.pwm_hz +/-2% |
| blocks.33 | Console send `disarm`, expect `^OK ` within 2 s |  | manifest commands[disarm] |

## Operating range and protection

| Step | Action | Limit | From |
|---|---|---|---|
| limits.01 | Supply 10 V, limit 0.2 A, output ON |  | requirements VIN min 10 V |
| limits.02 | Wait 1 s |  |  |
| limits.03 | Measure current: idle current at 10 V | 0.002 .. 0.18 A | idle current holds across the input range |
| limits.04 | Supply 28 V, limit 0.2 A, output ON |  | requirements VIN max 28 V |
| limits.05 | Wait 1 s |  |  |
| limits.06 | Measure current: idle current at 28 V | 0.002 .. 0.18 A | idle current holds across the input range |
| limits.07 | Supply 8.5 V, limit 0.2 A, output ON |  | manifest safety.vbus_uv_v 9 V - 0.5 V |
| limits.08 | Console read, expect `^EVT .*uv` within 5 s |  | under-voltage trip reported |
| limits.09 | Supply 12 V, limit 0.2 A, output ON |  |  |
| limits.10 | Console send `clear`, expect `^OK ` within 2 s |  | manifest safety.fault_clear |
| limits.11 | Supply 12 V, limit 0.2 A, output off |  |  |

