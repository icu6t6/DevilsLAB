# T-1 ENZO v1 — Overview

## What is T-1 ENZO?

T-1 ENZO is an educational ESP32 firmware and reference build platform.

It is designed to teach real-world electronics, power systems, wiring discipline, and firmware structure — not just “plug it in and it works”.

You build and test an ESP32-S3 sensor/UI assembly, build its protected battery and 5V power system, and integrate them. The tracked ENZO shows one physical installation; a tracked chassis is optional for V1 Free.

This is not a toy and not a finished consumer robot.
It is a learning platform.

---

## Who is this for?

T-1 ENZO is for people who:

- Want to learn ESP32 properly, not just blink LEDs
- Want to understand power rails, grounds, buck converters, and sensors
- Are comfortable learning step-by-step, even if new
- Want something physical to build, break, fix, and improve

You do not need formal qualifications.
You do need curiosity and patience.

---

## What will you learn?

By completing T-1 ENZO v1, you will learn:

- How to safely distribute input rail source power "2-cell LiPo" and 5V power in a mobile system
- What a common ground is and why it matters
- How to use buck converters correctly
- How to wire sensors, LEDs, and buttons to an ESP32
- How firmware maps to real hardware pins
- How to flash, edit, and extend MicroPython firmware
- How to structure a project so it can grow

Motor control is introduced later in ENZO V2, after the V1 baseline is complete.

---

## What do you end up with?

At the end, you will have:

- A working ESP32-S3 sensor/UI and power baseline that:
  - Boots with LED status states
  - Reads the documented sensors and responds to buttons
  - Passes Module A, Module B and final integration checks
  - Can be mounted on a suitable insulated base or the reference chassis
- A working understanding of how it actually works
- A project you can modify instead of starting over

---

## What this is NOT

- Not a plug-and-play toy
- Not a polished consumer product
- Not locked-down firmware
- Not “AI out of the box”

Those come later, if you choose.

---

## How long does it take?

- Original author estimate: ~1–3 evenings for the electrical build once parts are available; independent builder timing has not yet been established. Sourcing and custom chassis fabrication can add time.
- Skill level: Beginner → Intermediate
- Tools required:
  - Soldering iron
  - Screwdrivers
  - Multimeter for power and divider checks
  - Computer (Windows/Linux/macOS)
  - Patience

---

## What do you receive?

T-1 ENZO v1 is provided as a digital learning kit, including:

- Step-by-step build guide
- Full wiring instructions
- Editable firmware
- Bill of Materials (BOM)
- Software setup guide

Hardware is sourced separately.

---

## Why does this exist?

This project exists because learning electronics is often:

- too abstract
- too locked down
- too hand-wavy

T-1 ENZO is built around understanding, not shortcuts.

---

## Next Step

If you are following the public V1 build path:

1. Confirm the required parts in the [BOM](BOM_T1_ENZO_v1.md).
2. Continue to [Software Setup](SOFTWARE_SETUP_T1_ENZO_v1_USER.md).
3. Follow Module A, Module B and final wiring integration in the staged order from the [Start Here](README_START_HERE_T1_ENZO_v1-2.md) page.

The [Full Build Guide](BUILD_GUIDE_T1_ENZO_v1-2.md) remains available as an overall reference, but it does not replace the staged public build order.
