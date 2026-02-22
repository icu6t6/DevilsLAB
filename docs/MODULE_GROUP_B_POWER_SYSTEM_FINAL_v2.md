# MODULE GROUP B – POWER SYSTEM (ENZO v1)

This module covers **bringing the robot to life electrically**, before the ESP stack is powered.
Nothing in this module depends on firmware or GPIO configuration.  
You can complete **Module Group B** with the ESP completely disconnected.

This reflects how ENZO was actually built.

---

## PURPOSE OF MODULE GROUP B

By the end of this module you will have:

- A **stable input rail**
- A **common ground rail**
- A **regulated 5V rail**
- A **latching power button** that controls the 5V logic rail
- A safe way to test power *before* connecting the ESP

This teaches:
- Power sequencing
- Ground discipline
- Rail isolation
- Safe bring‑up methodology

---

## MODULE B1 – INPUT-RAIL & FUSE

**Goal:** Create a protected input source.

### Parts
- 2-cell LiPo Battery
- Deans connector 
- Double connecting block-connect one end of fuse and 14 AWG wire from GRN Rail
- Inline fuse holder + fuse
- input rail bus bar
- Heavy‑gauge wire (14–16 AWG)

### Steps
1. Do **NOT** connect the Battery yet
2. Wire the Deans connector **positive → fuse** 
3. Fuse output → **input bus bar**
4. + side after connecting block to fuse and - GND → **ground rail**

At this stage:
- input rail exists
- No loads connected
- Safe to measure with a multimeter

---

## MODULE B2 – GROUND RAIL

**Goal:** Establish a single electrical reference.

### Rules
- The chassis is **NOT** ground
- Ground rail floats above chassis
- All grounds eventually meet here

### Steps
1. Mount ground rail on insulated standoffs
2. Connect Deans - ground to ground rail after connecting block
3. Do **not** connect ESP yet

This ground rail will later accept:
- Buck converter ground
- ESP ground (single heavy wire)
- Button LED ground

---

## MODULE B3 – BUCK CONVERTER (input rail → 5V)

**Goal:** Create a regulated logic supply.

### Parts
- UBEC / buck converter
- Voltmeter (optional but recommended)

### Steps
1. Buck **IN + → input rail**
2. Buck **IN − → ground rail**
3. Buck **OUT + → temporary test lead**
4. Buck **OUT − → ground rail**
5. Adjust buck to **5.0–5.2V**

At this point:
- You can power the buck safely
- ESP is still disconnected

---

## MODULE B4 – 5V RAIL

**Goal:** Distribute regulated logic power.

### Steps
1. Mount 5V rail above ground rail "will be above the ESP32 clam"
2. Buck OUT + → **C1 on latching button**
3. Do NOT connect ESP yet

Nothing else connects to this rail yet.

---

## MODULE B5 – LATCHING POWER BUTTON (LOGIC ENABLE)

**Goal:** Control when logic power is enabled.

### Button Type
- Latching (press ON / press OFF)
- Separate LED pins
- NO / NC / COM terminals

### Wiring
- Buck OUT + → **C1**
- **NO1 → A on the 5V rail**
- Button LED + → ** slot 1 on 5V rail**
- Button LED − → **ground rail**
- NC1 unused -
### Result
- Button OFF → no 5V rail
- Button ON → 5V rail live + LED illuminated

This is intentional and mirrors real equipment.

---

## MODULE B6 – SAFE TESTING (NO ESP)

Before connecting the ESP:

- Power the system
- Measure:
  - input rail V
  - Buck output
  - 5V rail
- Verify:
  - Button correctly enables/disables 5V
  - No heat buildup
  - No unexpected voltage

# Early Power Validation (optional)
Before perminant powerinstalation, a low-current source may be connected to the input rail to verify buck converter operation
and downstream 5V distrobution.
This step intended only for validation and should be performed without logic or high current loads connected.

---

## WHEN TO STOP

If you can:
- Toggle 5V on/off with the button
- Read stable voltages
- See the button LED behave correctly

**STOP.**

Only now do you proceed to:
➡️ Module Group A (ESP stack) connection  
➡️ Module Group C (mechanical assembly)

---

## WHY THIS ORDER MATTERS

Most beginners destroy boards by:
- Powering logic before regulation
- Floating grounds
- Hot‑plugging rails

This module exists specifically to prevent that.

---

**END OF MODULE GROUP B**
