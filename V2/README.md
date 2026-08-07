# ENZO V2 — START HERE

## What this is

ENZO V2 builds on the locked V1 baseline to add multiple external control paths (PC serial and mobile HTTP) while preserving all existing ENZO behaviour.

V2 is structured as four documented phases.
Phases **1–3 are instructional** and may temporarily replace files.
Phase **4 integrates the final capability** without blocking or modifying core behaviour.

This file is a **map**, not a lesson.

---

## Prerequisites

- ENZO V1 baseline firmware (locked)
- Motor driver wired and verified
- ESP32-S3 running MicroPython
- PC with USB serial access
- Smartphone with Wi-Fi

---

## How to use this repository

### Option A — Learn it step by step (recommended)

Follow **Phase 1 → Phase 4** in order.

Each phase folder contains:

- A lesson document
- The exact files used in that phase
- Historical or optional variants where relevant

### Option B — Use the full baseline snapshots

If you do not want to work through each instructional phase, V2 also includes complete baseline snapshots.

Start with:

`V1END_V2_START_BASELINE_CODE/`

and compare or move directly to:

`V2_END_BASELINE_CODE/`

The V2 end baseline contains the completed integrated V2 runtime.

This route gives you the known-good end state, but it skips the staged learning path through Phases 1–4.

That means you will miss some of the reasoning behind:

- motor bring-up
- PC serial control
- mobile/AP/HTTP control
- deadman behaviour
- transport vs motor authority
- troubleshooting each stage

If you want to understand and modify V2 confidently, follow Option A.
If you mainly need the completed V2 baseline, Option B is the quicker route.

This enables mobile driving **without affecting existing ENZO features**.

---

## Phase overview

### Phase 1 — Group D: Locomotion proof

**Goal:** Verify motors and I²C control
**Result:** Confirmed hardware foundation
**Notes:** One-shot test script; not part of runtime

Folder:

```
PH1_GROUP_D_LOCOMOTION/
```

---

### Phase 2 — Group E: PC USB serial control

**Goal:** Drive ENZO from a keyboard over USB
**Result:** Deterministic serial control path
**Notes:** Uses a **temporary** **`main.py`** for the lesson

Folder:

```
PH2_GROUP_E_PC_USB_SERIAL/
```

---

### Phase 3 — Mobile control bring-up (ESP AP + HTTP)

**Goal:** Control ENZO from a phone browser
**Result:** Working Wi-Fi AP + HTTP command receiver
**Notes:** Lesson-only `main.py`; includes optional UI export

Folder:

```
PH3_AP_HTTP_RECEIVER/
```

---

### Phase 4 — V2 live mobile integration (final)

**Goal:** Add mobile driving without blocking ENZO
**Result:** Mobile control runs alongside all V1 features
**Notes:** No `main.py` replacement; integrates via app modules

Folder:

```
PH4_V2_LIVE_MOBILE_INTEGRATION/
```

---

## Understanding `main.py` in V2 (important)

During V2 you will encounter multiple files named `main.py`.
These are **contextual mains**, not a single persistent runtime file.

- **V1** **`main.py`** — ENZO’s permanent runtime
- **Phase lesson** **`main.py`** — temporary, replaced later
- **PC scripts** — not part of ESP runtime

Each phase explicitly states when a file is temporary.

---

## Where you end up

After completing Phase 4, ENZO can be driven from a mobile phone at any time by connecting to its Wi-Fi access point and opening the control interface.

This does **not** disable diagnostics, modes, or existing behaviour.

---

End of map.