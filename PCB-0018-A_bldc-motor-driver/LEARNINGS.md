# LEARNINGS - PCB-0018-A_bldc-motor-driver (workspace learnings)

Workspace-local. Every entry gets a date, tags (stage tag first: P0-P10), and a
one-line claim as its title. `learnings.py compile --workspace PCB-0018-A_bldc-motor-driver` turns new
entries into `learnings/queue.yaml`; the `promote` verb rules on them.
Research tasks (research.py close) append their entries here automatically.

## 2026-09-27 [P2][research][knowledge][block:gate_driver] research task block-gate-driver-bootstrap-1: 4 verified record(s) for block:gate_driver
Gap: research block 'gate-driver-bootstrap': produce its coverage checklist, then populate it
Operating point: {"board_layers": 4, "edge_ns": 50, "fsw_khz": 25, "pdiss_w": 0.1, "source_kind": "dc-input", "switching_kind": "hard", "vin_v": 28, "vout_v": 12}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- gate-driver-bootstrap-cboot-sizing [selection] PCB-0018-A_bldc-motor-driver/research/records/gate-driver-bootstrap-cboot-sizing.yaml
- gate-driver-bootstrap-charge-loop [power-loop, decoupling] PCB-0018-A_bldc-motor-driver/research/records/gate-driver-bootstrap-charge-loop.yaml
- gate-driver-bootstrap-gate-routing [emi, power-loop] PCB-0018-A_bldc-motor-driver/research/records/gate-driver-bootstrap-gate-routing.yaml
- gate-driver-bootstrap-gvdd-bypass-ratio [decoupling] PCB-0018-A_bldc-motor-driver/research/records/gate-driver-bootstrap-gvdd-bypass-ratio.yaml
Draft coverage checklist(s) for the owner to approve:
- gate-driver-bootstrap PCB-0018-A_bldc-motor-driver/research/checklists/gate-driver-bootstrap.yaml (4 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/drv8300.pdf tier vendor-layout sha256 bb467652a531 <https://www.ti.com/lit/ds/symlink/drv8300.pdf>
- research/sources/slua887a.pdf tier vendor-appnote sha256 2b4478dc5ce8 <https://www.ti.com/lit/an/slua887/slua887.pdf>
Task file: PCB-0018-A_bldc-motor-driver/research/tasks/block-gate-driver-bootstrap-1.json

## 2026-09-27 [P2][research][knowledge][block:sensing] research task block-current-sense-shunt-1: 7 verified record(s) for block:sensing
Gap: research block 'current-sense-shunt': produce its coverage checklist, then populate it
Operating point: {"board_layers": 4, "bw_khz": 400, "gain_vv": 20, "iout_a": 10, "ipeak_a": 20, "rshunt_mohm": 3}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- current-sense-shunt-constraints-emission [constraints-emission] PCB-0018-A_bldc-motor-driver/research/records/current-sense-shunt-constraints-emission.yaml
- current-sense-shunt-csa-bypass [decoupling] PCB-0018-A_bldc-motor-driver/research/records/current-sense-shunt-csa-bypass.yaml
- current-sense-shunt-diff-pair-routing [diff-pair, emi] PCB-0018-A_bldc-motor-driver/research/records/current-sense-shunt-diff-pair-routing.yaml
- current-sense-shunt-filter-series-r [emi, selection] PCB-0018-A_bldc-motor-driver/research/records/current-sense-shunt-filter-series-r.yaml
- current-sense-shunt-kelvin-taps [return-path] PCB-0018-A_bldc-motor-driver/research/records/current-sense-shunt-kelvin-taps.yaml
- current-sense-shunt-lowside-placement [power-loop, return-path] PCB-0018-A_bldc-motor-driver/research/records/current-sense-shunt-lowside-placement.yaml
- current-sense-shunt-selection-ladder [selection] PCB-0018-A_bldc-motor-driver/research/records/current-sense-shunt-selection-ladder.yaml
Draft coverage checklist(s) for the owner to approve:
- current-sense-shunt PCB-0018-A_bldc-motor-driver/research/checklists/current-sense-shunt.yaml (7 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/ina240.pdf tier vendor-layout sha256 c9d26e72ebdb <https://www.ti.com/lit/ds/symlink/ina240.pdf>
- research/sources/slva959b.pdf tier cross-vendor sha256 89adbce11092 <https://www.ti.com/lit/an/slva959b/slva959b.pdf>
Task file: PCB-0018-A_bldc-motor-driver/research/tasks/block-current-sense-shunt-1.json

## 2026-09-27 [P2][research][knowledge][block:power_in] research task block-reverse-polarity-fet-1: 6 verified record(s) for block:power_in
Gap: research block 'reverse-polarity-fet': produce its coverage checklist, then populate it
Operating point: {"board_layers": 4, "integration_kind": "controller", "iout_a": 12.2, "pdiss_w": 0.4, "source_kind": "dc-input", "vin_v": 28}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- reverse-polarity-fet-conduction-thermal-budget [thermal] PCB-0018-A_bldc-motor-driver/research/records/reverse-polarity-fet-conduction-thermal-budget.yaml
- reverse-polarity-fet-constraints-emission [constraints-emission] PCB-0018-A_bldc-motor-driver/research/records/reverse-polarity-fet-constraints-emission.yaml
- reverse-polarity-fet-controller-gate-vcap-placement [decoupling] PCB-0018-A_bldc-motor-driver/research/records/reverse-polarity-fet-controller-gate-vcap-placement.yaml
- reverse-polarity-fet-current-path-copper [power-loop, thermal] PCB-0018-A_bldc-motor-driver/research/records/reverse-polarity-fet-current-path-copper.yaml
- reverse-polarity-fet-nfet-and-tvs-selection [selection, inrush] PCB-0018-A_bldc-motor-driver/research/records/reverse-polarity-fet-nfet-and-tvs-selection.yaml
- reverse-polarity-fet-no-blocking-for-regen-load [selection] PCB-0018-A_bldc-motor-driver/research/records/reverse-polarity-fet-no-blocking-for-regen-load.yaml
Draft coverage checklist(s) for the owner to approve:
- reverse-polarity-fet PCB-0018-A_bldc-motor-driver/research/checklists/reverse-polarity-fet.yaml (6 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/lm74500-q1.pdf tier vendor-layout sha256 9468bb5e0c1f <https://www.ti.com/lit/ds/symlink/lm74500-q1.pdf>
- research/sources/and90146-d.pdf tier cross-vendor sha256 5dbcd17d1f30 <https://www.onsemi.com/download/application-notes/pdf/and90146-d.pdf>
Task file: PCB-0018-A_bldc-motor-driver/research/tasks/block-reverse-polarity-fet-1.json

## 2026-09-27 [P2][research][knowledge][block:power_stage] research task block-half-bridge-inverter-1: 2 verified record(s) for block:power_stage
Gap: research block 'half-bridge-inverter': produce its coverage checklist, then populate it
Operating point: {"board_layers": 4, "edge_ns": 50, "fsw_khz": 25, "integration_kind": "controller", "iout_a": 10, "ipeak_a": 20, "pdiss_w": 2.3, "rectifier_kind": "sync", "source_kind": "dc-input", "switching_kind": "hard", "vin_v": 28}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- half-bridge-inverter-leg-hot-loop [power-loop, decoupling] PCB-0018-A_bldc-motor-driver/research/records/half-bridge-inverter-leg-hot-loop.yaml
- half-bridge-inverter-thermal-copper-vias [thermal, thermal-via] PCB-0018-A_bldc-motor-driver/research/records/half-bridge-inverter-thermal-copper-vias.yaml
Refuted (left draft, not promotable):
- half-bridge-inverter-switch-node-damping: envelope vin_v 10-48V is unsupported: tiduf36a.pdf p1/p2 state the design operates 5V to 21V (18V nominal) with 40V-rated FETs (p5); no cited page mentions 48V or a 60V FET class, so the upper bound is an invented extrapolation, not a source-derived scaling limit. Rule content itself (snubber/Rg/loop) matches p26-27 SLVA959B and p5/p17 TIDUF36A verbatim.
Draft coverage checklist(s) for the owner to approve:
- half-bridge-inverter PCB-0018-A_bldc-motor-driver/research/checklists/half-bridge-inverter.yaml (5 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/slva959b.pdf tier vendor-appnote sha256 89adbce11092 <https://www.ti.com/lit/an/slva959b/slva959b.pdf>
- research/sources/tiduf36a.pdf tier vendor-layout sha256 1855b9a45799 <https://www.ti.com/lit/ug/tiduf36a/tiduf36a.pdf>
Task file: PCB-0018-A_bldc-motor-driver/research/tasks/block-half-bridge-inverter-1.json

## P7 routing (2026-09-27)
- route_critical --only diff reported status "pass" for the three Kelvin current-sense pairs (ISNS_x_P/N) while routing nothing: each net is one net-tie pad (NT40x) plus one amp pin, unmatched_stub_pads() detaches the net-tie pads as stubs, the net is left with one pad, and KRT's already_routed is taken as success. Check diffpair_facts[].routed and the unconnected count, not the status. Fix belongs in hwde (a pair whose only far-end pads are net-tie pads should not detach them).
- KRT's per-call timeout (600 s default) is too short on a loaded box for a 16-net power pass; split with --only and raise --timeout-s.
- route_critical --only power timed out three times (600 s, 1500 s, and 1800 s at grid 0.1) on this 78 mm board at box load 60-140. Motor-driver phase, shunt and input nets went in as planes_gen region pours instead (constraints "planes" entries with "region" and "connect": "solid"), tied between F.Cu and B.Cu by stitch_vias area vias; for 10 A nets that is also the better copper.
- stitch_vias --nets GND fails its post-apply verify and rolls back: its area grid puts GND vias inside the NTMFS5C628NL drain tabs (pad 5, VM) and a few other foreign pads, the worker drops them, and the verify then misses them. The workaround was --dry-run, drop every via within 0.42 mm of a foreign pad's bbox, and apply the rest with route_edit. Stitching several nets in one call fails the same way.
