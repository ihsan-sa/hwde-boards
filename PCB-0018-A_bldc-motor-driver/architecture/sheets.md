# hierarchical sheet plan (P2)

Net naming (canonical; constraints.json uses these):
- Power nets are global and bare: `VM`, `+12V`, `+5V`, `+3V3`, `GND`.
- Cross-sheet interface nets are labelled on the ROOT sheet, so they come out as `/NAME`.
- Sheet-local nets come out as `/<sheet>/NAME`.
- One GND net only (no AGND/PGND split); separation is done by placement and Kelvin routing.

Refdes: every sheet owns a hundred-block (R101..R199, C101.., U101.., #PWR0101..); pwr_base = the sheet base.
Root-sheet parts: H1-H4 (M3 corner holes), fiducials FID1-FID3 if P5 wants them.

| Sheet | Base | Blocks | Interface nets (hier pins) |
|---|---|---|---|
| power_in | 100 | VM/GND pads TP101 (VM), TP102 (GND); Q101 RP FET; U101 LM74500; D101 SMCJ28A; C101, C104 470uF/63V THT; C102-C103 MLCC | out: `VM`, `GND` |
| regulators | 200 | U201 LM5164 + L201; U202 TPS61040 + L202 + D201; U203 TLV75733; FB201 VDDA ferrite | in: `VM`; out: `+5V`, `+12V`, `+3V3`, `/VDDA` |
| gate_driver | 300 | U301 DRV8300D; C301-C303 boot caps; GVDD caps; R301 DT, MODE strap | in: `+12V`, `/INHA` `/INLA` `/INHB` `/INLB` `/INHC` `/INLC`; out: `/GHA` `/GLA` `/GHB` `/GLB` `/GHC` `/GLC`; bidir: `/PHASE_A` `/PHASE_B` `/PHASE_C` (SHx) |
| power_stage | 400 | leg A: Q401 (HS), Q402 (LS), R401 shunt, C401-C403 10uF 1210, C404 100nF; leg B: Q403, Q404, R402, C405-C408; leg C: Q405, Q406, R403, C409-C412; gate R R411-R416; gate pull-downs R421-R426; DNP snubbers R431-R436 / C431-C436; phase pads TP401-TP403 | in: `VM`, `GND`, `/GHx`, `/GLx`; out: `/PHASE_A/B/C`, `/ISNS_A_P` `/ISNS_A_N` (and B, C) |
| sensing | 500 | U501-U503 INA240A1 + input RC; phase dividers R5xx for `/VSENSE_A/B/C`; bus divider for `/VBUS_SENSE` | in: `/ISNS_x_P/N`, `/PHASE_x`, `VM`, `+3V3`; out: `/ISENSE_A/B/C`, `/VSENSE_A/B/C`, `/VBUS_SENSE` |
| mcu | 600 | U601 STM32G431CBT6 + decoupling; J601 SWD 2x5 1.27; SW601 reset, SW602 user; D601-D603 LEDs (power, status, fault) | in: `+3V3`, `/VDDA`, `/ISENSE_x`, `/VSENSE_x`, `/VBUS_SENSE`, `/HALL_A/B/C`, `/ENC_A/B/Z`, `/UART_RX`; out: `/INHx`, `/INLx`, `/UART_TX` |
| io | 700 | J701 JST-GH 4 control; J702 8-pin sensor; F701/F702 0.2 A PTC; ESD + series R + pull-ups + RC filters | in: `+5V`, `+3V3`; bidir: `/UART_TX`, `/UART_RX`, `/HALL_A/B/C`, `/ENC_A/B/Z` |

Sheet-local nets that constraints.json names: `/power_in/VM_IN` (pad to RP FET), `/power_stage/LS_SRC_A/B/C`
(LS source = shunt top), `/gate_driver/BSTA/B/C`, `/regulators/BUCK_SW`, `/regulators/BOOST_SW`.
Connector-side 5 V after the PTCs: `/io/CTL_5V`, `/io/SEN_5V`.

MCU pin notes for P3/P4: TIM1 CH1-3 + CH1N-3N for INH/INL (PA8/PA9/PA10, PB13/PB14/PB15); ISENSE_x on pins
that are both ADC and COMP+ inputs (COMP -> TIM1 BKIN for overcurrent); Halls on a timer's CH1-3 in XOR/hall
mode; encoder on another timer's CH1/CH2 + ETR/GPIO for Z; UART on USART1 or USART2; PB8/BOOT0 kept for BOOT0
(pull-down), not used as an input.

Silkscreen: "PCB-0018 REV A" on F.Silk, plus pad labels VM, GND, A, B, C beside the power pads.
