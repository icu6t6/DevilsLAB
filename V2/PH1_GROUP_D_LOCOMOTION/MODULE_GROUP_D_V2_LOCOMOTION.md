# MODULE GROUP D — V2 LOCOMOTION (INTENTIONAL MOVEMENT)

This document describes the introduction of **intentional locomotion** to ENZO.

This module adds controlled physical movement using a dual motor driver, without altering baseline behaviour, autonomy, or system authority.

Outside of deliberate motor commands, ENZO behaves exactly as before.

---

## Purpose

The purpose of this module is to introduce **deterministic, human-initiated movement**.

By the end of this module:

- ENZO can drive both tracks forward under explicit command
- ENZO can stop both tracks reliably
- Movement is intentional, reversible, and auditable
- No autonomous behaviour is introduced

---

## Scope

This module:

- adds a dual motor driver
- introduces I²C-based motor control
- validates movement using a proof-of-life script

This module does **not**:

- add autonomy
- add wireless control
- add speed curves or PID control
- modify baseline logic or sensor behaviour

Those belong to later work.

---

## Assumptions

This module assumes completion of:

- **Module Group A** — ESP core build
- **Module Group B** — Power system

Specifically:

- A stable 2S (≈7.4 V) motor rail exists
- A stable 5 V logic rail exists
- A single, authoritative ground rail exists
- ESP32 firmware can be uploaded and executed

---

## Hardware Overview

The ENZO V2 locomotion build uses the **Seeed Studio Grove - I2C Motor Driver (TB6612FNG)**.

It is a dual-channel motor driver with an onboard MCU and Grove I²C interface. The factory/default I²C address used by ENZO is:

```text
0x14
```

Key characteristics relevant to ENZO:

- TB6612FNG dual motor driver
- onboard MCU
- two independent DC motor channels
- I²C control interface
- separate logic and motor power domains
- motor supply input labelled **VM**
- channel outputs **A1/A2** and **B1/B2**

Motor driver behaviour is **command-driven**, not GPIO-driven.

---

## Power Integration

Motor driver power is connected as follows:

### Motor Power
- **VM** → 2S rail (≈7.4–7.8 V)
- **GND** → ground rail

### Logic Power
- **VCC** → 3.3V ESP
- **GND** → ground rail

All grounds reference the same physical ground rail.

No additional buck conversion is required for this module.

---

## Control Interface (I²C)

The motor driver is controlled exclusively via I²C.

Connections:

- **SDA** → ESP GPIO 8  
- **SCL** → ESP GPIO 9  

These pins are shared with the OLED in other configurations; for this module, the OLED is disconnected.

The motor driver responds at I²C address:

```text
0x14  (decimal 20)
```

---

## Motor Wiring

Two motors are connected directly to the driver outputs:

- **Motor A** → A1 / A2 terminals  
- **Motor B** → B1 / B2 terminals

Motor polarity determines direction and can be corrected later by swapping A1/A2 or B1/B2 if required.

### CW / CCW direction note

`CW` and `CCW` describe the rotation command sent to the motor driver. They do **not** define a universal vehicle-forward direction.

Whether a given command makes ENZO move forward or reverse depends on the physical build, including:

- motor / gearbox mounting orientation
- motor polarity
- A1/A2 and B1/B2 wiring orientation
- left/right installation in the chassis
- track orientation

The Phase 1 proof script reflects the tested orientation used during that bring-up. On another otherwise-correct build, the opposite rotation command may be the one that produces vehicle-forward motion.

Establish the correct forward/reverse mapping with the tracks lifted, then keep that mapping consistent through the later V2 control phases.

---

## Motor Addressing Model

The motor driver uses indexed channels:

- **Motor ID 0** → Channel A  
- **Motor ID 1** → Channel B

All commands reference motors by these IDs.

This mapping is fixed and must be used consistently in software.

---

## Software Interaction

Motor control is achieved by sending I²C commands to the driver.

No GPIO motor control is used.

### Command Concepts

- Each command targets a motor ID
- Direction and speed are explicit
- Motors do nothing unless commanded

Movement is therefore **intentional by design**.

---

## Validation — Proof of Life

Validation consists of a single, deterministic script.

The script:

1. Commands both motors to run in the tested forward direction for this build
2. Holds movement briefly
3. Commands both motors to stop

If both tracks move together in the expected direction and then stop, locomotion is considered functional.

If the tracks move together but in the opposite vehicle direction, the I²C path and motor channels are still functioning; establish the correct CW/CCW mapping for that physical orientation before continuing.

### How to run the proof script

Open `V2_PROOF_OF_LIFE.py` in Thonny with the ESP connected and run it directly as a temporary/manual proof. It does **not** replace the permanent root `/main.py`, does **not** become part of the permanent runtime, and normal V1 remains the baseline after the test.

---

## Proof-of-Life Script

```python
from machine import Pin, I2C
import time

# I2C setup
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)
ADDR = 0x14

# Motor IDs
MOTOR_A = 0
MOTOR_B = 1

# Command codes
CMD_RUN_CW = 0x02
CMD_STOP   = 0x01

def send(cmd, motor, speed=0):
    i2c.writeto(ADDR, bytes([cmd, motor, speed]))

# Run both motors in the tested forward direction for this build
send(CMD_RUN_CW, MOTOR_A, 200)
send(CMD_RUN_CW, MOTOR_B, 200)

time.sleep(2)

# Stop both motors
send(CMD_STOP, MOTOR_A)
send(CMD_STOP, MOTOR_B)
```

---

## Expected Behaviour

When the script is run:

- Both tracks move together
- Direction matches the mapping established for the physical build
- Movement is smooth and controlled
- Both tracks stop together after the delay

If only one side behaves differently, stop and verify that side's motor/channel wiring before continuing.

---

## Stop Condition

At this point:

- Locomotion hardware is verified
- Power integration is validated
- Control path is proven
- Forward/reverse mapping for the physical build is understood

No further features are added in this module.

Future work builds **on top of** this capability, not inside it.
