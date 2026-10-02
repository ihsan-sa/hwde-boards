# lipo-boost brief (PCB-0021-A)

I want a little board that runs a 5 V USB gadget off a single-cell LiPo and charges the cell from USB.

- USB in (micro-B or C) charges a 1S LiPo on a JST-PH 2-pin connector, about 1 A max.
- Load sharing: when USB is plugged in, the 5 V output keeps running while the cell charges.
- 5 V / 1 A out on a USB-A socket, from a synchronous boost.
- An enable pin to turn the output off, plus a low-battery LED and charge / done LEDs.
- Small, cheap, JLCPCB-assembled, 2 layers is fine.

Reference: this is a from-scratch recreation of Adafruit's PowerBoost 1000C (open hardware,
CC BY-SA). Design it from this brief, then compare the result with Adafruit's published design.
