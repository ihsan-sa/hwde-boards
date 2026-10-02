# power tree (P2) - reconciled against the final block choices

Lifted from research/power.md; changes: the boost now feeds a DRV8300D GVDD (unchanged in size), the
buck is LM5164 (100 V) instead of an unnamed 60 V part, the RP FET is the stage FET (NTMFS5C628NL, ~2 mOhm)
instead of <=1.5 mOhm, and the CSAs are INA240 (Iq 1.8 mA max each, up from INA181's 0.5 mA).

```
VM pads (10-28 V op, 45 V clamp)
 `- Q101 RP N-FET (LM74500)  -> VM bus: SMCJ28A, 470uF/63V, MLCC
     |- power stage, 3 legs ........................ 12.2 A DC cont, 24.5 A at 20 A pk
     `- U201 LM5164 buck -> +5V ...................... 0.65 A design (1 A part)
          |- sensor connector 5V (PTC 0.2 A) ......... 100 mA
          |- control connector 5V (PTC 0.2 A) ........ 150 mA
          |- U202 TPS61040 boost -> +12V (GVDD) ...... 50 mA out -> ~141 mA in
          `- U203 TLV75733 LDO -> +3V3 ............... 0.1 A design
               |- STM32G431 + VDDA (ferrite) ......... 60 mA
               |- 3x INA240A1 ........................ 5.4 mA
               `- LEDs, pull-ups ..................... ~10 mA
```

| Rail | Source | Design I | Loss | Note |
|---|---|---|---|---|
| VM (bus) | pads via RP FET | 12.2 A cont / 25 A pk | RP FET ~0.4 W cont (2 mOhm x1.4 hot x 12.2^2) | TVS + bulk within 10 mm of pads |
| +5V | LM5164, VM -> 5 V, ~400 kHz | 0.65 A (0.49 A sum x1.3) | ~0.45 W design, ~0.15 W typ | 100 V part, VIN min 6 V |
| +12V | TPS61040 from +5V | 0.05 A | ~0.1 W | 6 gates x 52 nC x 25 kHz = 7.8 mA + Iq + pull-downs |
| +3V3 | TLV75733 from +5V | 0.1 A | 0.17 W | VDDA via ferrite + 1 uF/100 nF |

Gate drive: DRV8300D GVDD = 12 V; LS VGS = 12 V, HS VGS = 12 - 0.8 (int. boot diode) - droop ~= 11 V,
independent of VM. Meets Answers #5 (>= 8 V at VM = 10 V). Bootstrap needs < 100 % duty: SVPWM capped at
~95 %, low sides pulsed to pre-charge before the first HS turn-on. Sequencing: MCU holds all INx low until
+12V is up (driver GVDDUV/BSTUV lockouts back this up); gate pull-downs hold FETs off meanwhile.

VM-rated parts (all >= the 45 V clamp): FETs 60 V, LM5164 100 V, LM74500 65 V, DRV8300 SHx 85 V / BST 105 V,
INA240 CM 80 V (sees only shunt mV), MLCC 50 V, electrolytic 63 V, dividers 150 k 0603 (fine at 45 V).

## Thermal estimate (no heatsink, 25-40 C ambient)

| Item | Loss @10 A RMS/phase, 28 V, 25 kHz |
|---|---|
| 6 stage FETs: conduction 3 x 10^2 x ~3 mOhm hot = 0.9 W; switching ~0.9 W | ~1.8 W |
| 3 shunts (LS half the time): 3 x 100 x 3 mOhm x 0.5 | 0.45 W |
| RP FET | 0.4 W |
| buck + boost + LDO (design) | 0.7 W (0.4 W typ) |
| **board total** | **~3.4 W** |

A 4-layer 2 oz board in still air sheds roughly 10-12 W/m^2K over both faces. At 60 x 60 mm (7200 mm^2 both
faces) that is ~12 C/W, so ~40 C mean rise and a hotter spot at the FETs; TIDA-010251 (same size, 2 oz,
no heatsink, lower-Rds FETs) measured 49 C FET max at 10 A RMS. So the board needs **at least ~60 x 60 mm of
copper as radiator**; smaller costs FET temperature directly. P6/P8 earn the final size and check_thermal
decides whether 10 A RMS holds or is derated (PROVISIONAL spec, must be stated either way).
