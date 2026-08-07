# MODULE GROUP E — V2 PHASE 2  
## PC MANUAL LOCOMOTION (USB SERIAL)

---

## Why This Module Exists

This module is a learning and bring-up stage between basic motor proof and mobile control.

It proves that ENZO can accept an external command source while the ESP remains responsible for motor behaviour and the deadman STOP condition.

Phase 2 is recommended if you want to understand the control path before moving to Phase 3.

---

## What This Module Does

Phase 2 temporarily replaces ENZO's normal `main.py` with a drive-only runtime.

During this lesson:

- the PC reads your keyboard
- the PC sends `W / A / S / D / X` over USB serial
- the ESP receives those commands
- the ESP drives the motor controller over I²C
- the ESP stops the motors if valid commands stop arriving

The normal V1 runtime is not deleted from the project, but it is **not running while the temporary Phase 2 `main.py` is installed**.

---

## Files Used in This Module

| File | Runs on | Purpose |
|---|---|---|
| [`keyboard_to_serial.py`](keyboard_to_serial.py) | PC — Python 3 | Reads keyboard input and sends repeated movement commands over USB serial |
| [`main.py`](main.py) | ESP32 — MicroPython | Temporary Phase 2 runtime; receives commands, controls motors and enforces the 250 ms deadman |

The permanent V1 runtime you return to afterwards is here:

[`../V1END_V2_START_BASELINE_CODE/main.py`](../V1END_V2_START_BASELINE_CODE/main.py)

---

## PC Requirements

You need:

- Python 3.x
- `pip`
- `pyserial`
- `pynput`

Install the two packages with:

```text
pip install pyserial pynput
```

MicroPython on ENZO and Python on the PC are separate environments.

---

## Before You Start

1. Complete Phase 1 and prove the motor driver works.
2. Keep ENZO lifted so the tracks cannot unexpectedly drive across the bench.
3. Find ENZO's USB serial port on the PC.
4. Open [`keyboard_to_serial.py`](keyboard_to_serial.py) and change:

```python
PORT = "COM7"
```

to the port actually used by your ESP.

On Linux/macOS the port name will not be `COM7`; use the serial device name shown by your system.

---

## Step 1 — Install the temporary Phase 2 runtime

Using Thonny with the **MicroPython** interpreter:

1. Open [`main.py`](main.py).
2. Save it to the **root of the ESP** as exactly:

```text
/main.py
```

3. Reset ENZO.
4. Confirm the serial output includes:

```text
WASD DRIVE READY (W forward, S reverse, X/space stop)
```

This temporary `main.py` is now the ESP runtime for this lesson.

---

## Step 2 — Give the PC controller access to the serial port

The PC sender and Thonny cannot both own the same serial port at the same time.

After the Phase 2 `main.py` is saved and running:

1. Release/disconnect Thonny from ENZO's MicroPython serial port, or switch away from the MicroPython interpreter.
2. Run [`keyboard_to_serial.py`](keyboard_to_serial.py) using **Local Python 3**.
3. Confirm you see:

```text
Serial open on COM7
```

using your actual port name.

---

## Step 3 — Drive ENZO

Controls:

- hold **W** → forward
- hold **S** → reverse
- hold **A** → left turn
- hold **D** → right turn
- release a movement key → STOP
- press **Space** → STOP
- press **Esc** → STOP and exit the PC controller

The PC sender refreshes the active command every **120 ms** while a movement key is held.

The ESP deadman is **250 ms**. If commands stop arriving for longer than that, the ESP commands STOP.

That means motor safety lives on the ESP; it does not depend on the PC successfully sending a final STOP packet.

---

## First Test — Required

Keep ENZO lifted off the ground.

Test:

1. **W** — both tracks should drive forward.
2. **S** — both tracks should reverse.
3. **A / D** — confirm the expected left/right movement.
4. Release each key — movement must stop.
5. While holding a movement key, terminate the PC script or disconnect the serial link — ENZO should stop after the deadman timeout.

Do not continue until STOP behaviour is reliable.

---

## If Forward and Reverse Are Wrong

Do **not** start rewiring a known-good motor installation just to correct command direction.

In [`main.py`](main.py), find:

```python
FWD_CMD = CMD_RUN_CCW
REV_CMD = CMD_RUN_CW
```

If forward and reverse are physically inverted on your build, swap those two assignments:

```python
FWD_CMD = CMD_RUN_CW
REV_CMD = CMD_RUN_CCW
```

Retest **W** and **S** with the tracks lifted.

If only one side is wrong, stop and verify the motor/channel wiring against the known-good Phase 1 result rather than blindly changing both direction mappings.

---

## Leaving Phase 2 — Important

Resetting ENZO **does not** restore V1 while the temporary Phase 2 `main.py` is still installed. A reset simply runs that same Phase 2 file again.

To return ENZO to its normal V1 runtime:

1. Stop the PC controller.
2. Reconnect Thonny using the **MicroPython** interpreter.
3. Restore the permanent V1 [`main.py`](../V1END_V2_START_BASELINE_CODE/main.py) to the ESP root as `/main.py`.
4. Reset ENZO.
5. Confirm the normal V1 behaviours return.

The rest of the V1 files remain in place; Phase 2 only needs the temporary root `main.py` for this lesson.

---

## What Phase 2 Proves

When complete, you have proven:

- an external PC can command ENZO over USB serial
- the ESP remains the motor-control authority
- command transport and motor behaviour are separate concerns
- STOP on command loss is enforced locally on the ESP
- the original V1 runtime can be restored intact after the lesson

Phase 3 changes the transport from PC USB serial to ENZO's own Wi-Fi access point and HTTP control.

---

## Completion Check

- [ ] Correct PC serial port configured
- [ ] Phase 2 `main.py` installed and boots
- [ ] PC controller opens the serial port
- [ ] W / S / A / D produce the expected movement
- [ ] Release sends STOP
- [ ] Deadman stops ENZO if commands disappear
- [ ] Permanent V1 `main.py` restored after the lesson
- [ ] Normal V1 behaviour returns after reset

When these are true, Phase 2 is complete.
