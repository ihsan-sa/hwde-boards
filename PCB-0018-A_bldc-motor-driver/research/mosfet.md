# mosfet — research

Must-haves: 40V N-channel, Rds(on) <= 5mOhm, 5x6 power package
(PDFN/DFN5x6/SO-8FL), logic or standard level, well stocked at JLC.

| mpn | lcsc | package | stock | price@1 | Basic/Ext | Rds(on) | rationale |
|---|---|---|---|---|---|---|---|
| TDM3436 | C380232 | DFN-8(5x6) | 11034 | $0.57 | Ext | 4.1mOhm@4.5V | meets spec, logic-level, cheap, well stocked — top pick |
| NTMFS5C410NLT1G | C348540 | SO-8FL | 4004 | $1.08 | Ext | 1.2mOhm@4.5V | best-in-class Rds(on), onsemi auto-grade, higher price |
| HY1904C2 | C358116 | PPAK-8L(5x6) | 6208 | $0.26 | Ext | 7mOhm@4.5V | cheapest, but over the 5mOhm target |
| AON6236 | C131413 | DFN-8(5x6) | 2916 | $0.48 | Ext | 10.5mOhm@10V | over spec, lower stock |
| WSD4062DN56 | C377871 | DFN5x6-8L | 4998 | $0.35 | Ext | 13.5mOhm@4.5V | well over spec, cheap backup only |

## Risks
- No JLC Basic-tier 40V/5x6/<=5mOhm part turned up; all candidates are
  Extended. Stock is deep on the top two so this is a price/logistics
  note, not a supply risk.
- TDM3436 (Techcode) is a lesser-known brand vs. NTMFS (onsemi) — if
  brand-name assurance matters more than price, NTMFS5C410NLT1G is the
  safer single-source swap at the same footprint (SO-8FL vs DFN5x6, both
  5x6mm, pinout should be checked against the chosen footprint).
- Only one function's shunt-referenced Rds(on) test condition (Vgs) varies
  across parts (4.5V vs 10V); confirm actual gate-drive voltage from the
  gate-driver pick before finalizing, since Rds(on) rises at lower Vgs.
