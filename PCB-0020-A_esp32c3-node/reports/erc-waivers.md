# P4 schematic waivers - PCB-0020-A esp32c3-node (2026-10-01)

ERC: 0 errors, 0 warnings (all 3 sheets). netlist_audit: pass, 182/182 expected pins.
schematic-reviewer (fresh context, sonnet): 0 errors, 6 warnings. Dispositions:

1. VBUS budget ~650 mA transient vs 500 mA default USB (charger 196 mA + TX peak).
   Accepted: the same deviation was recorded at P2 (power_tree.md); average load ~0.1 A,
   and the MCP73831 backs off as VBUS sags. Owner sees it at H2.
2. D1 SMF5.0A clamps up to 9.2 V at full pulse current; U2 VDD abs max 7.0 V.
   Accepted for a USB-powered hobby node: the clamp sits at ~6.4 V for the small
   hot-plug transients a USB port produces. A lower-clamp TVS is a candidate revision B item.
3. J2 LiPo has no reverse-polarity protection. Accepted at P2 (no reverse-battery FET);
   P6 must put a "+" silk mark at J2 pin 1 and the guide must state the pack polarity.
4. U3 Tj ~114 C worst case. Carried to P6/P7 as a layout duty: GND pour + >= 2 vias
   (constraints.json thermal entry).
5. Strap pins IO2/IO8 are on the J4 edge pads. Accepted: the 10k pull-ups hold them high,
   J4 is DNP, and the guide will say not to load them low at reset.
6. TS-1187A pin pairing (1+2, 3+4). Verified on PCB-0015 for the same pulled symbol against
   the XKB drawing (that board's main_sheet.py notes); no change.
Also noted: parts/ PDFs J2_SM04B... and J3_S2B-PH... carry swapped refdes prefixes from P3 naming;
the netlist and parts.json are right.
