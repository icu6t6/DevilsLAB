# MODULE GROUP B – POWER SYSTEM (ENZO v1)

This module covers **bringing the robot to life electrically**, before the ESP stack is powered.
Nothing in this module depends on firmware or GPIO configuration.
You can complete **Module Group B** with the ESP completely disconnected.

This reflects how ENZO was actually built.

---

## PURPOSE OF MODULE GROUP B

By the end of this module you will have:

- a **stable protected input rail**
- a **common ground rail**
- a **regulated 5V rail**
- a **latching power button** that controls the 5V logic rail
- the V1 **three-Schottky protection / isolation arrangement** documented
- a safe way to test power *before* connecting the ESP

This teaches:
- power sequencing
- reverse / back-feed protection
- ground discipline
- rail isolation
- safe bring-up methodology

---

## MODULE B1 – INPUT RAIL, FUSE & MAIN SCHOTTKY

**Goal:** Create a protected input source.

### Parts
- 2-cell LiPo battery
- Deans connector
- double connecting block
- inline fuse holder + fuse
- **1× main-path Schottky diode**
- input rail bus bar
- heavy-gauge wire (14–16 AWG)

### Steps
1. Do **NOT** connect the battery yet.
2. Wire the Deans connector **positive → fuse**.
3. Wire the fuse output → **main Schottky diode → input/source bus bar**.
4. Orient the main Schottky with its **band toward the source rail / downstream side**.
5. Connect the battery negative → **ground rail**.
6. Use the double connecting block where needed to join the positive path and ground return cleanly into the rail layout.

Canonical battery path:

```text
Battery → Fuse → Main Schottky → Source/Input Rail → Buck Converter → Latching Switch → 5V Rail
```

At this stage:
- the protected input rail exists
- no loads are connected
- it is safe to measure with a multimeter

---

## MODULE B2 – GROUND RAIL

**Goal:** Establish a single electrical reference.

### Rules
- The chassis is **NOT** ground.
- The ground rail floats above the chassis.
- All grounds eventually meet here.

### Steps
1. Mount the ground rail on insulated standoffs.
2. Connect battery negative to the ground rail.
3. Do **not** connect the ESP yet.

This ground rail will later accept:
- buck converter ground
- ESP ground (single heavy wire)
- button LED ground

---

## MODULE B3 – BUCK CONVERTER (INPUT RAIL → 5V)

**Goal:** Create a regulated logic supply.

### Parts
- UBEC / buck converter
- voltmeter (optional but recommended)

### Steps
1. Buck **IN + → protected input/source rail**
2. Buck **IN − → ground rail**
3. Buck **OUT + → temporary test lead**
4. Buck **OUT − → ground rail**
5. Historical V1 used a fixed-output RC-style 5V / 3A UBEC; there was no adjustment. A replacement may be fixed or adjustable, but it must provide regulated nominal 5V at least 3A continuous and its input range must suit the 2S source.
6. Record the protected input voltage and unloaded output before connecting the ESP. Historical V1 was about 5.28–5.30V at the 5V rail because its RC-style UBEC was fixed-output. For a replacement, use regulated nominal 5V at least 3A continuous and measure UBEC output, 5V rail and ESP 5V header; do not tune a replacement to 5.30V merely to reproduce the historical reading.

At this point:
- you can power the buck safely
- the ESP is still disconnected

---

## MODULE B4 – 5V RAIL

**Goal:** Distribute regulated logic power.

### Steps
1. Mount the 5V rail above the ground rail.
2. Buck **OUT + → C1 on the latching button**.
3. Do **not** connect the ESP yet.

Nothing else connects to this rail yet.

---

## MODULE B5 – LATCHING POWER BUTTON (LOGIC ENABLE)

**Goal:** Control when logic power is enabled.

### Button Type
- latching (press ON / press OFF)
- separate LED pins
- NO / NC / COM terminals

### Wiring
- Buck **OUT + → C1**
- **NO1 → 5V rail input**
- Button LED **+ → 5V rail**
- Button LED **− → ground rail**
- **NC1** unused

### Result — battery-only Module B test, ESP disconnected
- Button OFF → buck feed disconnected from the 5V rail
- Button ON → buck supplies the 5V rail and the button LED illuminates

After integration, USB can supply the 5V rail through Channel A even when the button is OFF. Disconnect the battery and USB before changing wiring; the button is not an all-source disconnect.

This is intentional and mirrors real equipment.

---

## MODULE B5A – ESP / USB 5V SCHOTTKY ISOLATION

ENZO V1 uses **two additional SR560 Schottky diodes** as opposite-direction supply paths between the ESP 5V header and the 5V rail; the main path uses a third SR560. The Waveshare ESP32-S3-DEV-KIT-N8R8 also has onboard USB diode D1, which provides the board-side reverse-current block toward USB VBUS. The external pair alone does not guarantee the reverse-drive behaviour of an arbitrary replacement UBEC.

See the [Schottky reference](V1%20schottky%20OR-ing%20method.txt) for the original operating record and the limits of that evidence.

These are in addition to the main-path Schottky from Module B1, making **three Schottky diodes total in the V1 arrangement**.

### Channel A — USB / ESP → 5V Rail
- ESP32-S3 **5V pin → Schottky → 5V rail**
- diode **band faces the 5V rail**

### Channel B — 5V Rail → ESP
- **5V rail → Schottky → ESP32-S3 5V pin**
- diode **band faces the ESP**

Do not connect the ESP until the rail tests in Module B6 have passed. Install / verify these two channels during final ESP integration using the Wiring Reference and the dedicated V1 Schottky reference.

---

## MODULE B6 – SAFE TESTING (NO ESP)

Before connecting the ESP:

- power the system
- measure:
  - input rail voltage after the main Schottky
  - buck output
  - 5V rail
- verify:
  - the main Schottky polarity is correct
  - the button correctly enables/disables 5V
  - no heat buildup
  - UBEC output, 5V rail and ESP 5V header measured and recorded; the historical 5.28–5.30V rail reading is a reference for the original fixed UBEC, not a universal target
  - no power-source connection has been inferred from a wire colour or terminal position

### Early Power Validation (optional)
Before permanent power installation, a low-current source may be connected to the input rail to verify buck converter operation and downstream 5V distribution.

This step is intended only for validation and should be performed without logic or high-current loads connected.

---

## WHEN TO STOP

If you can:
- toggle 5V on/off with the button
- read stable voltages
- confirm the main Schottky is correctly oriented
- see the button LED behave correctly

**STOP.**

Module Group A should already have been completed and proven independently on USB bench power.
Only now proceed to **final integration of the completed Module A ESP stack with the completed Module B power system**, using the [V1 Wiring Reference](WIRING_REFERENCES_T1_ENZO_v1_COMBINED.md) and the [V1 Schottky OR-ing reference](V1%20schottky%20OR-ing%20method.txt).

---

## WHY THIS ORDER MATTERS

Most beginners destroy boards by:
- powering logic before regulation
- floating grounds
- hot-plugging rails
- allowing power sources to back-feed each other

This module exists specifically to prevent that.

---

**END OF MODULE GROUP B**
