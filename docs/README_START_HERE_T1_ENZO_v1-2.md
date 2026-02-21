# T1-ENZO v1 — Educational ESP32 Firmware & Reference Project

## IMPORTANT — READ FIRST
T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.
This project is **NOT a physical product or kit**.

Acknowledgement
This project was designed and developed by the author, with support from an AI assistant used for analysis, discussion, and continuity during development.

## How to Use This Repository (Read Order)

This repository is structured as a **guided baseline build**, not a loose collection of files.

Recommended order:
1. Read this document fully (project scope, rules, completion criteria)
2. Review the Overview and architecture documents
3. Follow the hardware Build Guide
4. Consult the BOM and wiring references
5. Complete Software Setup and flash firmware
6. Verify behaviour against the Completion Criteria

Do not skip steps or mix documents out of order.


**T1-ENZO v1 provides:**
- Firmware
- Pin mappings
- Reference wiring logic
- Documentation
- Educational structure

**T1-ENZO v1 does NOT provide:**
- A robot
- A chassis
- Motors
- Batteries
- Power electronics
- Any assembled hardware

You are expected to source, fabricate, or design your own hardware.

---

## What This Project Is

T1‑ENZO v1 is an **educational embedded‑systems firmware baseline** designed to help learners move from
“I can follow tutorials” to “I can design and reason about a complete system.”

It focuses on:
- Power architecture (Source/input rail → Regulated 5v logic rail → controller )
- Grounding strategy
- GPIO planning
- Modular firmware structure
- Safe expansion paths
- "In v1, the input rail is typically supplied by a 2-cell LiPo battyer but the firmware are power-source-agnostic."

This is **not** a toy demo or copy‑paste project.

T1-ENZO v1 is an educational embedded-systems reference designed to teach real-world power and wiring architecture.
It models how industrial and mobile machines handle raw power: energy enters the system, is protected, regulated, and distributed before reaching logic.
The firmware operates downstream of electrical safety — it never replaces it.

Default power model: 2S battery → protected input/source rail → regulated 5V logic rail → controller & peripherals.
USB power is acceptable for firmware flashing and early bench testing, but the architecture is designed to be battery-powered.

The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
“Builders may replicate this implementation exactly. The power architecture may be reused as a platform, but the firmware + pin map are ESP32-S3 specific.”

Controller support (V1): The ENZO v1 firmware and Pin Truth Map are authored for the ESP32-S3 dev board and the exact pinout documented in this repository.
If you use any other controller (ESP32-WROOM, Pico, Arduino, etc.), the pin map and wiring instructions will not apply.
Adapting ENZO to a different board is outside v1 scope (V2+ territory) and requires your own remapping and validation.

What you may substitute: You may reuse the power architecture (2S → protected input rail → regulated 5V rail → ground rail) as a general-purpose test bench,
and connect your own controller to the 5V/GND rails.
In that case, ENZO’s firmware is not the product you’re using — you’re using ENZO’s electrical baseline.

---

## Who This Is For
You should be comfortable with:
- Arduino / ESP32 basics
- Uploading firmware
- Editing Python files
- Basic electronics concepts

You do **not** need to be an expert.

---

## What You Will Learn
- Why grounding matters
- How to separate high‑current and logic domains
- How to plan GPIO usage
- How to structure firmware cleanly
- How to expand without breaking a baseline

---

## Completion Criteria (v1)
T1‑ENZO v1 is considered complete when:
- Firmware boots successfully
- LEDs respond as expected
- Buttons register correctly
- PIR input is stable
- No pin conflicts exist
- Files are named exactly as specified

---

What Comes After V1

- T1-ENZO v1 is a complete baseline. No further steps are required.

- From this point, builders may:

- Stop here, with a finished and stable embedded system

- Optionally explore T1-ENZO v1 Advanced, which adds diagnostics and validation tools for learning and confidence

- Proceed to ENZO V2, which introduces motion and external control

V1 Baseline is always the launch point for V2.
V1 Advanced is an educational overlay and is not a dependency.

---

## Baseline Rules
- Do not rename files
- Do not partially copy files
- Replace entire files only
- Maintain pin assignments

---

## Licensing
This project is released under a **custom license**.

- Open for learning, modification, and experimentation
- Commercial use is reserved by the author
- Monetisation applies to V2+ "dont worry wont break the bank"

See: LICENSE_T1_ENZO_v1.md
