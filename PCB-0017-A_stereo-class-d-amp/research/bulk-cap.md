# bulk-cap — 2x 100 uF >= 25 V PVCC bulk, per orchestrator update

Orchestrator specified two 100uF>=25V caps of different technology per PVCC bulk site (not
alternates of each other): one **polymer, ripple current >= 2A** (handles the switching-frequency
ripple with low ESR) and one **low-ESR electrolytic** (bulk low-frequency storage, cheap, small).
Compared electrolytic vs polymer vs ceramic first (see below), then picked one of each per the
orchestrator's spec.

## Cap A — polymer, ripple >= 2A, >= 25V
Filtered JLC's SMD (not through-hole "Plugin") 100uF/25V polymer parts by rated ripple current;
most listings on JLC don't publish a ripple-current attribute at all, so this table only includes
ones that do, to avoid guessing:

| rank | mpn | lcsc | package | ripple (100kHz) | ESR | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MA25V100M6x6 | C46550465 | SMD D6.3xL6mm | 2.65A | 30mΩ@100kHz | 61,325 | $0.1685 | Extended | meets both the >=2A ripple floor and the 30mOhm ESR ceiling exactly; best stock of the group |
| 2 | SVS1EM101E06E00RAXXX | C2939798 | SMD D6.3xL6mm | 2.2A | 45mΩ@100kHz | 20,035 | $0.1803 | Extended | same footprint, thinner ripple margin and higher ESR than #1, less stock |

Two SMD polymer parts (SVZ1EM101E06E00RAXXX C320569, OVZ101M1ETR-0606 C164071) are rated 25V and
otherwise similar but LCSC doesn't publish their ripple spec — excluded rather than assumed. One
option, SA11AM101A19R15XXX (C135491), has the best ESR/ripple/footprint (15mOhm, 2.5A, 7.3x4.3mm)
of anything checked but is only 10V-rated — fails the >=25V floor, not usable here.

## Cap B — low-ESR electrolytic, >= 25V
JLC's SMD electrolytics only publish ripple current at 120Hz (mains-rectifier rating, tens of mA)
rather than an ESR figure at switching frequency — none of the general-purpose electrolytics I
checked are branded "low-ESR" or publish an ESR attribute. Flagging this as a data gap rather than
guessing a number:

| rank | mpn | lcsc | package | stock | price@1 | Basic/Ext | rationale |
|---|---|---|---|---|---|---|---|
| 1 | RVT100UF35V167RV0082 | C5138965 | SMD D6.3xL5.4mm | 291,726 | $0.0514 | Extended | best stock of any 100uF electrolytic checked, compact can, 35V gives margin over 25V floor |
| 2 | RST100UF25V004 | C4747964 | SMD D6.3xL5.4mm | 162,793 | $0.0411 | Extended | cheapest, same footprint, exactly-25V rated |

**Open for P2/architect**: JLC doesn't surface a 100kHz-ESR spec for any SMD electrolytic in this
search; if a specific ESR ceiling matters, that has to come from the manufacturer's own datasheet
(KNSCHA for #1/#2), not from the LCSC listing.

## Technology trade (electrolytic vs polymer vs ceramic), for context
- Electrolytic: cheapest, smallest footprint for 100uF@25-35V, deepest stock — the bulk-storage
  choice.
- Polymer: 2-4x the price, similar footprint, real ripple/ESR specs at switching frequency —
  the ripple-duty choice (Cap A above).
- Ceramic stack: reaching 100uF at 25V+ needs several 22-47uF X7R MLCCs (1210/2220-class,
  heavily DC-bias-derated at 25V) — more parts, more footprint, more cost than one electrolytic
  can for the same capacitance; not used here.

## Risks
- No JLC Basic part exists for 100uF>=25V in any technology — both caps are Extended.
- Ripple/ESR data gaps noted above; do not assume a number where JLC's listing doesn't provide
  one.
