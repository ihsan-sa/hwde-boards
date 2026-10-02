# Bring-up shopping list: PCB-0018-A_bldc-motor-driver

Derived from bringup/procedure.json (2026-09-30T19:48:24Z) by npie shopping.py. Every line names the steps that need it; regenerate after the procedure changes.

## Equipment

| Role | What | Minimum spec | Needed by |
|---|---|---|---|
| psu | programmable bench power supply, one channel | >= 30 V and >= 0.3 A, a settable current limit and output switch, SCPI over USB or LAN; highest setting 28 V / 0.2 A | power-up.01, power-up.04, power-up.06, limits.01 (+6 more) |
| dmm | bench multimeter | functions diode, resistance, voltage; DC volts to >= 15 V; SCPI over USB or LAN | unpowered.03, unpowered.05, unpowered.07, unpowered.09 (+19 more) |
| scope | digital oscilloscope with 10x probes | >= 50 MHz, >= 2 channels, automatic measurements (duty, freq, vpp) and screenshots over SCPI | rails.12, rails.14, blocks.23, blocks.24 (+4 more) |
| logic | logic analyser supported by sigrok | >= 8 channels at >= 1 MS/s (an fx2lafw 8-channel clone is enough) | blocks.18 |
| console | USB-UART adapter | 3V3 logic levels, 115200 baud, TX/RX/GND on loose leads | programming.04, programming.05, blocks.01, blocks.02 (+12 more) |
| probe | SWD programming probe | a CMSIS-DAP, ST-LINK/V2+ or J-Link SWD probe (all driven by probe-rs); a cable to fit J601 | programming.02 |

## Parts

| What | Qty | Spec | Needed by |
|---|---|---|---|
| micro hook clips / test-point grabbers | 4 | for test points and passive pads | unpowered.03, unpowered.05, unpowered.07, unpowered.09 (+27 more) |
| supply leads, banana to croc clip, red + black | 1 | rated for the supply current | power-up.01 |
| female-female jumper wires, 2.54 mm | 10 | UART and analyser to the board's headers | programming.04 |
| ESD wrist strap and mat | 1 |  | all |

Stages not in this procedure (nothing bought for them): full-function - firmware has no spin command yet (manifest stage sixstep); limits:ov - over-voltage trip at 30 V is above the rated input max 28 V; not applied.
