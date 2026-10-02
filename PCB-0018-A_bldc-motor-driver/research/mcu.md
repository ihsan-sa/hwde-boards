# mcu — research

Must-haves: STM32G431CBT6/G474 class, LQFP-48/64, FOC-capable timers/ADC.

| mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|
| STM32G431CBT6 | C529355 | LQFP-48(7x7) | 2043 | $5.38 | Ext | exact requested part, FOC-class G4, 128KB flash — top pick |
| STM32G474RBT3 | C1235414 | LQFP-64(10x10) | 2082 | $4.02 | Ext | same family, more pins/peripherals, cheaper and better stocked |
| STM32G474CBT6 | C730123 | LQFP-48_7x7 | 730 | $4.28 | Ext | G474 features, same LQFP-48 footprint, lower stock |
| STM32G431C8T6 | C730096 | LQFP-48(7x7) | 1176 | $7.46 | Ext | half the flash for more money than the CB — dominated, skip |
| STM32G431KBU6 | C529358 | UFQFPN-32(5x5) | 3643 | $8.96 | Ext | smaller package, best stock, but pricier and off the requested package class |

## Risks
- None of the G4-family parts are JLC Basic-tier; all Extended, but stock
  is healthy (700-3600 units) across every candidate — no supply risk
  at prototype qty (5 boards).
- STM32G431CBT6 and STM32G474RBT3 are close in price/stock; final choice
  is a peripheral-count/pin-count tradeoff for P2/P3, not availability.
