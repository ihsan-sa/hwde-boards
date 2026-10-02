# P0 Intake digest - esp32c3-node (2026-10-01)

- Artifact: `requirements.md` (9 sections); `check_requirements.py` PASS, 0 violations
  (`log/check_requirements-P0.json`).
- Mode: no token -> mode none; product scope; XIAO size recorded SOFT (no HARD cap).
- Safety flags: BATTERY applies (1S LiPo charging), RF TRANSMIT applies (pre-certified
  module, antenna keep-out binding). Mains / motors / >30 V / >3 A not applicable.
- Battery unknowns answered PROVISIONALLY by delegate, conservative: 4.20 V, ~400 mAh
  class, charge <= 200 mA (0.5C), no NTC (protected cell + charger thermal regulation),
  no active reverse-battery element (silk polarity) - all re-confirmed at H1.
- Other OPEN answers: indoor 0-40 C, Qwiic 100 mA, qty 5, size soft, plated THT edge
  pads (no castellation), 1.6 mm.
- One agent plays P0-P3 roles (spend cap) - recorded decision.
