# LEARNINGS - PCB-0017-A_stereo-class-d-amp (workspace learnings)

Workspace-local. Every entry gets a date, tags (stage tag first: P0-P10), and a
one-line claim as its title. `learnings.py compile --workspace PCB-0017-A_stereo-class-d-amp` turns new
entries into `learnings/queue.yaml`; the `promote` verb rules on them.
Research tasks (research.py close) append their entries here automatically.

## 2026-09-27 [P2][research][knowledge][block:B1] research task block-dc-input-1: 2 verified record(s) for block:B1
Gap: research block 'dc-input': produce its coverage checklist, then populate it
Operating point: {"board_layers": 2, "bulk_kind": "polymer-plus-electrolytic", "cbulk_uf": 200, "connector_kind": "wire-pad", "copper_oz": 2, "esr_bulk_mohm": 30, "hotplug_ring_v_max": 26, "iin_a": 4.0, "protection_kind": "none", "source_kind": "dc-input", "vabs_max_v": 30, "vin_max_v": 13.2, "vin_min_v": 10.8, "vin_v": 12}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- dc-input-bulk-esr-damping-budget [inrush, selection] PCB-0017-A_stereo-class-d-amp/research/records/dc-input-bulk-esr-damping-budget.yaml
- dc-input-hotplug-ring-physics [inrush] PCB-0017-A_stereo-class-d-amp/research/records/dc-input-hotplug-ring-physics.yaml
Draft coverage checklist(s) for the owner to approve:
- dc-input PCB-0017-A_stereo-class-d-amp/research/checklists/dc-input.yaml (6 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/sluaal8.pdf tier vendor-appnote sha256 05ba68c6736a <https://www.ti.com/lit/pdf/sluaal8>
- research/sources/slyt199.pdf tier vendor-appnote sha256 44015908ed38 <https://www.ti.com/lit/pdf/slyt199>
- research/sources/ssztda5.pdf tier vendor-appnote sha256 6caca6c00334 <https://www.ti.com/lit/pdf/ssztda5>
Task file: PCB-0017-A_stereo-class-d-amp/research/tasks/block-dc-input-1.json

## 2026-09-27 [P2][research][knowledge][block:B2] research task block-audio-line-in-1: 4 verified record(s) for block:B2
Gap: research block 'audio-line-in': produce its coverage checklist, then populate it
Operating point: {"board_layers": 2, "cin_uf": 2.2, "coupling_kind": "ac-ceramic", "f_corner_hz": 1.2, "input_kind": "single-ended", "source_kind": "line-level", "vbias_v": 3.0, "vin_vrms": 1.0, "zin_kohm": 60}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- audio-line-in-2layer-switch-node-keepaway [emi] PCB-0017-A_stereo-class-d-amp/research/records/audio-line-in-2layer-switch-node-keepaway.yaml
- audio-line-in-analog-input-star-ground [return-path] PCB-0017-A_stereo-class-d-amp/research/records/audio-line-in-analog-input-star-ground.yaml
- audio-line-in-cap-corner-vs-popup-settle [selection] PCB-0017-A_stereo-class-d-amp/research/records/audio-line-in-cap-corner-vs-popup-settle.yaml
- audio-line-in-single-ended-unused-leg-ac-ground [diff-pair] PCB-0017-A_stereo-class-d-amp/research/records/audio-line-in-single-ended-unused-leg-ac-ground.yaml
Draft coverage checklist(s) for the owner to approve:
- audio-line-in PCB-0017-A_stereo-class-d-amp/research/checklists/audio-line-in.yaml (4 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/tpa3116d2.pdf tier vendor-layout sha256 4339471f438d <https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf>
- research/sources/slaa719.pdf tier vendor-appnote sha256 9de0d36defac <https://www.ti.com/lit/an/slaa719/slaa719.pdf>
- research/sources/slaa896.pdf tier vendor-appnote sha256 eb3735d9a2a2 <https://www.ti.com/lit/an/slaa896/slaa896.pdf>
Task file: PCB-0017-A_stereo-class-d-amp/research/tasks/block-audio-line-in-1.json

## 2026-09-27 [P2][research][knowledge][block:B4] research task block-lc-output-filter-1: 9 verified record(s) for block:B4
Gap: research block 'lc-output-filter': produce its coverage checklist, then populate it
Operating point: {"board_layers": 2, "c_nf": 680, "copper_oz": 2, "damping_c_nf": 10, "damping_kind": "zobel-rc", "damping_r_ohm": 3.3, "dcr_mohm": 66, "f0_khz": 61, "filter_kind": "lc-second-order", "fsw_khz": 400, "il_pk_a": 3.5, "inductor_body_mm": 7.3, "inductor_kind": "shielded-power", "ioc_trip_a": 7.5, "iout_a": 3.0, "isat_min_a": 4.0, "l_min_at_trip_uh": 1.0, "l_uh": 10, "output_kind": "btl", "rload_ohm_min": 4, "rload_ohm_typ": 8}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- lc-output-filter-butterworth-pairing [selection] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-butterworth-pairing.yaml
- lc-output-filter-cap-voltage-dc-bias [selection] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-cap-voltage-dc-bias.yaml
- lc-output-filter-constraints-emission [constraints-emission] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-constraints-emission.yaml
- lc-output-filter-dcr-dissipation [thermal] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-dcr-dissipation.yaml
- lc-output-filter-ground-return-2layer [return-path] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-ground-return-2layer.yaml
- lc-output-filter-inductor-isat-and-min-l [selection] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-inductor-isat-and-min-l.yaml
- lc-output-filter-placement-and-loop [emi] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-placement-and-loop.yaml
- lc-output-filter-q-tracks-load [selection] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-q-tracks-load.yaml
- lc-output-filter-snubber-networks [emi] PCB-0017-A_stereo-class-d-amp/research/records/lc-output-filter-snubber-networks.yaml
Draft coverage checklist(s) for the owner to approve:
- lc-output-filter PCB-0017-A_stereo-class-d-amp/research/checklists/lc-output-filter.yaml (5 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/slaa701b.pdf tier vendor-appnote sha256 c0b700ff0643 <https://www.ti.com/lit/an/sloa119b/sloa119b.pdf>
- research/sources/tpa3116d2.pdf tier vendor-layout sha256 4339471f438d <https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf>
- research/sources/slou336b.pdf tier vendor-layout sha256 7c23a786f2f3 <https://www.ti.com/lit/ug/slou336b/slou336b.pdf>
- research/sources/doc1404_classd.pdf tier cross-vendor sha256 951968970d51 <https://www.coilcraft.com/getmedia/4dde0ed8-535d-4960-bf95-2b450f1fe702/doc1404_classd.pdf>
Task file: PCB-0017-A_stereo-class-d-amp/research/tasks/block-lc-output-filter-1.json

## 2026-09-27 [P2][research][knowledge][block:B3] research task block-class-d-amp-1: 10 verified record(s) for block:B3
Gap: research block 'class-d-amp': produce its coverage checklist, then populate it
Operating point: {"board_layers": 2, "channels": 2, "cooling_kind": "natural-convection", "copper_oz": 2, "edge_ns": 15, "fault_kind": "self-clearing", "fsw_khz": 400, "gain_db": 20, "iin_a": 4.0, "integration_kind": "integrated-fet", "iout_a": 3.0, "limit_kind": "none", "modulation_kind": "bd", "output_kind": "btl", "package_kind": "powerpad-down", "pdiss_max_w": 4.2, "pdiss_w": 1.5, "pout_w_per_ch_4ohm": 15.6, "pout_w_per_ch_8ohm": 8.4, "rds_on_mohm": 120, "rload_ohm_min": 4, "rload_ohm_typ": 8, "rth_ja_target_cw": 56.7, "source_kind": "dc-input", "switching_kind": "hard", "ta_c": 40, "tj_max_c": 125, "vin_max_v": 13.2, "vin_min_v": 10.8, "vin_v": 12}
Missing classes: coverage-checklist

Verified records (second reader signed). Promotion = the research verb's promote step (copies record + sources into the library), then the queue ruling with kind knowledge_record targeting reference/knowledge/records/<id>.yaml, then the owner's approval block:
- class-d-amp-2layer-pour-heat-spreader [thermal] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-2layer-pour-heat-spreader.yaml
- class-d-amp-bootstrap-cap-per-output [feedback, decoupling] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-bootstrap-cap-per-output.yaml
- class-d-amp-constraints-emission [constraints-emission] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-constraints-emission.yaml
- class-d-amp-emi-filter-and-snubber [emi] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-emi-filter-and-snubber.yaml
- class-d-amp-family-pad-orientation-selection [selection, thermal] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-family-pad-orientation-selection.yaml
- class-d-amp-fault-latch-self-clear [sequencing] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-fault-latch-self-clear.yaml
- class-d-amp-output-loop-star-ground [power-loop, return-path] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-output-loop-star-ground.yaml
- class-d-amp-powerpad-thermal-via-array [thermal-via] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-powerpad-thermal-via-array.yaml
- class-d-amp-pvcc-three-tier-decoupling [decoupling] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-pvcc-three-tier-decoupling.yaml
- class-d-amp-single-gnd-two-layer-pour [return-path] PCB-0017-A_stereo-class-d-amp/research/records/class-d-amp-single-gnd-two-layer-pour.yaml
Draft coverage checklist(s) for the owner to approve:
- class-d-amp PCB-0017-A_stereo-class-d-amp/research/checklists/class-d-amp.yaml (10 classes)
Sources (quarantined, sha-pinned in the task ledger):
- research/sources/tpa3116d2.pdf tier vendor-layout sha256 4339471f438d <https://www.ti.com/lit/ds/symlink/tpa3116d2.pdf>
- research/sources/slma002h.pdf tier vendor-appnote sha256 cdab5db91631 <https://www.ti.com/lit/an/slma002h/slma002h.pdf>
- research/sources/slou342a.pdf tier vendor-layout sha256 f811b6fcdf1c <https://www.ti.com/lit/ug/slou342a/slou342a.pdf>
Task file: PCB-0017-A_stereo-class-d-amp/research/tasks/block-class-d-amp-1.json
