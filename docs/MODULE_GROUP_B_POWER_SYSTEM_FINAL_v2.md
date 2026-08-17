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
5. Adjust the buck to **5.0–5.2V**

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

### Result
- Button OFF → no 5V rail
- Button ON → 5V rail live + LED illuminated

This is intentional and mirrors real equipment.

---

## MODULE B5A – ESP / USB 5V SCHOTTKY ISOLATION

ENZO V1 uses **two additional Schottky diodes** around the ESP 5V connection so battery/rail power and USB power can coexist without direct back-feed.

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
  - no unexpected voltage

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
