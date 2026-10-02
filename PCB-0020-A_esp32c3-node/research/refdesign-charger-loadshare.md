# refdesign - MCP73831 charger + load-sharing power path (reference design, P1)

Decisions (sources in the .json):
1. RPROG 5.1 k -> ~196 mA charge (IREG = 1000 V/RPROG), 4.20 V -2 option.
2. 4.7 uF in and out of the charger (datasheet typical application).
3. Load sharing: B5819W VBUS->VSYS, AO3401A drain=VBAT, source=VSYS, gate=VBUS,
   100 k gate pull-down. The AN1149 citation is an OPINION until verified (not fetched).
4. STAT -> red charge LED anode at VBUS: lights while charging only.
5. No NTC - the IC has no TS input; the P0 provisional decision covers it.
Footgun: no-battery VBAT reads ~4.2 V; firmware note for the bring-up doc.
