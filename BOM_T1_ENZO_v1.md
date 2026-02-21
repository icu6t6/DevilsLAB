# T1 ENZO v1 – Bill of Materials (BOM)

## T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.

This document lists all components required to build **T1 ENZO v1**, including brand, purpose, and source.
Where exact model numbers were not written explicitly, they are noted and can be confirmed or swapped with equivalents.

---

## Core Electronics

### ESP32 Controller
- **Item:** ESP32-S3 Dev Board
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

### 2-cell Battey 7.4V LiPo
- **Item:** 2s1p 29.6Wh Gens ace
- **Notes:** Main power source
- **Source:** Amazon
- **Qty:** 1

### Double block connecter
- **Item:** inline connection block (+-=IN, +-=OUT
- **Notes:** links Deans-IN from Battery
- **Source:** Amazon
- **Qty:** 1

### Power in → Deans "male"
- **Item:** Male Deans Connector
- **Notes:** Dean male with 2 inch wire ish
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
- **Item:** Common Ground Bus / Terminal Block
- **Notes:** Single ground reference (“ground motorway”)
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
- **Item:** Latching Button
- **Notes:** Latching power switch; LED powered from 5v; interrupts main 5v rail
_ **Source: PiHut
_ **Qty:** 1
 
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
- **Item:** DFR “Radiator-style” Chassis
- **Notes:** Custom / repurposed metal chassis
- **Source:** Existing / custom
- **Qty:** 1

### Battery Tray
- **Item:** Custom / Temporary Tray
- **Notes:** May be redesigned depending on battery
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
