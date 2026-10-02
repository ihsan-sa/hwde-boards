# refdesign - ESP32-C3-MINI-1 minimum system (reference design, P1)

Sources: Espressif module datasheet v2.2 (s3, s4, s9, s11) and the ESP32-C3 Hardware
Design Guidelines (PCB layout). Decisions with citations are in the .json; summary:

1. EN = 10 k pull-up + 1 uF RC, RESET button to GND (DS s9).
2. Straps: GPIO9 BOOT button + 10 k pull-up; GPIO8 10 k pull-up; GPIO2 10 k pull-up
   (DS Table 4-1/4-3). LED on GPIO10, VBAT ADC on GPIO3 (ADC1_CH3).
3. 3V3: 10 uF + 0.1 uF at pin 3; supply must deliver 0.5 A (DS 6.2).
4. Antenna at the edge, overhang preferred, no copper below it (guidelines).
5. USB D-/D+ on IO18/IO19, no external pull-up, no crystal needed (module has 40 MHz).

Pin plan proposal (architect reconciles): IO18/IO19 USB; IO9 BOOT; EN RESET;
IO6 SDA, IO7 SCL (ASSUMED free - JTAG only on eFuse); IO3 VBAT_SENSE; IO10 LED;
spare to edge pads: IO0, IO1, IO2 (pulled up), IO4, IO5, IO8 (pulled up), IO20/RX0,
IO21/TX0.
