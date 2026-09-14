# ENZO V1 Wiring Reference

Use this with the [BOM](BOM_T1_ENZO_v1.md), [Module A](ESP_BUILD_GUIDE_MODULE_GROUP_A.md) and [Module B](MODULE_GROUP_B_POWER_SYSTEM_FINAL_v2.md). It describes the Free V1 electrical baseline; chassis mounting is optional and locomotion belongs to V2.

Retained physical/as-built reference (for build and mounting context):

![ENZO V1 physical/as-built wiring reference](updated_v1_wiring_diagram_ELF.png)

Supplementary electrical topology reference (for corrected connection, polarity and label truth): [WIRING_T1_ENZO_V1.svg](WIRING_T1_ENZO_V1.svg)

## Connections that must agree

| Function | Connection |
|---|---|
| Protected positive input | Battery + → 5A automotive blade fuse → SR560 main Schottky → source/input rail; diode band toward source rail |
| Regulated battery feed | Source rail → buck IN+; buck OUT+ → switch C1; switch NO1 → 5V rail; NC1 unused |
| External Channel A | ESP 5V header → SR560 → 5V rail; band toward rail |
| External Channel B | 5V rail → SR560 → ESP 5V header; band toward ESP |
| Common ground | Battery −, buck IN−/OUT−, ESP GND and load returns share GND; chassis is not the return |
| RGB | GPIO16 → DIN / DATA; RGB supply → 5V; RGB GND → GND |
| LDR | 3.3V → 10 kΩ resistor → GPIO7 junction → LDR → GND |
| PIR | Freenove HC-SR501: OUT → GPIO14; supply → 5V; GND → GND; output HIGH is 3.3V |
| LEDs | GPIO2 heartbeat and GPIO12 Wi-Fi, each through its own 220–330 Ω series resistor and LED to GND |
| Buttons | GPIO4 Mode and GPIO5 Wi-Fi; each momentary contact to GND |
| Switch LED | LED+ → 5V rail; LED− → GND |

Module A’s recommended RGB data resistor and supply capacitor remain as documented there. Board-specific USB isolation and the original three-diode operating record are explained in the [Schottky reference](V1%20schottky%20OR-ing%20method.txt).

The prior combined drawings mislabelled the RGB data terminal, labelled the LDR resistor as 10uF or 220K, and omitted the main Schottky from the positive path. This reference supersedes those labels. The 4-way distribution fuse block shown in earlier as-built pictures is not required Free V1 hardware.

## Integration and V1 completion

Complete Module A on USB first and Module B with the ESP disconnected. Use the BOM’s SR560, fuse, switch/terminal and voltage requirements before power integration.

1. Disconnect battery, USB and any external supply. Verify all connections against the table, diode bands, LED polarity, insulated mounting and strain relief.
2. Connect ESP GND to common GND and install both external ESP/rail diode channels with their stated orientations. Never wire GPIO7 or GPIO16 to the 5V supply.
3. For the battery-only integration check, leave USB disconnected, turn the latching switch OFF, then connect the battery. Confirm the switch removes the buck feed from the rail. Turn it ON; measure UBEC output, 5V rail and ESP 5V header relative to common GND and record them. Historical V1 showed about 5.28–5.30V on the rail; do not treat that historical reading as a replacement set-point.
4. Confirm the Module A behaviours still work on battery power. A USB serial connection would change this into a combined-source state; label it accordingly if used after that state has been validated.
5. Record which power states were actually checked. Integrated USB can keep the rail powered with the switch OFF. Historical V1 passed battery-only, USB-only and combined operation; for a substitute UBEC, do not use switch-ON combined-source operation unless the converter is specified to tolerate an externally driven output.
6. Pass the Module A and Module B checklists and record integration results. Record untested required functions and unresolved faults as incomplete; a partial build is welcome but is not full V1 completion.

V1 Free completion means a working ESP32-S3 sensor/UI assembly, completed Module A, a verified protected battery/5V Module B system, completed integration and passed documented checks. Tracked mounting is optional. Locomotion is V2.

[Building ENZO / show your build](https://github.com/icu6t6/DevilsLAB/issues/new?template=build-report.yml). Include your build stage and any substituted parts; photos are optional.
