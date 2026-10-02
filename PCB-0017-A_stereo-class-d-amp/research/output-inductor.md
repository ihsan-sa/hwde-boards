# output-inductor — 10 uH shielded power inductor, per channel (x2)

Spec: 10 uH, shielded SMD, Isat >= 4 A, Irms >= 3 A, low DCR, JLC-stocked, smallest footprint that
clears the spec (this sizes the board around the output filter, alongside the amp IC's thermal
pad). Orchestrator refined the speaker-output spec to 3A rms / 3.5A peak per channel — that's
covered by the same Isat>=4A / Irms>=3A floor already used below (Isat >= 4A gives >=0.5A margin
over the 3.5A peak on every part that clears the floor; the 5.5A-Isat parts, #1-#3, give 2A of
margin over peak).

Swept two size tiers below the spec floor before landing on the one that clears it, to show the
floor is real, not just unsearched:
- 4x4mm and smaller (SWPA/NR4018 series): best case Isat 2.9A (SWPA5040, 5x5mm) — fails Isat.
- 6x6mm (SWPA6045S100MT): Isat 3.5A — still fails Isat.
- 5.5x5.2mm Vishay IHLP2020CZER100MA1: Isat 4A (passes) but Irms(rated) 2.5A — fails Irms.
- **7x6.6mm class is the smallest footprint where both Isat >= 4A and Irms >= 3A are met** on
  JLC today for a 10uH shielded part.

| rank | mpn | lcsc | package | Isat | Irms(rated) | DCR | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SLO0630H100MTT | C207842 | SMD 7.3x6.6mm | 5.5A | 4A | 66mΩ | 16,183 | $0.1116 | Extended | best stock+price+margin at the size floor |
| 2 | MHCI06030-100M-R8A | C108290 | SMD 7.3x6.6mm | 5.5A | 4A | 68mΩ | 9,210 | $0.1326 | Extended | Chilisin alt source, near-identical specs to #1, good stock |
| 3 | CMLO0630H100MTT | C439002 | SMD 7x6.6mm | 5.5A | 4A | 66mΩ | 3,747 | $0.1116 | Extended | slightly smaller footprint than #1/#2, same specs, lower stock |
| 4 | AMRU00060630100MA1 | C2981193 | SMD 7.3x6.8mm | 5A | 4A | 62mΩ | 7,296 | $0.2696 | Extended | lowest DCR (best efficiency), Chilisin premium line, 2.4x price of #1 |
| 5 | MWSA0624S-100MT | C408435 | SMD 7x6.6mm | 4A | 3.1A | 101mΩ | 3,498 | $0.1191 | Extended | thinnest margin that still clears spec (Irms 3.1A vs 3A floor); higher DCR than 1-4, listed as compact alternate only |

FYI: TI's own EVM uses a 5.8A-Isat-rated part (Toko 931BS-100M, per the power-architect's read of
the EVM BOM) as its reference inductor — picks #1-#4 here (5-5.5A Isat) land close to that
reference, not just at the bare 4A floor.

## Risks
- No JLC Basic part meets the Isat/Irms floor at any size; all 5 candidates are Extended.
- #1-#3 are functionally interchangeable (same footprint, near-identical Isat/Irms/DCR) —
  low single-source risk, three viable suppliers at this spec.
- #5 is included only to show the size/margin trade explicitly; #1 is the recommended pick unless
  board area is desperately tight, in which case #3 (7x6.6mm, same margin as #1) is the better
  compact choice over #5 (thinner current margin, worse DCR).
