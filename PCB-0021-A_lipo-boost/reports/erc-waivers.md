# ERC waivers PCB-0021-A
ERC gate passed with 0 failing. The review warnings (no input fuse/TVS, no reverse-battery FET, no 5 V limit, timer spread) are accepted per the PROVISIONAL P2 decision 'no PTC/eFuse on 5V, no reverse-battery FET'; see review-schematic.json.

## P8 verify waivers (PROVISIONAL, agent-proposed 2026-10-01; full list in reports/verify-waivers.json)
- U1 thermal (check_thermal, 1.1 W -> ~81 C model rise vs 40 C declared): a 2-layer board's model floor is ~55 C/W, GND copper already saturates the model. Acceptable because the BQ24074 folds back charge current at 125 C junction and typical dissipation is below the 1.1 W worst case. Risk: slower charging when hot at 5 V in with a deeply discharged cell.
- U1 GND vias 4, wanted 5 (check_current transition at the U1 pad): the exposed pad fits only 4 vias. Acceptable: 4 vias at 0.5 A each cover the charger return; risk: slightly higher pad-to-plane thermal and via resistance.
- +SYS pour neck and 2-via transition at R6 (check_current, 2.2 A net budget): this is the DONE-LED branch, a few mA. Risk: none for the rail; checker budget is net-wide.
- GND F.Cu sliver neck near J4 (63.5, 51.3): J4 return runs through its THT pads into the B.Cu GND plane, which is the parallel path. Risk: if the owner wants F.Cu return continuity at 1 A, add stitching vias there.
- Advisory warnings left (not waived in the gate, they do not fail it): C11/C12/C13 ground pads 7-8 mm from a GND via and C13 loop ~11.4 nH (5V output caps, plane is solid so low risk); U2/R10 refdes silk ambiguity; 16 two-terminal parts and J3/J4/Q1 have no datasheet extraction for the pin-ratings check.
