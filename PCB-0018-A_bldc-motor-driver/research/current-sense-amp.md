# current-sense-amp — research

Must-haves: differential amp for low-side shunts, 3.3V supply, uni or
bidirectional w/ offset, gain 20-50, bandwidth >= 200kHz.

| mpn | lcsc | package | stock | price@1 | Basic/Ext | gain / BW | rationale |
|---|---|---|---|---|---|---|---|
| INA181A2IDBVR | C2058784 | SOT-23-6 | 22358 | $0.33 | Ext | 50V/V / 210kHz | meets both specs at the cheapest price, deep stock — top pick |
| INA181A1IDBVR(XBLW) | C45351496 | SOT-23-6 | 6249 | $0.20 | Ext | 20V/V / 350kHz | low end of gain range, cheapest, no datasheet URL returned (LCSC listing gap) |
| INA240A2DR | C2060768 | SOIC-8 | 6989 | $1.74 | Ext | 50V/V / 400kHz | enhanced PWM common-mode rejection, better for switched motor phases, 5x the price |
| INA240A1DR | C2060769 | SOIC-8 | 27297 | $0.90 | Ext | 20V/V / 400kHz | same PWM-rejection benefit at low gain, deepest stock of the INA240 family |
| INA186A2IDDFR | C2869854 | TSOT-23-8 | 17023 | $0.82 | Ext | 50V/V / 37kHz | fails the >=200kHz bandwidth requirement, excluded |

## Risks
- INA181 is unidirectional-with-offset (fits "unidirectional w/ offset"
  branch of the spec); if bidirectional sensing around 0A is required
  in the final architecture, INA240 (also unidirectional-with-offset
  variants exist, e.g. A2 rated ±) should be re-checked against the
  actual shunt polarity scheme at P2.
- INA181A1(XBLW) returned no datasheet URL from JLC — a variant-suffix
  listing quirk, not a stock issue; verify against TI's INA181 page
  before commit.
- No JLC Basic-tier low-side CSA turned up at this gain/BW combination;
  all candidates are Extended but well stocked.
