# MODULE GROUP B – POWER SYSTEM (ENZO v1)

This module covers **bringing the robot to life electrically**, before the ESP stack is powered.
Nothing in this module depends on firmware or GPIO configuration.
You can complete **Module Group B** with the ESP completely disconnected.

This reflects how ENZO was actually built.

---

## PURPOSE OF MODULE GROUP B

By the end of this module you will have:

- a **stable input rail**
- a **common ground rail**
- a **regulated 5V rail**
- a **latching power button** that controls the 5V logic rail
- a safe way to test power *before* connecting the ESP

This teaches:
- power sequencing
- ground discipline
- rail isolation
- safe bring-up methodology

---

## MODULE B1 – INPUT RAIL & FUSE

**Goal:** Create a protected input source.

### Parts
- 2-cell LiPo battery
- Deans connector
- double connecting block
- inline fuse holder + fuse
- input rail bus bar
- heavy-gauge wire (14–16 AWG)

### Steps
1. Do **NOT** connect the battery yet.
2. Wire the Deans connector **positive → fuse**.
3. Wire the fuse output → **input bus bar**.
4. Connect the battery negative → **ground rail**.
5. Use the double connecting block where needed to join the fused positive path and the ground return cleanly into the rail layout.

At this stage:
- the input rail exists
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
1. Buck **IN + → input rail**
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

## MODULE B6 – SAFE TESTING (NO ESP)

Before connecting the ESP:

- power the system
- measure:
  - input rail voltage
  - buck output
  - 5V rail
- verify:
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
- see the button LED behave correctly

**STOP.**

Only now do you proceed to:
➡️ [Module Group A (ESP stack) connection](ESP_BUILD_GUIDE_MODULE_GROUP_A.md)

---

## WHY THIS ORDER MATTERS

Most beginners destroy boards by:
- powering logic before regulation
- floating grounds
- hot-plugging rails

This module exists specifically to prevent that.

---

**END OF MODULE GROUP B**
