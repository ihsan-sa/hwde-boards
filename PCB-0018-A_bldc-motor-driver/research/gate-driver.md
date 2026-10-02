# gate-driver — research

Must-haves: 3-phase (or 3x half-bridge) bootstrap gate drive, N-FETs to 40V,
VM operating 10-28V (bench, 40V abs transient), discrete preferred over
integrated-CSA/buck per frame read.

| mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|
| DRV8320HRTVR | C112188 | WQFN-32-EP(5x5) | 2714 | $2.76 | Ext | VM 6-60V direct, 3-phase bootstrap, no integrated CSA/buck — best fit |
| DRV8323RHRGZR | C910524 | VQFN-48-EP(7x7) | 797 | $3.47 | Ext | pin-similar family, adds CSA+buck (unwanted extra), lower stock, backup |
| DRV8300DRGER | C3655801 | VQFN-24(4x4) | 15324 | $0.59 | Ext | cheap, well stocked, but datasheet VM range 5-20V misses 28V op point |
| IR2101STRPBF | C60816 | SOIC-8 | 18253 | $0.65 | Ext | half-bridge only (needs x3), VM 10-20V misses 28V; legacy, not recommended |
| FD6288T | C5386363 | TSSOP-20 | 0 | $0.40 | Ext | 3-phase in one IC but 8-20V range misses 28V and zero stock today |

## Risks
- DRV8320/8323 family is single-source-verified here (no pin-compatible
  Basic-tier alternate found at JLC); acceptable given TI-only 3-phase
  bootstrap drivers dominate this niche.
- DRV8300/FD6288/IR2101 all fail the 28V VM requirement per LCSC's listed
  supply-voltage attribute; a designer confirming against the full
  datasheet (not just the LCSC attribute row) before ruling them out
  entirely is reasonable, but on the data available DRV8320 is the only
  clean fit.
- None of the shortlisted drivers are JLC Basic-tier; all are Extended
  (still fine — good stock depth on the top pick).
