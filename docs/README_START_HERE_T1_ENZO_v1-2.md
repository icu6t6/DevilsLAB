# T1-ENZO v1 — Educational ESP32 Firmware & Reference Project

## IMPORTANT — READ FIRST
T1-ENZO v1 is an educational firmware and reference build package.
The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.
Builders may replicate this implementation or substitute their own hardware, provided the electrical and pin-mapping rules are preserved.
This project is **NOT a physical product or kit**.

ENZO V1 Free is complete when the ESP32-S3 sensor/UI assembly works, Module A is complete, the protected battery and 5V power system has passed Module B, the ESP and power system are integrated, and the documented V1 completion checks pass. The photographed tracked chassis is a reference installation and optional mounting context. Locomotion begins in V2.

Use the [canonical V1 firmware](../material/v1/firmware/) and the [Software Setup file layout](SOFTWARE_SETUP_T1_ENZO_v1_USER.md). Do not substitute `CURRENT_ESP_FIRMWARE/` or `V2/` files.

## Acknowledgement
This project was designed and developed by the author, with support from an AI assistant used for analysis, discussion, and continuity during development.

## How to Use This Repository (Read Order)

This repository is structured as a **guided baseline build**, not a loose collection of files.

### Recommended practical order
1. Read this document fully ([README Start Here](README_START_HERE_T1_ENZO_v1-2.md))
2. Review the project overview ([Overview](OVERVIEW_T1_ENZO_v1.md))
3. Review the Bill of Materials ([BOM](BOM_T1_ENZO_v1.md))
4. Complete software setup and flash firmware first ([Software Setup](SOFTWARE_SETUP_T1_ENZO_v1_USER.md))
5. Build and test the ESP stack on USB bench power ([Module Group A — ESP Core Stack](ESP_BUILD_GUIDE_MODULE_GROUP_A.md))
6. Build and verify the robot power system with the ESP disconnected ([Module Group B — Power System](MODULE_GROUP_B_POWER_SYSTEM_FINAL_v2.md))
7. Use the [Wiring Reference](WIRING_REFERENCES_T1_ENZO_v1_COMBINED.md) while integrating the ESP stack with the robot power system
8. Verify behaviour against the Completion Criteria

### Where the full Build Guide fits
The [Build Guide](BUILD_GUIDE_T1_ENZO_v1-2.md) remains useful as an overall project reference, but the practical public V1 path is the staged order above.

### Safety rule during assembly
Do **not** solder, move wires, or change connections while the system is powered.
Disconnect the battery, USB and any external power before making physical wiring changes. The latching button does not disconnect USB power.

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
- Power architecture (source/input rail → regulated 5V logic rail → controller)
- Grounding strategy
- GPIO planning
- Modular firmware structure
- Safe expansion paths
- In v1, the input rail is typically supplied by a 2-cell LiPo battery, but the firmware is power-source-agnostic.

This is **not** a toy demo or copy‑paste project. (Its your choice if you want to write out the code while learning or copy paste is fine.)

T1-ENZO v1 is an educational embedded-systems reference designed to teach real-world power and wiring architecture.
It models how industrial and mobile machines handle raw power: energy enters the system, is protected, regulated, and distributed before reaching logic.
The firmware operates downstream of electrical safety — it never replaces it.

Default power model: 2S battery → protected input/source rail → regulated 5V logic rail → controller & peripherals.
USB power is acceptable for firmware flashing and early bench testing, but the architecture is designed to be battery-powered.

The documentation includes one proven physical implementation (“ENZO”) used to validate the firmware and architecture.

Builders may reproduce the documented electrical baseline. The photographed chassis and layered mounting are reference examples; exact mechanical reproduction is not a V1 completion requirement. The firmware and pin map are ESP32-S3 specific.

Controller support (V1): The ENZO v1 firmware and Pin Truth Map are authored for the Waveshare ESP32-S3 dev board N8R8 and the exact pinout documented in this repository.
If you use any other controller (ESP32-WROOM, Pico, Arduino, etc.), the pin map and wiring instructions will not apply.
Adapting ENZO to a different board is outside v1 scope (V2+ territory) and requires your own remapping and validation.

Substituted parts must preserve the documented electrical functions, pin rules and verified operating limits. A different controller or USB power circuit requires its own validation; the Waveshare board’s USB isolation cannot be assumed for another board.

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
ENZO V1 Free is complete when the ESP32-S3 sensor/UI assembly works, Module A is complete, the protected battery and 5V power system has passed Module B, the ESP and power system are integrated, and the documented V1 completion checks pass. The photographed tracked chassis is a reference installation and optional mounting context. Locomotion begins in V2.

- [ ] Pass the [Module A checks](ESP_BUILD_GUIDE_MODULE_GROUP_A.md#completion-criteria-module-group-a).
- [ ] Pass [Module B](MODULE_GROUP_B_POWER_SYSTEM_FINAL_v2.md) with the ESP disconnected.
- [ ] Complete the [integration and completion checks](WIRING_REFERENCES_T1_ENZO_v1_COMBINED.md#integration-and-v1-completion).
- [ ] Record any substituted hardware and unresolved issue. An unresolved failed check means a partial build, not full completion.

[Building ENZO / show your build](https://github.com/icu6t6/DevilsLAB/issues/new?template=build-report.yml) — a partial build or parts question is welcome.

---

## What Comes After V1

T1-ENZO v1 is a complete baseline. No further steps are required.

From this point, builders may:
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
The [root LICENSE](../LICENSE) contains the custom V1 non-commercial terms and exact file scope. It permits personal and non-commercial educational use, experimentation, modification and sharing with attribution. Commercial use requires prior permission.

The V1 licence does not grant rights to V2, current later-tier firmware, T2 or Lifetime. See the [licence guide](LICENCE_T1_ENZO_V1.md).
