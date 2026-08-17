# T‑1 ENZO v1 – Full Build Guide

INTRO:
T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.

## How to use this guide
This file is an **overall project reference**.

For the clearest public V1 build path, use the staged order below:
1. [Software Setup](SOFTWARE_SETUP_T1_ENZO_v1_USER.md)
2. [Module Group A — ESP Core Stack](ESP_BUILD_GUIDE_MODULE_GROUP_A.md)
3. [Module Group B — Power System](MODULE_GROUP_B_POWER_SYSTEM_FINAL_v2.md)
4. [Wiring Reference](WIRING_REFERENCES_T1_ENZO_v1_COMBINED.md)

Module A is built and tested first on USB bench power. Module B is then built and verified with the ESP disconnected before the two are integrated.

Do **not** solder, move wires, or change connections while the system is powered.
Disconnect battery / external power before making physical wiring changes.

---

## 1. Bill of Materials (Exact)

### Core Electronics
- ESP32‑S3 development board (core controller)
- PIR motion sensor (5V)
- LDR + resistor (3.3V divider)
- 8-pixel WS2812 / NeoPixel eyes module
- Heartbeat LED (single)
- Wi‑Fi status LED (single)
- Push buttons:
  - Mode / eyes button (GPIO4)
  - Wi‑Fi button (GPIO5)

### Power
- 2-cell LiPo 7.4V battery
- Deans connector male with 2 inch wire
- double-connecting block
- inline fuse holder + fuse
- **3× Schottky diodes** for the verified V1 protection/isolation arrangement
- UBEC / buck converter (input/source rail → 5V, 3A minimum recommended)
- input/source rail
- latching switch with LED
- 5V distribution rail
- ground bus bar

### Chassis & Mechanical
- **Black Gladiator tracked robot chassis (Pi Hut)**
- DC motors (12V, ~300 RPM)
- M3 risers (20–30mm)
- M3 bolts, nuts, nylocs
- 0.5mm steel or aluminium sheet (platforms)
- standoffs
- heat-shrink
- cable ties

### Wiring
- 14 AWG (battery / rails)
- 18–20 AWG (motors)
- 22 AWG (logic, sensors)
- Dupont leads (temporary only)

---

## 2. Mechanical Assembly

### Step 1: Chassis
- Assemble the black Gladiator tracked chassis and motors
- Ensure smooth movement
- Do **NOT** wire motors yet

### Step 2: Level System
- Level 0: Chassis base
- Level 1: ESP
- Level 2: Power rails
- Level 3: Battery platform

Use risers to create clear vertical separation.
Nothing should touch the chassis metal directly.

---

## 3. Power System (CRITICAL)

### Canonical V1 Power Flow
```text
2S 7.4V LiPo (Battery)
 ↓
Double-connecting block / input connection
 ↓
Fuse (~5A)
 ↓
Main Schottky diode
 ↓
Source / input bus bar
 ↓
UBEC / buck converter
 ↓
Latching switch
 ↓
5V Rail
```

Main-path Schottky orientation:
- **band faces the source/input rail / downstream side**

V1 also uses two additional Schottky isolation channels around the ESP 5V connection:

```text
USB / ESP 5V pin → Schottky → 5V Rail
5V Rail → Schottky → ESP 5V pin
```

Use the dedicated [V1 Schottky OR-ing reference](V1%20schottky%20OR-ing%20method.txt) for exact diode direction. The V1 arrangement uses **three Schottky diodes total**.

### Grounding Rule
- ONE heavy ground from ESP → ground rail
- All sensor grounds stay on ESP pins
- All rails share common ground via bus bar
- Chassis is NOT ground

---

## 4. Wiring – ESP32 Core

### Power
- 5V rail / USB isolation is connected to the ESP through the documented two-Schottky V1 arrangement
- GND → ESP GND pin (single heavy wire to rail)

### Sensors
- PIR → GPIO14 (5V + GND)
- LDR → GPIO7 (3.3V divider)
- Mode / eyes button → GPIO4
- Wi‑Fi button → GPIO5
- Heartbeat LED → GPIO2
- Wi‑Fi LED → GPIO12 (active HIGH)
- RGB / Eyes → GPIO16

---

## 5. Firmware

1. Flash the provided firmware files
2. Verify serial output
3. Test modes:
   - Idle
   - Blink
   - Solid
   - Angry
   - Happy
4. Test PIR motion reaction
5. Test Wi‑Fi button / LED behaviour

---

## 6. Final Checks
- No loose wires
- Fuse installed
- Main Schottky installed with correct polarity
- ESP/5V isolation Schottkys installed with correct polarity
- Tracks free-moving
- ESP secure

---

## 7. When v1 Is Finished
STOP.
Do not add features.
Document.
Photograph.
Tag firmware.

## Next Step

For the practical public V1 path, follow the staged documents in this order:
1. [Software Setup](SOFTWARE_SETUP_T1_ENZO_v1_USER.md)
2. [Module Group A — ESP Core Stack](ESP_BUILD_GUIDE_MODULE_GROUP_A.md)
3. [Module Group B — Power System](MODULE_GROUP_B_POWER_SYSTEM_FINAL_v2.md)
4. [Wiring Reference](WIRING_REFERENCES_T1_ENZO_v1_COMBINED.md)

Do not skip ahead or mix stages out of order.
