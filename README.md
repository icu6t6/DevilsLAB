![ENZO V1 overview](enzo_v1_overview_800.jpg)

# ENZO — T1 V1 Free Baseline

ENZO is a structured embedded systems reference project built around a known-good ESP32 baseline.

This repository is the **free V1 baseline**.

It is designed to help builders move from:
"copying small examples"
to
"understanding and building a complete, disciplined system."

This is not a kit.  
This is not a loose pile of example files.  
This is a guided baseline.

---

## What this repository is

T1 ENZO V1 Free is the public baseline for ENZO.

It provides:
- a known-good firmware baseline
- trusted pin truth
- reference wiring logic
- educational structure
- a stable launch point for later tiers

It is intended to be:
- stable
- repeatable
- teachable
- expandable without guesswork

---

## What this repository is not

This repository is **not**:
- a full robot kit
- a chassis pack
- a motor system
- a battery pack
- a Pi-side AI build
- a random collection of experiments

If you want the public starting point, this is it.
If you want the deeper machine, that comes later.

---

## Start here

If you are new to ENZO, start here:

👉 [README Start Here](docs/README_START_HERE_T1_ENZO_v1-2.md)

Recommended order:
1. Start Here
2. Overview
3. Bill of Materials
4. Build Guide
5. Wiring Reference
6. Software Setup
7. Completion check

Do not jump around randomly.  
This baseline is designed to be followed in order.

---

## Version map

### V1 Free
The repository you are in now.

Known-good baseline:
- firmware
- wiring truth
- pin truth
- minimal stable behaviour

### V1 Advanced
Optional diagnostics and validation layer.

Used to:
- verify behaviour step-by-step
- expose state
- validate the build properly

V1 Advanced is **not required** for V1.

👉 https://devilslab.gumroad.com/l/qposal

### V2
Locomotion and external control layer.

### V3
Management and observability layer.

### T2
Advanced internal Pi-side ENZO continuation layer.  
Not part of this public baseline.

---

## Looking for smaller ESP32 circuits?

If you want a lighter entry path first, use **ENZO-Labs**.

ENZO-Labs is separate from the main ENZO baseline and is used for:
- smaller circuits
- short buildable modules
- step-by-step learning progression
- confidence-building before bigger systems

👉 [ENZO-Labs branch](https://github.com/icu6t6/DevilsLAB/tree/Enzo-Labs)

---

## Why clone this?

Clone this repository if you want:
- a serious ESP32 baseline instead of random examples
- a structured learning path
- a known-good reference to build from
- a stable launch point for V1 Advanced and later ENZO tiers

If you only want to inspect the project, reading online is fine.
If you want to build properly, clone it and work through it in order.

---

## Rules

- Do not add OLED, DHT, telemetry, or diagnostics to V1 Free
- Do not casually rewrite the baseline
- Changes only happen through deliberate new baseline versions
- This baseline is the reference point other tiers derive from

If you want diagnostics, use V1 Advanced.  
If you want experiments, keep them out of baseline truth.

---

## Who this is for

You should already be comfortable with:
- basic ESP32 / Arduino workflow
- uploading firmware
- editing code
- basic electronics concepts

You do **not** need to be an expert.

But this repository is meant to teach proper system thinking, not just quick copy-paste results.

---

## Main idea

ENZO V1 is serious about:
- being right
- being understandable
- being stable
- teaching disciplined building

That is the point of the baseline.

---

## Next step

If you want the main baseline:

👉 [Start Here](docs/README_START_HERE_T1_ENZO_v1-2.md)

If you want the optional diagnostics/validation layer after V1:

👉 https://devilslab.gumroad.com/l/qposal

If you want smaller public learning circuits first:

👉 [ENZO-Labs branch](https://github.com/icu6t6/DevilsLAB/tree/Enzo-Labs)
