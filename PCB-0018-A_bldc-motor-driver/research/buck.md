# buck — research

Must-haves: VM (10-28V op, 40V abs) to 3.3V/5V at ~0.5-1A, small, JLC
stocked.

| mpn | lcsc | package | stock | price@1 | Basic/Ext | Vin range | rationale |
|---|---|---|---|---|---|---|---|
| TPS54331DR | C9865 | SOIC-8 | 345196 | $0.34 | Ext | 3.5-28V | direct VM input, 3A, huge stock, cheap — top pick |
| MP1584EN-LF-Z | C15051 | SOIC-8-EP | 2335 | $2.92 | Ext | 4.5-28V | same input coverage, ~9x price, far less stock — backup |
| MP2315GJ-Z-JSM | C49367820 | TSOT-23-8 | 2103 | $0.47 | Ext | 4-24V | misses top of 28V range, excluded |
| TPS563201DDCR | C116592 | SOT-23-THIN-6 | 165036 | $0.07 | Ext | 4.5-17V | can't take VM directly; fine only for a post-regulated 5V rail |
| AP62200TWU-7 | C2895288 | TSOT-26 | 31062 | $0.20 | Ext | 4.2-18V | same VM limitation as TPS563201 |

## Risks
- The 40V abs-max transient requirement was checked only via the LCSC
  "Voltage - Supply" attribute (operating range), not the full datasheet
  abs-max table; TPS54331's datasheet abs max Vin is commonly cited at
  ~40V in this family, but confirm against the actual TI datasheet
  before layout.
- No JLC Basic-tier part meeting the full VM range turned up; the two
  parts that do (TPS54331, MP1584) are both Extended. TPS54331 has by
  far the deeper stock and lower price so this isn't a real risk.
- If the design ends up wanting VM->5V and 5V->3.3V in two stages, the
  <28V-only parts (TPS563201, AP62200) become excellent second-stage
  candidates — worth keeping on file for P2.
