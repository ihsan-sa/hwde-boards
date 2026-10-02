# P1 digest
- One combined sonnet researcher (power-architect + scout + reference-design) to save spend: research/power.md, parts-scout.md, reference-adafruit-powerboost1000c.md.
- Charger/power-path: BQ24074RGTR C54313 (OUT regulated 4.4 V, so boost never passes USB through); fallback BQ24072RGTR C140288.
- Boost: TPS61023DRLR C919459 (SOT-563, 3.7 A valley limit, ~94 %); inductor 1 uH Isat >= 4 A, to verify.
- Reference: Adafruit PowerBoost 1000C, CC BY-SA 3.0 Unported; MCP73871 + TPS61090.
- Gaps for P2/P3: low-battery detector (TPS61023 has no LBO), DONE LED (BQ24074 has CHG + PGOOD only), TS tied to 10k (no NTC, same as reference), charger heat ~1.1 W.
- Prices/stock from LCSC web 2026-10-01 (parts_search offline); re-verify at P3.
