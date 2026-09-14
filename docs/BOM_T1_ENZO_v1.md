## T1 ENZO v1 – Bill of Materials (BOM)

T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.

This document separates the documented V1 reference parts from functional replacement requirements. Historical V1 used a fixed-output RC-style 5V / 3A UBEC; later ENZO replacement bucks are different hardware and are not backdated into this BOM.

**Power selection rule:** all three external V1 diodes are SR560. Historical V1 used a fixed 5V / 3A RC-style UBEC and a 5A automotive blade fuse. Where the original switch or terminal SKU is unavailable, use the functional electrical ratings stated below rather than guessing an exact historical part.

---

## Core Electronics

### ESP32 Controller
- **Item:** Waveshare ESP32-S3-DEV-KIT-N8R8 development board
- **Reference:** [manufacturer documentation](https://docs.waveshare.com/ESP32-S3-DEV-KIT-N8R8)
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
  - 1× ESP/USB → 5V rail supply channel
  - 1× 5V rail → ESP supply channel
- **Part and ratings:** SR560 on all three external paths; 5A average forward current, 60V repetitive peak reverse voltage, 150A non-repetitive forward surge rating. The onboard USB diode is additional and is not one of these three external parts.
- **Orientation:** follow the dedicated V1 Schottky wiring reference exactly
- **Notes:** These three diodes are part of the verified V1 power architecture and must not be omitted from a faithful ENZO V1 build

### Buck Converter
- **Item:** Fixed-output RC-style UBEC / buck converter, source-rail input to nominal 5V output
- **Original specification:** 5V / 3A fixed-output RC-style UBEC; the historical V1 rail was observed at about 5.28–5.30V and the unit had no adjustment
- **Notes:** Powers the 5V logic rail. Exact historical brand/SKU is unavailable and is not required. For a replacement, use a regulated nominal-5V unit rated for at least 3A continuous, verify its input range suits the 2S source, and measure its output before connecting the ESP. Historical V1 was observed at about 5.28–5.30V on the rail; that is evidence for the original fixed UBEC, not a replacement set-point.
- **Source:** Amazon
- **Qty:** 1

---

## Distribution & Wiring

### Power Distribution PCB
- **Item:** 2-way Power Distribution Board / Bus
- **Notes:** Used as input/source rail
- **Source:** Amazon
- **Qty:** 1

### 5V Distribution Rail
- **Item:** A separate 5V distribution bus, fed through the latching switch
- **Notes:** Electrically separate from the source rail and GND; allow terminals for the RGB, PIR, button LED and two ESP diode channels. Verify terminal grouping before wiring.
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
- **Notes:** Freenove-supplied HC-SR501 PIR. OUT → GPIO14; 5V supply and common GND. Freenove documents a 5–20V DC supply range and a 3.3V HIGH output, so the signal is suitable for the ESP32-S3 GPIO input.
- **Source:** Amazon
- **Qty:** 1

### LDR (Light Sensor)
- **Item:** LDR + 10 kΩ fixed resistor
- **Notes:** 3.3V → 10 kΩ resistor → GPIO7 junction → LDR → GND
- **Source:** Amazon
- **Qty:** 1

### Push Button Latching Switch with LED
- **Item:** Latching button
- **Notes:** Latching contacts C1/NO1/NC1 with separate LED terminals. Buck OUT+ → C1; NO1 → 5V rail; NC1 unused. LED+ → 5V rail, LED− → GND. Use contacts rated for at least 5A DC at 5V or higher for margin on the 3A rail, and a 5V-rated LED if illumination is connected. The button interrupts the buck feed; integrated USB can keep the 5V rail powered while the button is OFF.
- **Source:** Pi Hut
- **Qty:** 1
 
### NeoPixel Eyes
- **Item:** Freenove 8-pixel RGB module (photographed reference); V1 uses the WS2812 / NeoPixel protocol
- **Notes:** GPIO16; V1 firmware drives an 8-pixel device and uses two pixels as the visible eyes
- **Source:** Amazon
- **Qty:** 1

### Status LEDs
- **Heartbeat LED:** GPIO2
- **WiFi LED:** GPIO12
- **Notes:** Each LED needs its own 220–330 Ω series resistor, as specified in Module A
- **Source:** Amazon
- **Qty:** 2

### Buttons
- **Mode / Eyes button:** GPIO4
- **Wi-Fi button:** GPIO5
- **Notes:** Momentary push buttons
- **Source:** Amazon
- **Qty:** 2

---

## Bench Assembly and Tools

- USB data cable matching the ESP board and a computer running Thonny
- Perfboard / protoboard and insulated mounting standoffs for the ESP assembly
- Multimeter, soldering tools, insulation / heat-shrink and suitable terminals; source-side terminals must be rated for the 5A fused path and 5V-rail terminals for at least the 3A converter output
- Historical main battery/source wiring was about 14 AWG, with smaller downstream power wiring (typically 16–18 AWG) and smaller logic/signal wiring where appropriate. Use proper stranded hookup/power wire and suitable crimp/screw terminations; do not use cheap Dupont jumper-wire conductor as permanent power/interconnect wiring. Module A’s 330–470 Ω RGB data resistor and ≥470 µF supply capacitor remain recommended as documented there.
- A charger suitable for the chosen 2S LiPo battery; the ENZO power path is not a battery charger

## Mechanical / Structure — Optional Reference Installation

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
- All power wiring is done **with battery, USB and any external power disconnected**
- Substitute only where the electrical specifications and operating limits above are met; verify the actual part before power-up rather than relying on a visual match
- For diode orientation and USB/battery isolation, use [V1 schottky OR-ing method.txt](V1%20schottky%20OR-ing%20method.txt)

---

## Next Step

Once you have gathered the required parts, continue to [Software Setup](SOFTWARE_SETUP_T1_ENZO_v1_USER.md), then follow the staged public V1 path through Module A, Module B and final wiring integration.

The [Full Build Guide](BUILD_GUIDE_T1_ENZO_v1-2.md) remains available as an overall reference.

Gather first. Build second. Do not skip ahead.

*This BOM reflects the current T1 ENZO v1 build and may be updated in future revisions.*
