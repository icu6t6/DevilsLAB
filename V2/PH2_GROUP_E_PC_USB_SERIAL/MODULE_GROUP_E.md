# MODULE GROUP E — V2 PHASE 2  
## PC MANUAL LOCOMOTION (USB SERIAL)

---

## Why This Module Exists

This module exists **primarily as a learning and bring-up tool**.

Experienced builders may choose to bypass this module entirely and proceed directly to Phase 3 (mobile UI control). Doing so will still result in a working system.

However, learners are encouraged to complete this module to understand:

- how external input enters the system  
- how control is transported and gated  
- how STOP and safety are enforced  
- how ENZO is brought up incrementally and provably  

This module demonstrates the **middle ground** between “it works” and “here is how we got there”.

Completion of this module is **not required** for Phase 3 functionality, but it provides valuable insight for curious builders who want to understand the system boundaries before moving on.

---

## What This Module Does

This module runs ENZO in a **temporary manual drive mode** using a PC keyboard.

While manual drive is active, ENZO boots into a locomotion-focused runtime.  
During this time, **other ENZO features may not run**.

Existing ENZO features are **not deleted**.  
Stopping the PC control script and/or resetting ENZO returns the system to its normal firmware behaviour.

---

## PC Requirements (Read Before Starting)

This module requires **Python to be installed on your computer**.

If you have previously only worked with MicroPython on the ESP, you may not yet have a full PC Python environment set up.

### Required on the PC

- Python 3.x installed  
- `pip` available  
- The following Python packages installed:
  - `pyserial`
  - `pynput`

These packages are used by the PC controller script to:
- read keyboard input
- send commands over USB serial

Once these requirements are met, you will **first run the PC controller script**, then **load the drive firmware onto ENZO**.

---

## Installing the Required Packages

1. Open a terminal or command prompt on your computer  
2. Run:
   ```
   pip install pyserial pynput
   ```

If the install completes without errors, the PC environment is ready.

If this step is skipped, the PC control script will not run.

---

## Common Clarification

MicroPython on the ESP and Python on your PC are **separate environments**.

Installing Python packages on your PC does **not** affect the ESP, and vice versa.

---

## Files Used in This Module

In this module you will **run one script on your PC** and **copy one script onto the ESP**.

| File | Runs on | Purpose |
|---|---|---|
| `keyboard_to_serial.py` | PC (Local Python 3) | Reads keyboard input and sends commands over USB serial |
| `main.py` | ESP32 (MicroPython) | Receives commands and drives locomotion |

These scripts run at the same time in **different execution contexts**, even though they are launched from the same computer using Thonny.

---

## Module Phase 2 Behaviour

This phase places ENZO into a **manual drive session**.

The ESP runs a drive-focused `main.py` that:
- listens for external commands
- controls locomotion
- enforces STOP and safety rules

This drive firmware is intended for **manual control sessions only** and is not the normal ENZO runtime.

---

## Part 1 — PC Controller Script

### File
```
keyboard_to_serial.py
```

### Where to save it
- On the **PC**
- Anywhere convenient (Desktop is fine)
- **Do not upload this file to the ESP**

### Interpreter
- Thonny
- **Local Python 3**

### What it does
- Reads keyboard input  
- Sends single-character commands over USB serial:
  - `W`, `A`, `S`, `D`
- Sends `X` (STOP) on:
  - key release
  - space bar  
- Opens the ENZO USB serial port (e.g. COM7)

The PC does **not** control motors directly.

---

### How to run it

1. Plug ENZO into the PC  
2. Open Thonny  
3. Set the interpreter to **Local Python 3**  
4. Open `keyboard_to_serial.py`  
5. Run the script  

You should see output similar to:
```
Serial open on COM7
```

Leave this script **running**.

---

## Part 2 — ENZO Drive Firmware

### File
```
main.py
```

### Where to save it
- On the **ESP32**
- Root of the device
- Filename must be exactly `main.py`

This file runs automatically when ENZO boots.

---

### What it does
- Reads incoming USB serial data  
- Maps characters to motor commands:
  - `W` → forward  
  - `S` → reverse  
  - `A / D` → pivot turns  
  - `X / Space / timeout` → STOP  
- Enforces a deadman timeout  
- Uses **known-good I²C motor commands**

The ESP is the **authority** for safety.

---

### How to install it

1. In Thonny, switch interpreter to:
   ```
   MicroPython (Generic ESP32)
   ```
2. Open `main.py`  
3. Save it **to the ESP**  
4. Reset ENZO  

---

## Running the System (Normal Use)

This is the correct Thonny workflow.

### Step 1 — Start the PC script
- Interpreter: **Local Python 3**
- Run `keyboard_to_serial.py`
- Leave it running

### Step 2 — Run the ESP firmware
- Switch interpreter to **MicroPython**
- Reset ENZO (or run `main.py`)

Thonny handles the connection switching automatically.

---

## Expected Behaviour

- Hold **W** → ENZO moves  
- Release **W** → STOP  
- Hold **A / D** → pivot  
- Hold **S** → reverse  
- Press **Space** → STOP  
- Exit PC script → STOP  

Motion only occurs while input is active.

---

## First Test (Required)

- Lift ENZO off the ground  
- Test all directions briefly  
- Confirm STOP works immediately  

If direction is wrong:
- Fix it in `main.py`
- Do not rewire motors

---

## Exiting Manual Drive

To stop using manual drive:
- Exit the PC script **or**
- Reset ENZO  

ENZO returns to its normal firmware behaviour.

Manual drive does not persist.

---

## What This Enables

Because of this module:

- ENZO can accept external control safely  
- Locomotion is decoupled from input  
- Existing ENZO features remain intact **in the codebase and return after exiting manual drive**

In Phase 3, the PC control script is replaced by a **mobile UI input script**.  
The ESP-side safety and locomotion logic does not need to change.

---

## Completion Check

- [ ] PC script runs  
- [ ] ESP firmware runs  
- [ ] Forward / reverse work  
- [ ] STOP works on release  
- [ ] STOP works on disconnect  
- [ ] No ENZO features permanently altered  

When complete:

**V2 Phase 2 is locked.**
