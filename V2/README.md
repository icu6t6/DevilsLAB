# ENZO V2 — START HERE

## What this is

ENZO V2 builds on the locked V1 baseline to add locomotion plus external control paths while preserving the working V1 behaviour model.

V2 is structured as four phases.

- Phases **1–3 are instructional bring-up stages**.
- Phases **2 and 3 temporarily replace the ESP root `main.py`**.
- Phase **4 returns to the permanent V1 `main.py` and integrates mobile control into the existing V1 application loop**.

This page is the map. The phase documents contain the working instructions.

---

## Prerequisites

Before V2, complete the public V1 baseline.

You should have:

- working V1 firmware
- ESP32-S3 running MicroPython
- working V1 sensors / buttons / eyes / heartbeat
- robot power architecture completed and verified
- motor driver wired to the robot power system
- PC with USB serial access
- smartphone with Wi-Fi

V1 Advanced is optional and is not a dependency for V2.

---

## Choose your route

### Option A — Learn it step by step (recommended)

Follow:

**Phase 1 → Phase 2 → Phase 3 → Phase 4**

Each phase proves one new layer before the next layer is added.

### Option B — Use the complete baseline snapshots

V2 also includes two complete snapshots:

- [V1 end / V2 start baseline](V1END_V2_START_BASELINE_CODE/)
- [V2 completed baseline](V2_END_BASELINE_CODE/)

The first snapshot is the working V1 runtime at the exact point V2 begins.

The second snapshot is the completed integrated V2 runtime.

Option B is useful for comparison, recovery, or moving directly to the known-good V2 end state. It skips the staged learning and troubleshooting path through Phases 1–4.

### Installing a full baseline snapshot on the ESP

The snapshot folders are source packages. On the ESP:

- `main.py` belongs at the device root as `/main.py`
- application modules such as `config.py`, `tasks.py`, `eyes_8led.py`, `drive_i2c.py` and `control_ap_http.py` belong inside `/app/`
- the empty `actuators/__init__.py` package is intentionally retained as part of the baseline structure

Do not place every snapshot file at the ESP root.

---

## Phase 1 — Group D: locomotion proof

**Goal:** prove the motor driver and I²C motor-control path before adding any external controller.

Start here:

[Phase 1 — Module Group D lesson](PH1_GROUP_D_LOCOMOTION/MODULE_GROUP_D_V2_LOCOMOTION.md)

The one-shot proof script is:

[Phase 1 motor proof script](PH1_GROUP_D_LOCOMOTION/motor_proof.py)

Phase 1 is a manual validation tool only. It does not replace the permanent V1 runtime.

When the motor driver and both tracks behave correctly, continue to Phase 2.

---

## Phase 2 — Group E: PC USB serial control

**Goal:** prove external manual control over USB while the ESP remains responsible for motor commands and command-loss STOP.

Start here:

[Phase 2 — Module Group E lesson](PH2_GROUP_E_PC_USB_SERIAL/MODULE_GROUP_E.md)

Working files:

- [PC keyboard sender](PH2_GROUP_E_PC_USB_SERIAL/keyboard_to_serial.py)
- [temporary ESP Phase 2 `main.py`](PH2_GROUP_E_PC_USB_SERIAL/main.py)

Phase 2 temporarily replaces the root `/main.py`.

The lesson explains how to install it, how the **120 ms sender refresh / 250 ms ESP deadman** pair works, how to correct forward/reverse mapping if required, and how to restore the permanent V1 `main.py` when the lesson is finished.

---

## Phase 3 — Mobile AP + HTTP bring-up

**Goal:** replace the PC USB transport with phone control over ENZO's own Wi-Fi access point and HTTP server.

Start here:

[Phase 3 — Mobile manual control lesson](PH3_AP_HTTP_RECEIVER/LESSON_PHASE_3_MOBILE_MANUAL_CONTROL_V2.md)

Working ESP bring-up runtime:

[Phase 3 AP / HTTP `main.py`](PH3_AP_HTTP_RECEIVER/Phase-3_AP_HOST_main.py)

Phase 3 also temporarily replaces the root `/main.py`.

The working dashboard is embedded inside that ESP file and served by ENZO at its AP address, normally:

```text
http://192.168.4.1
```

The separate file below is retained only as an optional UI/layout proof:

[Standalone Phase 3 HTML UI proof](PH3_AP_HTTP_RECEIVER/PH3_UI_HTML_EXPORT/enzo.host.html)

That standalone HTML file does **not** currently send HTTP commands to ENZO and is not the working control path.

---

## Phase 4 — Live mobile integration (final V2 stage)

**Goal:** return to the permanent V1 runtime and add mobile driving without replacing the V1 behaviour loop.

Start here:

[Phase 4 — Integration instructions](PH4_V2_LIVE_MOBILE_INTEGRATION/README_PH_4.txt)

Files added / replaced inside `/app`:

- [drive_i2c.py](PH4_V2_LIVE_MOBILE_INTEGRATION/drive_i2c.py) — motor authority + deadman
- [control_ap_http.py](PH4_V2_LIVE_MOBILE_INTEGRATION/control_ap_http.py) — non-blocking AP / HTTP adapter + hosted dashboard
- [tasks.py](PH4_V2_LIVE_MOBILE_INTEGRATION/tasks.py) — V1 tasks loop with PH4 services integrated

**Do not use the temporary Phase 2 or Phase 3 `main.py` in Phase 4.**

Phase 4 uses the permanent V1 root runtime again:

[V1 permanent `main.py`](V1END_V2_START_BASELINE_CODE/main.py)

That permanent `main.py` still starts `app.tasks.run()`. The V2 capability is integrated through the Phase 4 application modules.

---

## Understanding `main.py` in V2

There are two different roles that happen to use the filename `main.py`:

- **Permanent V1/V2 root `main.py`** — starts the normal ENZO application via `app.tasks.run()`
- **Temporary Phase 2 / Phase 3 lesson `main.py`** — replaces the permanent runtime only for a bring-up exercise

A reset does **not** magically restore the permanent runtime. If a temporary lesson `main.py` is installed, resetting simply runs that temporary file again.

Restore the permanent V1 `main.py` explicitly before returning to normal V1 operation or starting Phase 4.

---

## V2 completion state

V2 is complete when:

- the permanent V1 behaviour loop still runs
- the motor driver is integrated
- ENZO creates `ENZO_HOST`
- the hosted dashboard loads from the ESP
- W / A / S / D movement works
- release / STOP works
- command loss triggers the ESP deadman STOP
- V1 eyes / heartbeat / PIR / LDR / buttons continue to operate alongside mobile control

The complete final reference is here:

[V2 end baseline](V2_END_BASELINE_CODE/)
