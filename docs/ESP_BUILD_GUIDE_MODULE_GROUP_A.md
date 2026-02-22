# MODULE GROUP A — ESP CORE STACK (ENZO V1)

> **Purpose:** Build a complete, working “ESP stack” (controller + indicators + sensors) **on the bench first**, before you mount anything onto the robot chassis.
> When this module is finished, you should be able to plug the ESP in via USB and see ENZO “come alive”.

---

## What this module produces

A self‑contained ESP assembly with:
- **Heartbeat LED** (system alive indicator)
- **Wi‑Fi LED** (network status indicator)
- **8‑LED “Eyes” NeoPixel** output
- **PIR sensor** input (motion)
- **LDR** input (light level)
- **Mode / Big button** input

All wires should exit the stack as a tidy bundle (a “tail”), ready to mount later.

---

## Hardware baseline (important)

**ENZO V1 is pinned and documented for an ESP32‑S3 dev board.**

If you use a different ESP32 (e.g. ESP32‑WROOM / “Vroom”), ENZO **may not run as‑is** because:
- the **GPIO pinout is different**
- some boards have different boot‑strap pins and LED wiring
- the physical header layout differs

**For V1, use the ESP32‑S3 baseline.** Support for other boards is a later (V2+) project.

---

## Pin map (locked for ENZO V1)

These are the pins ENZO V1 code expects:

| Function | Pin |
|---|---:|
| Heartbeat LED | **GPIO 2** |
| Wi‑Fi LED | **GPIO 12** |
| LDR analog input | **GPIO 7** |
| PIR input | **GPIO 14** |
| Eyes (NeoPixel data) | **GPIO 16** |
| Mode / Big button | **GPIO 4** |
| (Optional) Aux button (reserved) | **GPIO 5** |

> If your hardware uses different pins, **change the constants in `config.py` / `tasks.py`** to match (and document it for your build).

---

## A0 — Software sanity check (before wiring)

This module assumes you have already followed **SOFTWARE_SETUP** and copied the ENZO files to the ESP.

1. Plug ESP into your PC via USB.
2. Open Thonny / your serial REPL.
3. Confirm there are **no import errors** on boot.
4. Confirm you can run the firmware (usually it auto‑runs via `main.py`).

If you see errors, fix software first (it’s much easier before you have a nest of wires).

---

## A1 — Mount the ESP “stack” (bench build)

**Goal:** secure the ESP so you can wire it without ripping pads off. "Foam block"

Recommended approach:
- mount the ESP onto a small **perfboard / protoboard**
- use standoffs so the board is protected and doesn’t short on metal
- label the board edge with the key GPIO numbers (2, 4, 7, 12, 14, 16)

This becomes the “core module” you later bolt onto ENZO’s deck.

---

## A2 — Wire the Heartbeat LED (GPIO 2)

**What it teaches:** basic GPIO output + LED + resistor + “alive” indicator.

**Parts**
- 1× LED
- 1× resistor (typically **220–330 Ω**)
- hookup wire

**Wiring**
- **GPIO2 → resistor → LED anode (+)**
- **LED cathode (–) → GND**

**Test**
- Power the ESP by USB.
- You should see a repeating heartbeat pattern.

> If your LED never lights, flip it around (LED polarity matters).

---

## A3 — Wire the Wi‑Fi LED (GPIO 12)

**What it teaches:** status indicator LED + mapping “state” to a physical signal.

**Parts**
- 1× LED
- 1× resistor (**220–330 Ω**)

**Wiring**
- **GPIO12 → resistor → LED anode (+)**
- **LED cathode (–) → GND**

**Test**
- On boot, the Wi‑Fi indicator should follow whatever the firmware uses for network state.

---

## A4 — Wire the “Eyes” (8‑LED NeoPixel on GPIO 16)

**What it teaches:** addressable LEDs + data timing + safe wiring.

**Parts**
- 1× NeoPixel / WS2812 8‑LED module
- (Recommended) 1× data resistor (**330–470 Ω**) in series
- (Recommended) 1× capacitor (**≥ 470 µF**) across 5V/GND near the LEDs

**Wiring**
- **5V → NeoPixel 5V**
- **GND → NeoPixel GND**
- **GPIO16 → (330–470 Ω) → NeoPixel DIN**

**Test**
- On boot you should see the ENZO boot animation then idle “eyes”.

> If the NeoPixels flicker randomly, check ground quality and add the capacitor.

---

## A5 — Wire the PIR sensor (GPIO 14)

**What it teaches:** digital input and real‑world sensor behaviour.

**Typical PIR pins:** VCC, OUT, GND

**Wiring**
- **PIR VCC → 5V** *(most PIR modules expect 5V; many also work on 3.3V, but don’t assume)*
- **PIR GND → GND**
- **PIR OUT → GPIO14**

**Test**
- Leave the PIR still for ~30–60 seconds to settle.
- Move your hand in front of it; ENZO should react.

---

## A6 — Wire the LDR (GPIO 7)

**What it teaches:** analog reading + voltage divider.

**Parts**
- 1× LDR (photoresistor)
- 1× fixed resistor (start with **10 kΩ**)
- hookup wire

**Wiring (voltage divider)**
- **3.3V → LDR → node → resistor → GND**
- **node → GPIO7**

**Test**
- Cover the LDR with your finger: readings should shift.
- Shine a light: readings should shift the other way.

---

## A7 — Wire the Mode / Big Button (GPIO 4)

**What it teaches:** button input + pull‑ups + debouncing.

**Wiring (simple)**
- One leg of the button → **GPIO4**
- Other leg → **GND**

Firmware uses an internal pull‑up (so the pin reads HIGH normally, LOW when pressed).

**Test**
- Press the button; ENZO should change mode / brightness / behaviour depending on your firmware build.

---

## A8 — (Optional) Aux button (GPIO 5)

GPIO5 is reserved for expansion. If you wire a second button, document what you use it for (V2+).

---

## A9 — Grounding philosophy (don’t overthink this)

You **do not** need to move every sensor ground wire to the future ground rail.

Correct approach:
- In Module A, everything can share the ESP’s **local ground** (common GND).
- In Module Group B/C, you add **one “ground motorway” wire** from ESP GND to the **ground bus bar**, so the whole robot shares a stable reference.

That’s it.

---

## Completion criteria (Module Group A)

You’re done with Module Group A when:

- [ ] ESP boots with **no import errors**
- [ ] Heartbeat LED works (GPIO2)
- [ ] Wi‑Fi LED behaves as expected (GPIO12)
- [ ] NeoPixel eyes run and idle cleanly (GPIO16)
- [ ] PIR triggers reliably (GPIO14)
- [ ] LDR readings change with light (GPIO7)
- [ ] Mode button is detected (GPIO4)
- [ ] Wiring is bundled and labelled (so later mounting is easy)

---

## Next module

Proceed to **MODULE GROUP B — POWER SYSTEM** once your ESP stack is stable.
