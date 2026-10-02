# Brief: esp32c3-node (unattended track run, 2026-10-01)

A tiny WiFi + Bluetooth LE sensor node, in the spirit of the Seeed XIAO ESP32-C3. Product
scope (no mode token), 2 layers, meant to go to JLCPCB as-is with economy PCBA.

- ESP32-C3-MINI-1 module; keep its antenna keep-out clear of copper and parts, antenna at a board edge.
- USB-C for power and flashing over the C3's native USB (no USB-UART bridge); BOOT and RESET buttons.
- Runs from a single-cell LiPo (JST-PH 2-pin) with a charger that has power path, so it runs
  from USB with or without a battery. 3.3 V LDO for everything. Battery voltage sense into an ADC pin.
- A BME280-class temperature/humidity/pressure sensor on I2C, plus a Qwiic/STEMMA QT connector on the same bus.
- One status LED on a GPIO.
- Keep it small, roughly XIAO-sized if an honest layout allows; spare GPIOs on castellated or 0.1 in edge pads.
