# output-filter-cap — LC filter cap + Zobel damping RC, per channel (x2)

**Correction to my first pass**: I initially mislabeled "10 ohm + 330 pF" as the reference design's damping/
Zobel branch, sourced from a web-search summary of the TI E2E forum. The refdesign-amp research
(which read the actual TI datasheet, TI's EVM BOM, and JLCPCB's own blog post) found this is
wrong — there are **two distinct RC networks**, and I had conflated them:
- **Damping/Zobel branch, at the filter output** (what requirements.md's "damping branch" and
  the reference design's reported parts list actually mean): **3.3 ohm + 10 nF**, per TI's EVM BOM (R15-R18 +
  C25-C28) and matching the reference design's own reported parts exactly.
- **Switch-node EMI snubber, right at the IC's output pins** (before the inductor, TI datasheet
  section 7.3.14): TI's own suggested value is 18 ohm + 330 pF; the TI EVM actually implements
  10 ohm + 330 pF instead. This is a *separate, optional* network — **the reference design's reported parts list
  does not include it**, so it's not required to match the reference design's BOM/part-count, but the architect
  may still want it for EMI margin; noted as optional below, not as the primary Zobel branch.

LC filter cap value (10 uH + 680 nF) is unaffected by the correction above and is independently
confirmed by refdesign-amp's read of the datasheet's own BTL test condition — matches what I had.

## LC filter cap: 680 nF (0.68 uF), X7R, >=50V
No JLC Basic part exists at this value (checked "0.68uF" and "680nF" basic-only, both empty).

| rank | mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|
| 1 | CC0805KKX7R9BB684 | C107133 | 0805 | 15,895 | $0.0389 | Extended | YAGEO, best stock of the 0.68uF/50V parts |
| 2 | TCC0805X7R684K500DT | C282780 | 0805 | 10,944 | $0.0174 | Extended | CCTC, cheapest, good stock |
| 3 | CC1206KKX7R9BB684 | C145012 | 1206 | 18,619 | $0.0618 | Extended | YAGEO, best stock overall but larger 1206 footprint |

## Damping/Zobel branch (primary, matches the reference design's BOM): 3.3 ohm + 10 nF
| rank | mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|
| 1 | RC0603FR-073R3L | C137725 | 0603 | 159,062 | $0.0072 | Extended | 3.3 ohm, best stock; no Basic 3.3 ohm resistor exists at any package (checked) |
| 2 | RS-03L3R30FT | C140101 | 0603 | 37,615 | $0.0039 | Extended | 3.3 ohm alt, cheaper, less stock |
| 3 | CL05B103KB5NNNC | C15195 | 0402 | 4,457,219 | $0.005 | **Basic** | 10 nF X7R 50V, smallest Basic footprint at value |
| 4 | 0603B103K500NT | C57112 | 0603 | 7,105,220 | $0.0108 | **Basic** | 10 nF alt, 0603, huge stock |

## Switch-node EMI snubber (optional, not in the reference design's BOM): 10 ohm + 330 pF
Already scouted in my first pass — kept here since both parts are JLC Basic and the values are
still correct for this (different) network, just re-labeled correctly:

| rank | mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|
| 1 | 0603WAF100JT5E | C22859 | 0603 | 8,506,972 | $0.0032 | **Basic** | 10 ohm, huge stock, cheapest |
| 2 | CL10C331JB8NNNC | C1664 | 0603 | 914,400 | $0.0179 | **Basic** | 330 pF C0G 50V, only Basic hit at this value |

## Risks
- The 0.68uF LC-filter cap has no Basic option; it is the one part in this block that drives an
  Extended-part fee.
- The 3.3 ohm Zobel resistor also has no Basic option at any package I checked (0402/0603/0805/
  1206) — flag if the architect wants to swap to a Basic-only BOM; the nearest Basic values would
  be off-value (e.g. 1 ohm or 4.7 ohm) and change the damping behavior, not a drop-in substitute.
- Whether to include the optional switch-node snubber (10 ohm + 330 pF) is an architect decision,
  not mine — it adds 4 parts (2 per channel) beyond the reference design's reported ~40-part count and would be a
  stated deviation in COMPARISON.md if added.
