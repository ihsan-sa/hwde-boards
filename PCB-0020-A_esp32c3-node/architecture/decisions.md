# decisions - esp32c3-node (P2)

- 2 layers, JLC2313_1.6: no impedance control needed (USB-FS, short run); density, not layers, binds.
- Module ESP32-C3-MINI-1-N4 (PCB antenna, pre-certified) over the bare C3 chip: RF path untouched,
  no crystal/matching on a 2L board. -H4X is the pin-compatible alternate.
- Charger MCP73831-2 + AO3401A/B5819W load sharing (AN1149) over a dedicated power-path IC
  (BQ24074 class): stocked, cheap, Basic MOSFET/Schottky; the cost is a Schottky drop on USB.
  TP4054 is the pin-compatible fallback.
- RT9080-33 over AP2112K/ME6211: 600 mA headroom for TX peaks + Qwiic, 2 uA Iq.
- BME280 kept despite 7 USD (brief asks BME280-class); SHT40 is the stock fallback.
- No USB series resistors, no 90 ohm impedance target (interface-usb-fs research).
- No NTC, no reverse-battery FET (provisional Q1d/Q1e, silk polarity), protected cell required.
- No mounting holes; edge pads are plated through-holes, not castellations.
- Accepted deviation: VBUS attach charge ~65 uC > 50 uC guideline.
- Outline is an output; XIAO 21 x 17.8 mm is soft and is not expected to hold (stackup.md).
