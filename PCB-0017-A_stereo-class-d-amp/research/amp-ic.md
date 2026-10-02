# amp-ic — TI class-D amp, pad-down PowerPAD package (orchestrator update)

**Correction to my first pass below**: I had DAD/DAP backwards. Verified independently (web
search of TI's own part-detail pages, not just the earlier assignment note): **DAP = PowerPAD
pad DOWN** (solders to PCB copper, what this design needs), **DAD = PowerPAD pad UP** (needs a
clip-on heatsink). This is the opposite of my first draft's assumption. Orchestrator's power
research caught the same thing and re-pointed the pick to TPA3118D2DAPR; I confirmed it
independently before rewriting this file.

Also confirmed: TPA3116D2 has **no DAP (pad-down) listing on LCSC at all** — every TPA3116D2
part on JLC is DAD (pad-up), which is why the orchestrator moved off it. TPA3118D2 (same family,
lower-power sibling: 30W x2 @ 8ohm vs TPA3116D2's 50W x2 @ 4ohm) does have a DAP part in stock.
TPA3118D2 has no DAD (pad-up) listing on LCSC either — the two part numbers are cleanly split by
package/pad orientation on this platform, so there's no ambiguity once you pick TPA3118D2.

| rank | mpn | lcsc | package | pad orientation | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|---|
| 1 (lead) | TPA3118D2DAPR | C46497 | HTSSOP-32-EP-6.1mm | **DAP = pad-down** (correct for copper heat-sinking) | 38,915 | $1.0751 | Extended | TI genuine, good stock, only pad-down option for this power tier on JLC |
| rejected | TPA3116D2DADR | C50144 | HTSSOP-32-6.1mm | DAD = pad-up (needs a top-side clip heatsink) | 26,775 | $1.0442 | Extended | had the best stock/price of the whole TPA3116D2 family, but the family has no pad-down listing at all — wrong pad orientation for the "copper alone, no clip heatsink" design goal (req Q8) |
| rejected | TPA3116D2DAD | C2865736 | HTSSOP-32-EP-6.1mm | DAD = pad-up | 507 | $1.3187 | Extended | same rejection reason as above; lower stock too |
| not used | TPA3116D2-MNS | C47967307 | HTSSOP-32-6.1mm | unstated (Minos clone) | 652 | $0.7779 | Extended | moot — whole TPA3116D2 family is pad-up only |

No TPA3118D2DAD (pad-up) listing exists on LCSC either — checked, 0 hits. So TPA3118D2DAPR is not
just the best pad-down option, it's the *only* TPA3118D2 package variant JLC stocks at all,
matching the DAP naming with no other option to confuse it with.

## Risks
- Power headroom: TPA3118D2 is rated 30W x2 @ 8ohm vs TPA3116D2's 50W x2 @ 4ohm — lower max
  output. That's an architect-level trade (also eases the "borderline >3A" supply-current flag
  from requirements Q6), not something I resolve here; flagging so P2/architect confirms it still
  meets the speaker-output spec (3A rms / 3.5A peak per the latest update) at the target
  impedance.
- Only Extended parts exist for either TPA3116D2 or TPA3118D2 on JLC — no Basic option at all in
  this IC family, regardless of pad orientation.
- Single JLC-visible source for the lead part (TI genuine, no verified pin-compatible 2nd source
  in the pad-down orientation).
