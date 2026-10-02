# LEARNINGS - PCB-0021-A_lipo-boost (workspace learnings)

Workspace-local. Every entry gets a date, tags (stage tag first: P0-P10), and a
one-line claim as its title. `learnings.py compile --workspace PCB-0021-A_lipo-boost` turns new
entries into `learnings/queue.yaml`; the `promote` verb rules on them.
Research tasks (research.py close) append their entries here automatically.

## 2026-10-01 [P2][research][knowledge][block:B2] research task block-boost-1: 5 verified record(s) for block:B2
Gap: research block 'boost': produce its coverage checklist, then populate it
Operating point: {"board_layers": 2, "control_kind": "cot", "fsw_khz": 1000, "integration_kind": "integrated-fet", "iout_a": 1.0, "pdiss_w": 0.45, "rectifier_kind": "sync", "source_kind": "battery", "switching_kind": "hard", "vin_v": 3.6, "vout_v": 5}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- boost-hot-loop-vout-cap-to-gnd [power-loop] PCB-0021-A_lipo-boost/research/records/boost-hot-loop-vout-cap-to-gnd.yaml
- boost-inductor-and-peak-current [selection] PCB-0021-A_lipo-boost/research/records/boost-inductor-and-peak-current.yaml
- boost-input-output-caps [decoupling] PCB-0021-A_lipo-boost/research/records/boost-input-output-caps.yaml
- boost-passthrough-enable-sequencing [sequencing] PCB-0021-A_lipo-boost/research/records/boost-passthrough-enable-sequencing.yaml
- boost-sw-node-containment [emi] PCB-0021-A_lipo-boost/research/records/boost-sw-node-containment.yaml
Refuted (left draft, not promotable):
- boost-fb-divider-and-feedforward: p5 EC table: VREF is 580/595/610 mV in PWM and 585/601 in PFM (min/typ), not a 585-601 band; record states the PFM min-typ pair as the tolerance. Fix: give 580-610 PWM, 585-601 PFM; R2<300k, FF 1 kHz/40 uF and Fig 10-1 are otherwise correct.
- boost-thermal-copper-and-vias: p4 s6.4 gives RthJA 142.7 C/W (standard) and 91.4 C/W (4-layer 2oz EVM), not cited; record says RthJA unspecified. 0.3-0.55 W loss is unsourced arithmetic (94% eff is quoted at 1.5 A, not 1 A). At 142.7 C/W and 2 layers that loss is 43-78 C rise. Cite p4 numbers, mark 2-layer board vs EVM, label loss as derived.
Draft coverage checklist(s) for the owner to approve:
- boost PCB-0021-A_lipo-boost/research/checklists/boost.yaml (7 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/tps61023.pdf tier vendor-layout sha256 45653870fc7e <https://www.ti.com/lit/ds/symlink/tps61023.pdf>
- research/sources/slva372d.pdf tier vendor-appnote sha256 27f8a71623f2 <https://www.ti.com/lit/an/slva372c/slva372c.pdf>
Task file: PCB-0021-A_lipo-boost/research/tasks/block-boost-1.json

## 2026-10-01 [P2][research][knowledge][block:B1] research task block-linear-charger-power-path-1: 1 verified record(s) for block:B1
Gap: research block 'linear-charger-power-path': produce its coverage checklist, then populate it
Operating point: {"board_layers": 2, "control_kind": "linear", "integration_kind": "integrated-fet", "iout_a": 1.5, "pdiss_w": 1.1, "source_kind": "usb", "vin_v": 5, "vout_v": 4.4}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- linear-charger-input-dpm-and-startup-behaviour [sequencing] PCB-0021-A_lipo-boost/research/records/linear-charger-input-dpm-and-startup-behaviour.yaml
Refuted (left draft, not promotable):
- linear-charger-ilim-iset-programming: p21/p12/p34 re-read: KILIM table 1500/1610/1720 vs worked example 1550 confirmed (example also mislabels RISET). Advice to size with min 1500 is backwards: actual I=K/R can reach 1720/R, so to never exceed the limit use Kmax 1720. Envelope vin max 6.4 is the VI recommended max for 72/73/75/79; for 74 it is 10.2 V (VOVP 10.5), p5/p12/p6.
- linear-charger-pin-caps-ts-and-leds: p35 content correct (10k TS, 1.5k LED to OUT, ~100k pullup, 2x rating). Envelope vin 4.35-6.4 unsupported for the BQ24074-specific record: p5 recommended VI is 4.35-10.2 V for '74, VOVP 10.2-10.8 (p6 EC). Correct envelope or drop the bound.
- linear-charger-single-point-ground-and-current-paths: p40 guidelines correct. Envelope vin max 6.4 wrong for BQ24074 (4.35-10.2 V per p5 EC/p6 comparison table). Also p41 Fig 12-1: ISET pads show no dedicated via (only ILIM-area/TS have one; VSS pads carry vias), so 'each with its own via' overreaches.
- linear-charger-thermal-dissipation-and-pad: p42 Eq 11, 3.4 V rule and thermal-loop advice match. Envelope vin max 6.4 wrong for BQ24074 (10.2 V recommended), and dissipation grows with VIN so the bound hides the worst case. Fix envelope to 4.35-10.2 V.
Draft coverage checklist(s) for the owner to approve:
- linear-charger-power-path PCB-0021-A_lipo-boost/research/checklists/linear-charger-power-path.yaml (6 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/bq24074.pdf tier vendor-layout sha256 4fe4e4f98555 <https://www.ti.com/lit/ds/symlink/bq24074.pdf>
Task file: PCB-0021-A_lipo-boost/research/tasks/block-linear-charger-power-path-1.json
