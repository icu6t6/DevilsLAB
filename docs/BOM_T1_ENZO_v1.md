## T1 ENZO v1 – Bill of Materials (BOM)

T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.

This document lists all components required to build **T1-ENZO v1**, including brand, purpose, and source.
Where exact model numbers were not written explicitly, they are noted and can be confirmed or replaced with suitable equivalents.

---

## Core Electronics

### ESP32 Controller
- **Item:** Waveshare ESP32-S3 N8R8 development board
- **Notes:** Main controller (WiFi + BLE)
- **Source:** Amazon
- **Qty:** 1

---

## Power System

### 2-cell Battery 7.4V LiPo
- **Item:** 2s1p 29.6Wh Gens Ace
- **Notes:** Main power source
- **Source:** Amazon
- **Qty:** 1

### Double-connecting block
- **Item:** Inline connection block (+/- IN, +/- OUT)
- **Notes:** Connects Deans input from battery
- **Source:** Amazon
- **Qty:** 1

### Power input → Deans male
- **Item:** Male Deans connector
- **Notes:** Deans male connector with short wire lead
- **Source:** Amazon
- **Qty:** 1

### Inline Fuse + Holder
- **Item:** Automotive Blade Fuse Holder + Fuse
- **Rating:** ~5A (recommended)
- **Notes:** Inline on the source/input rail positive line only
- **Source:** Amazon
- **Qty:** 1

### Schottky Diodes
- **Item:** Schottky power diodes suitable for the V1 current path
- **Qty:** 3
- **Purpose:**
  - 1× main-path reverse-protection diode after the fuse and before the source/input rail
  - 1× ESP/USB → 5V rail isolation channel
  - 1× 5V rail → ESP isolation channel
- **Orientation:** follow the dedicated V1 Schottky wiring reference exactly
- **Notes:** These three diodes are part of the verified V1 power architecture and must not be omitted from a faithful ENZO V1 build

### Buck Converter
- **Item:** DC-DC Buck Converter (input/source-rail → 5V)
- **Notes:** Powers the 5V logic rail
- **Source:** Amazon
- **Qty:** 1

---

## Distribution & Wiring

### Power Distribution PCB
- **Item:** 2-way Power Distribution Board / Bus
- **Notes:** Used as input/source rail
- **Source:** Amazon
- **Qty:** 1

### Ground Rail
- **Item:** Common ground bus / terminal block
- **Notes:** Single ground reference for the system
- **Source:** Amazon
- **Qty:** 1

### Wires
- **Item:** Silicone Wire
- **Specs:** 
  - 14 AWG (main power)
  - 16 AWG (power distribution)
  - Dupont jumper wires (signals)
- **Source:** Amazon
- **Qty:** As required

---

## Sensors & UI

### PIR Motion Sensor
- **Item:** PIR Sensor Module
- **Notes:** GPIO14
- **Source:** Amazon
- **Qty:** 1

### LDR (Light Sensor)
- **Item:** LDR + Resistor
- **Notes:** GPIO7
- **Source:** Amazon
- **Qty:** 1

### Push Button Latching Switch with LED
- **Item:** Latching button
- **Notes:** Latching power switch; LED powered from 5V; interrupts main 5V rail
- **Source:** Pi Hut
- **Qty:** 1
 
### NeoPixel Eyes
- **Item:** 8-pixel WS2812 / NeoPixel module
- **Notes:** GPIO16; V1 firmware drives an 8-pixel device and uses two pixels as the visible eyes
- **Source:** Amazon
- **Qty:** 1

### Status LEDs
- **Heartbeat LED:** GPIO2
- **WiFi LED:** GPIO12
- **Notes:** With appropriate resistors
- **Source:** Amazon
- **Qty:** 2

### Buttons
- **Mode / Eyes button:** GPIO4
- **Wi-Fi button:** GPIO5
- **Notes:** Momentary push buttons
- **Source:** Amazon
- **Qty:** 2

---

## Mechanical / Structure

### Chassis
- **Item:** Black Gladiator tracked robot chassis
- **Source:** Pi Hut
- **Qty:** 1

### Battery Tray
- **Item:** Custom battery tray
- **Notes:** May be redesigned depending on battery choice
- **Qty:** 1
---

## Notes & Assumptions

- Canonical battery-positive path is **Battery → Fuse → Main Schottky → Source/Input Rail**
- All grounds ultimately tie back to the **Ground Rail**
- ESP32 ground is connected to ground rail via a single heavy reference wire
- Sensors may ground locally at ESP, but share common ground via rail
- All power wiring is done **with battery disconnected**
- Parts listed can be substituted with equivalents if specs are matched
- For diode orientation and USB/battery isolation, use [V1 schottky OR-ing method.txt](V1%20schottky%20OR-ing%20method.txt)

---

## Next Step

Once you have gathered the required parts, continue to [Software Setup](SOFTWARE_SETUP_T1_ENZO_v1_USER.md), then follow the staged public V1 path through Module A, Module B and final wiring integration.

The [Full Build Guide](BUILD_GUIDE_T1_ENZO_v1-2.md) remains available as an overall reference.

Gather first. Build second. Do not skip ahead.

*This BOM reflects the current T1 ENZO v1 build and may be updated in future revisions.*
