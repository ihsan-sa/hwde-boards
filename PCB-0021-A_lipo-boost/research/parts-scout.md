# Parts scout: charger+power-path and sync boost (PCB-0021-A)

NOTE: scripts/parts_search.py was offline ("JLCPCB search endpoint unreachable, no --db cache"), so all numbers below come from
lcsc.com / jlcpcb.com pages via web search on 2026-10-01 and are NOT parts_search-verified. Stock moves; recheck at P3.
Basic/Extended: every IC here is Extended (JLC Basic is passives and a few discretes only); one extra $3 feeder fee each at assembly.
Prices are LCSC 1+ unless noted.

## Charger with power path (1S Li-ion, 1.5 A, USB input)
| Rank | MPN | LCSC | Pkg | JLC | Stock | Price | Notes |
|---|---|---|---|---|---|---|---|
| 1 | BQ24074RGTR | C54313 | QFN-16 3x3 | Extended | ~1,066 | $1.23 (1+), $0.79 (100+) | OUT 4.4 V fixed, OVP 10.5 V, ITERM pin, 1.5 A. Best fit: keeps OUT < 5 V so boost never passes through. |
| 2 | BQ24072RGTR | C140288 | QFN-16 3x3 | Extended | ~7,970 | "from $0.60" (qty break unclear) | OUT = VBAT+225 mV, OVP 6.6 V. Deeper stock; higher IN->OUT heat at low battery. Same footprint as #1 (drop-in). |
| 3 | BQ24075RGTR | C15464 | QFN-16 3x3 | Extended | ~23,600 | "from $0.57" | OUT fixed 5.5 V: boost would pass-through to ~5.3-5.5 V on USB-A when plugged in. Reject unless the 5 V rail tolerates it. |
| 4 | MCP73871-2CCI/ML | C5121473 | QFN-20 4x4 | Extended | ~112 | $2.79 | Adafruit's part. Low stock, dearest. Reject for stock. |
| alt | IP5306 | C181692 | ESOP-8 | Extended | ~3,860 | $0.14 | One-chip charger+boost power bank SoC (2.1 A chg, 2.4 A out). Cheapest, but no EN pin, no low-batt LED output, auto-shuts at light load (<~50 mA, from memory, unverified), little control. Not a PowerBoost clone; mention only. |

Recommend: BQ24074RGTR, C54313. Fallback if stock dries: BQ24072RGTR C140288 (same footprint, check thermals).
Risks: single vendor (TI), no pin-compatible second source; stock 1k is thin for volume; QFN-16 3x3 with exposed pad (JLC fine).

## Synchronous boost (2.2-5.5 V out, 3.0-4.4 V in, 1 A)
| Rank | MPN | LCSC | Pkg | JLC | Stock | Price | Notes |
|---|---|---|---|---|---|---|---|
| 1 | TPS61023DRLR | C919459 | SOT-563 | Extended | ~41,700 | $0.27 @5, $0.17 @500, $0.15 @2500 | 0.5-5.5 V in, 3.7 A valley, 1 MHz, 94% @3.6 V/5 V, pass-through, true disconnect, 5 V/1.5 A from Li-ion in TI's example. Cheapest, deep stock. 6-pin 1.6x1.6 mm, tight to hand-route; no LBO. |
| 2 | TPS61022RWUR | C915088 | VQFN-7 2x2 | Extended | ~1,186 | $2.56 (1+), $2.15 (1000+) | 8 A valley limit, 94.7%. Overkill and 9x dearer. |
| 3 | TPS61090RSAR | C206167 | QFN-16 4x4 | Extended | ~2,593 | $2.85 (1+), $1.95 (100+) | Adafruit's boost: 2.2 A switch (2.0 A min), has LBI/LBO low-batt comparator, 700 kHz class. Easier to hand-solder; 12x dearer. |

Recommend: TPS61023DRLR, C919459. Single source risk: yes; no pin-compatible drop-in, but TPS61022 (different pkg) is a layout change.
Risk: TPS61023 has no low-battery comparator, so low-batt LED needs a separate detector.

## Supporting parts (to verify at P3, not yet confirmed)
- Inductor 1 uH, Isat >= 4 A, 4x4 mm: FHD4020S-1R0MT C602028 (Changjiang, ~10,200 stock, $0.11 @10; listed 11 A Isat / 6.7 A rated, odd ordering, check datasheet and DCR) ; alt FXL0420-1R0-M C167203 (7 A Isat, 27 mohm DCR, 4.2x4.4 mm); alt Coilcraft XGL4020-102MEC C5357696 (8.8 A, premium price).
- Low-battery detector 3.2 V, open drain SOT-23: XC61CN3202MR-G (Torex), LCSC number not found; one listing showed out of stock at MOQ 3000. Fallbacks: TLV803 family lacks 3.2 V (2.93 V and 4.38 V options only); use a comparator + divider, or a 3.0-3.1 V CMOS detector. P3 must source.
- Passives: all passives (0603/0805 R/C, 22 uF 0805 X5R 10 V, 10 uF, 1.07k/890 ohm resistors) should be JLC Basic where possible; use parts_search --pick basic-passive at P3.
- Connectors: micro-B or USB-C receptacle, USB-A receptacle (THT or SMT), JST-PH 2-pin (B2B-PH-K-S or SMD S2B-PH-SM4): not searched here.
