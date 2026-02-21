# T‑1 ENZO v1 – Full Build Guide

INTRO:
T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.

## 1. Bill of Materials (Exact)

### Core Electronics
- ESP32‑S3 development board (core controller)
- ESP32‑S3 with LCD (optional, not required for v1)
- TB6612FNG motor driver (Grove I2C version)
- PIR motion sensor (5V)
- LDR + resistor (3.3V divider)
- RGB LED module or individual LEDs
- Heartbeat LED (single)
- Wi‑Fi status LED (single)
- Push buttons:
  - Mode button
  - Power / function buttons

### Power
- 2-cell LiPo 7.4V battery
- Deans connector male with 2 inch wire
ATTENTION TO POLARITY MATCH
- Double-connecting block (-) to GND bar, (+) to one end of fuse 
_ Fuse (+) → input rail (+)
- UBEC / buck converter (input/source-rail → 5V, "3A minimum buck")
- Inline fuse holder + fuse
- input rail 
- Latching switch w/LED
- 5V distribution rail
- Ground bus bar

### Chassis & Mechanical
- Gladiator tracked robot chassis
- DC motors (12V, ~300 RPM)
- M3 risers (20–30mm)
- M3 bolts, nuts, nylocs
- 0.5mm steel or aluminium sheet (platforms)
- Standoffs
- Heat‑shrink
- Cable ties

### Wiring
- 14 AWG (battery / rails)
- 18–20 AWG (motors)
- 22 AWG (logic, sensors)
- Dupont leads (temporary only)

---

## 2. Mechanical Assembly

### Step 1: Chassis
- Assemble tracks and motors
- Ensure smooth movement
- Do NOT wire motors yet

### Step 2: Level System
- Level 0: Chassis base
- Level 1: ESP + motor driver
- Level 2: Power rails
- Level 3: Battery platform

Use risers to create clear vertical separation.
Nothing should touch the chassis metal directly.

---

## 3. Power System (CRITICAL)

### Power Flow
```
2S 7.4V LiPo (Battery)
 ↓
Double-connecting block
 ↓
Fuse (5A)
 ↓
source/intput Bus Bar
 ├── Motor Driver (VM)
 └── UBEC (source-rail → 5V)
        ↓
      5V Rail
        ↓
      ESP32 + Sensors
```

### Grounding Rule
- ONE heavy ground from ESP → ground rail
- All sensor grounds stay on ESP pins
- All rails share common ground via bus bar
- Chassis is NOT ground

---

## 4. Wiring – Motor Driver (TB6612FNG)

### Power
- VM → input rail
- VCC → 5V rail
- GND → ground rail

### Control (ESP GPIO example)
- AIN1 → GPIO X
- AIN2 → GPIO Y
- BIN1 → GPIO Z
- BIN2 → GPIO W
- STBY → GPIO (or tied HIGH)

### Motors
- Motor A → A01 / A02
- Motor B → B01 / B02
(Swap wires to reverse direction)

---

## 5. Wiring – ESP32 Core

### Power
- 5V → ESP 5V pin
- GND → ESP GND pin (single heavy wire to rail)

### Sensors
- PIR → GPIO14 (5V + GND)
- LDR → GPIO7 (3.3V divider)
- Buttons → GPIO4 / GPIO5
- Heartbeat LED → GPIO2
- Wi‑Fi LED → GPIO12 (active HIGH)
- RGB / Eyes → GPIO16

---

## 6. Firmware

1. Flash provided firmware files
2. Verify serial output
3. Test modes:
   - Idle
   - Blink
   - Solid
   - Angry
   - Happy
4. Test motion reaction
5. Test Wi‑Fi LED toggle

---

## 7. Final Checks
- No loose wires
- No exposed 12V
- Fuse installed
- Tracks free‑moving
- ESP secure

---

## 8. When v1 Is Finished
STOP.
Do not add features.
Document.
Photograph.
Tag firmware.

Then — and only then — begin v2.
