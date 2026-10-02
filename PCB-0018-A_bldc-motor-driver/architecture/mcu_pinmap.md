# STM32G431CBT6 (LQFP-48) pin map (P3 -> P4 input)

Grounded in parts/C529355.json (DS12589 Table 12). Chosen by the orchestrator at P3 exit.

| Pin | Port | Net | Function | Why |
|---|---|---|---|---|
| 30 | PA8 | /INHA | TIM1_CH1 | 6-PWM with complementary outputs on one advanced timer |
| 31 | PA9 | /INHB | TIM1_CH2 | |
| 32 | PA10 | /INHC | TIM1_CH3 | |
| 27 | PB13 | /INLA | TIM1_CH1N | |
| 28 | PB14 | /INLB | TIM1_CH2N | |
| 29 | PB15 | /INLC | TIM1_CH3N | |
| 9 | PA1 | /ISENSE_A | ADC12_IN2 + COMP1_INP | each phase on its own comparator (COMP1/2/4) -> TIM1 BKIN (internal) for overcurrent |
| 15 | PA7 | /ISENSE_B | ADC2_IN4 + COMP2_INP | A/B on ADC2, A/C on ADC1: two phases sample simultaneously |
| 16 | PB0 | /ISENSE_C | ADC1_IN15 + COMP4_INP | |
| 8 | PA0 | /VBUS_SENSE | ADC12_IN1 | |
| 10 | PA2 | /VSENSE_A | ADC1_IN3 | |
| 11 | PA3 | /VSENSE_B | ADC1_IN4 | |
| 12 | PA4 | /VSENSE_C | ADC2_IN17 | |
| 39 | PA15 | /HALL_A | TIM2_CH1 | TIM2 hall-sensor (XOR) mode needs CH1-3 of one timer |
| 40 | PB3 | /HALL_B | TIM2_CH2 | JTDO freed: SWD-only debug |
| 22 | PB10 | /HALL_C | TIM2_CH3 | |
| 41 | PB4 | /ENC_A | TIM3_CH1 | TIM3 encoder mode; JTRST freed |
| 42 | PB5 | /ENC_B | TIM3_CH2 | |
| 46 | PB9 | /ENC_Z | GPIO/EXTI9 | index pulse |
| 43 | PB6 | /UART_TX | USART1_TX | PA9/PA10 are taken by TIM1 |
| 44 | PB7 | /UART_RX | USART1_RX | |
| 37 | PA13 | SWDIO | SWD | J601 |
| 38 | PA14 | SWCLK | SWD | J601 |
| 7 | PG10-NRST | NRST | reset | SW601 to GND + 100 nF to GND; J601 nRESET |
| 45 | PB8-BOOT0 | BOOT0 | strap | 10 k pull-down (boot from flash) |
| 2 | PC13 | USER_SW | GPIO in (pull-up) | SW602 to GND; PC13 sink limit (3 mA) is not loaded |
| 25 | PB11 | LED_STATUS | GPIO out | D602 via 1 k |
| 26 | PB12 | LED_FAULT | GPIO out | D603 via 1 k |
| 24, 36, 48 | VDD | +3V3 | | 100 nF each + one 4.7 uF |
| 23, 35, 47 | VSS | GND | | |
| 21 | VDDA | /VDDA | | ferrite from +3V3, 1 uF + 10 nF |
| 20 | VREF+ | /VDDA | | 1 uF + 100 nF (tied to VDDA; no VREFBUF) |
| 19 | VSSA | GND | | single GND net |
| 1 | VBAT | +3V3 | | tied to VDD (no RTC battery) |

Unused, no-connect: PC14, PC15, PF0, PF1 (HSI clock, no crystal), PA5, PA6, PA11, PA12, PB1, PB2.
SWO is not wired (PB3 is HALL_B). The D601 power LED sits on +3V3 directly via 1 k.
