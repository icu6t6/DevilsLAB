# Lesson — Phase 3: Mobile Manual Locomotion (V2)

## Lesson Position

This lesson sits **after Phase 2** and before any autonomy or higher-level behaviour.

It teaches how to add **mobile manual control** to ENZO **without breaking or replacing** existing functionality.

Phase 3 is treated as a **tool**, not a takeover.

---

## Lesson Goal

By the end of this lesson:

- ENZO can be driven from a phone using a browser
- No USB cable is required
- ENZO still stops immediately when control is released
- Existing ENZO behaviour is not permanently altered

---

## Prerequisites

Before starting this lesson, you must have:

- Completed **Phase 2 – Manual Locomotion**
- Proven that ENZO responds correctly to:
  - `W` = forward
  - `S` = reverse
  - `A` = left
  - `D` = right
  - `X` = stop
- Observed that ENZO:
  - Moves only while commands are actively received
  - Stops when commands stop

If Phase 2 is not working, stop here.

---

## Files Used in This Lesson

This lesson uses **two files**.

### ESP-Side (runs on ENZO)

**File:** `Phase-3_AP_HOST_main.py`

**Purpose:**

- Runs ENZO as a Wi-Fi Access Point
- Hosts a simple web control page
- Receives locomotion commands over HTTP
- Injects commands into the existing locomotion control path
- Enforces deadman safety

**How it is used:**

- Upload this file to ENZO **as `main.py`**
- This temporarily replaces the normal runtime
- This is intentional for bring-up

---

### Phone-Side (control interface)

**File:** `enzo.host.html`

**Purpose:**

- Provides on-screen buttons for locomotion
- Sends `W / A / S / D / X` commands to ENZO over HTTP

**How it is used:**

- If provided as `.html`, open it directly in a browser
- If provided as `.py`, copy the contents and save as `enzo.host.html`
- No build step is required

---

## Step 1 — Run the Phase 3 Host on ENZO

1. Copy `Phase-3_AP_HOST_main.py` to ENZO
2. Rename it to `main.py`
3. Reboot ENZO

You should see output indicating:

- ENZO Wi-Fi Access Point is active
- An IP address is shown (typically `192.168.4.1`)

---

## Step 2 — Connect Your Phone to ENZO

1. On your phone, open Wi-Fi settings
2. Connect to ENZO’s Wi-Fi network
3. Ignore any “no internet” warnings

This is expected.

ENZO **is** the network.

---

## Step 3 — Open the Control Page

You may use either method below.

### Option A — Page Hosted by ENZO (recommended)

1. Open a browser on the phone
2. Navigate to the IP address shown by ENZO
3. The control page loads from ENZO

---

### Option B — Local HTML File (teaching path)

1. Open `enzo.host.html` on the phone
2. Buttons send commands to ENZO over HTTP

This option exists to demonstrate that:

- The UI itself is not special
- Only the transport matters

---

## Step 4 — Drive ENZO

1. Press and hold a movement button
2. Observe ENZO move
3. Release the button
4. Observe ENZO stop immediately

Repeat for all directions.

ENZO should stop if:

- You release the button
- The page loses focus
- The connection drops

---

## What to Observe During This Lesson

While driving ENZO, observe that:

- The same commands from Phase 2 are being used
- Only the **source** of commands has changed
- Safety behaviour is unchanged
- ENZO does not continue moving on its own

If ENZO briefly moves and then stops, this is the deadman safety working.

---

## What This Lesson Teaches

This lesson demonstrates that:

- Manual control does not depend on USB
- Safety does not depend on a PC
- Transport can change without changing behaviour
- Safety must live at the receiver

ENZO has not become autonomous.

Control has become **portable**.

---

## V2 Intent (Important)

In V2, mobile control is treated as a **tool**, not a replacement.

The intended behaviour is:

- ENZO runs normally
- Mobile control can be enabled at any time
- Control can be released without rebooting
- ENZO continues operating as before

This lesson proves that capability.

---

## Lesson Complete When

This lesson is complete when:

- ENZO can be driven from a phone
- USB is not required
- ENZO stops when input stops
- Behaviour matches Phase 2
- Existing ENZO functionality is unaffected

---

End of Lesson — Phase 3
