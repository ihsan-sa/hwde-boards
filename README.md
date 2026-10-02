# hwde-boards

KiCad board designs made with [hwde](https://github.com/ihsan-sa/hwde), an AI PCB design skill for
Claude Code that takes a board from a written brief to a JLCPCB order. Each folder is one board's
whole workspace: the brief, research notes, architecture, parts choices, the KiCad project,
routing work, review reports, logs, and the fab package.

Every board has a part number of the form **PCB-NNNN-R**: four digits for the product, then a
revision letter. `register.yaml` lists them.

## The boards

Layers and size come from each board's KiCad file. Stage is the hwde phase recorded in the board's
`state.json`: P3 parts, P4 schematic, P7 routing, P8 verification, P9 DFM and fab outputs, P10 ordering.

| Number | What it is | Layers | Size (mm) | Stage |
|---|---|---|---|---|
| [PCB-0001-A](PCB-0001-A_stm32-blinky) | STM32F103 2-layer blinky dev board | 2 | 50 x 40 | P10 |
| [PCB-0002-A](PCB-0002-A_usb-buck) | STM32F103 4-layer USB device board with 3.3 V buck | 4 | 50 x 40 | P10 |
| [PCB-0003-A](PCB-0003-A_pd-trigger) | USB-C PD trigger, 5 A / 100 W bench board | 2 | 48 x 30 | P10 |
| [PCB-0004-A](PCB-0004-A_lumina-carrier) | LUMINA PoE ESP32 carrier | 4 | 100 x 80 | P10 |
| [PCB-0005-A](PCB-0005-A_lumina-par) | LUMINA RGB+W par light daughter board | 4 | 100 x 80 | P8, no fab package |
| [PCB-0006-A](PCB-0006-A_lumina-strobe) | LUMINA strobe daughter board | - | - | P4, no board yet |
| [PCB-0007-A](PCB-0007-A_rf-de-20m) | 20 MHz Class E GaN RF power stage, 200 W | 4 | 120 x 80 | P9, see its `fab/README.md` |
| [PCB-0008-A](PCB-0008-A_buck-5v3a) | 12 V to 5 V / 3 A synchronous buck, first attempt | - | - | closed at P3, never built |
| [PCB-0008-B](PCB-0008-B_sbuck-5v3a) | 12 V to 5 V / 3 A synchronous buck | 4 | 50 x 40 | P10 |
| [PCB-0009-A](PCB-0009-A_rf-term-150w) | 50 ohm / 150 W RF termination | 2 | 26 x 20 | P9 |
| [PCB-0010-A](PCB-0010-A_bb-buck) | Bare-bones 24 V to 5 V / 2 A buck | 2 | 35 x 25 | P9 |
| [PCB-0011-A](PCB-0011-A_bb-mcu) | Block-basics microcontroller board | 2 | 34.8 x 22.3 | P9 |
| [PCB-0012-A](PCB-0012-A_bb-ldo) | Block-basics 5 V to 3.3 V / 500 mA LDO | 2 | 34.7 x 34.7 | P9 |
| [PCB-0013-A](PCB-0013-A_bb-amp) | Block-basics bridge-sensor amplifier | 2 | 48.0 x 28.3 | P9 |
| [PCB-0014-A](PCB-0014-A_bb-adc) | Block-basics 12-bit single-channel ADC | 2 | 54.8 x 34.9 | P9 |
| [PCB-0015-A](PCB-0015-A_g0-sense) | USB-C STM32G0 temperature/humidity sensor node | 2 | 35.8 x 28.3 | P10 |
| [PCB-0016-A](PCB-0016-A_pd-trigger-lite) | Low-cost USB-C PD trigger (CH224K) | 2 | 25 x 15 | P8 |
| [PCB-0016-B](PCB-0016-B_pd-trigger-lite-dip) | The same, voltage picked with a DIP switch | 2 | 25 x 21 | P9 |
| [PCB-0017-A](PCB-0017-A_stereo-class-d-amp) | TPA3118D2 stereo class-D amplifier, 12 V | 2 | 53.5 x 36.8 | P7 |
| [PCB-0018-A](PCB-0018-A_bldc-motor-driver) | 3-phase BLDC motor driver, 10-28 V, 10 A RMS/phase, STM32G4 FOC | 4 | 78 x 78 | P9 |
| [PCB-0020-A](PCB-0020-A_esp32c3-node) | ESP32-C3 WiFi/BLE sensor node, USB-C, 1S LiPo, BME280 | 2 | 26 x 38 | P8 |
| [PCB-0021-A](PCB-0021-A_lipo-boost) | Single-cell LiPo charger + 5 V / 1 A boost with load sharing | 2 | 53.9 x 38.8 | P9 |

All boards with a fab package are 1.6 mm thick.

## Where things are in a board folder

- `kicad/` the KiCad project (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`); it was made with KiCad 10, so open it with KiCad 10.
- `fab/` the order package: `<folder>_gerbers.zip`, `BOM.csv` and `CPL.csv` in JLCPCB's format.
- `reports/` review reports, renders, a schematic PDF for every board that has a schematic, and a
  design document PDF for most of them.
- `brief/`, `requirements.md`, `research/`, `architecture/`, `parts/` why the board is the way it is.
- `state.json` the phase, the gates that passed, and every decision hwde recorded.

## Ordering a board from JLCPCB

1. On jlcpcb.com, start a PCB order and upload the board's `fab/<folder>_gerbers.zip`. Set the
   layer count and thickness to match the table above.
2. To have JLCPCB assemble it, turn on PCB Assembly and upload `fab/BOM.csv` as the BOM and
   `fab/CPL.csv` as the pick-and-place file.
3. Check the part matches and the placement preview before you pay. Stock changes, so a part may
   need a substitute from the same footprint.

Read the board's reports first. Unless a board's own documents say it was built and tested, treat
the design as unverified on real hardware.

## What is not included

- **3D models.** Vendor STEP and WRL models are not redistributed, so footprints that pointed at
  them show no 3D body in KiCad's 3D viewer. The copper, silkscreen and fab outputs are unaffected.
- **Datasheets and app notes.** Vendor PDFs and copies of vendor pages are left out. The research
  notes and `parts/` records still cite them by name and part number.
- Order and shipment records, and a few design documents whose text carried private details.
  Their LaTeX sources are still under `reports/`.

Some files keep absolute paths from the machine a board was designed on (for example
`C:/Users/<user>/...`). They are records of a run and are not needed to open the design.

## License

MIT, see [LICENSE](LICENSE).
