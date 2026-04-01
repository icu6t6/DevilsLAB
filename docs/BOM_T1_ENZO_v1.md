## T1 ENZO v1 – Bill of Materials (BOM)

T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.

This document lists all components required to build **T1-ENZO v1**, including brand, purpose, and source.
Where exact model numbers were not written explicitly, they are noted and can be confirmed or replaced with suitable equivalents.

---

## Core Electronics

### ESP32 Controller
- **Item:** ESP32-S3 Dev_Kit_NXR8
- **Notes:** Main controller (WiFi + BLE)
- **Source:** Amazon
- **Qty:** 1

### Motor Driver
- **Item:** TB6612FNG Dual Motor Driver (I2C / Grove variant supported)
- **Notes:** Drives motors, logic-level controlled
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
- **Notes:** Inline on source-rail "positive only"
- **Source:** Amazon
- **Qty:** 1

### Buck Converter
- **Item:** DC-DC Buck Converter (input/source-rail → 5V)
- **Notes:** Powers 5V rail / logic
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
 
### RGB LED
- **Item:** Addressable RGB LED
- **Notes:** GPIO16
- **Source:** Amazon
- **Qty:** 1

### Status LEDs
- **Heartbeat LED:** GPIO2
- **WiFi LED:** GPIO12
- **Notes:** With appropriate resistors
- **Source:** Amazon
- **Qty:** 2

### Buttons
- **Button 1:** GPIO4
- **Button 2:** GPIO5
- **Notes:** Momentary push buttons
- **Source:** Amazon
- **Qty:** 2

---

## Mechanical / Structure

### Chassis
- **Item:** DFR “radiator-style” chassis
- **Notes:** Custom or repurposed metal chassis
- **Source:** Existing or custom
- **Qty:** 1

### Battery Tray
- **Item:** Custom battery tray
- **Notes:** May be redesigned depending on battery choice
- **Qty:** 1
---

## Notes & Assumptions
- All grounds ultimately tie back to the **Ground Rail**
- ESP32 ground is connected to ground rail via a single heavy reference wire
- Sensors may ground locally at ESP, but share common ground via rail
- All power wiring is done **with battery disconnected**
- Parts listed can be substituted with equivalents if specs are matched

---

*This BOM reflects the current T1 ENZO v1 build and may be updated in future revisions.*
