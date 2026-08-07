# Lesson — Phase 3: Mobile Manual Locomotion (V2)

## Lesson Position

Phase 3 moves the external control path from PC USB serial to ENZO's own Wi-Fi access point and HTTP server.

It is still a **temporary bring-up runtime**. The permanent V1 runtime is integrated with mobile control in Phase 4.

---

## Lesson Goal

By the end of this lesson:

- ENZO creates its own Wi-Fi access point
- a phone can connect directly to ENZO
- ENZO serves the control dashboard from the ESP
- W / A / S / D / X commands arrive over HTTP
- the ESP still enforces the motor deadman

No internet connection is required.

---

## Prerequisites

You must have:

- completed V1
- completed Phase 1 and proven the motor driver / I²C path

Phase 2 is **recommended for the learning path** because it demonstrates the same external-command idea over USB serial first, but Phase 3 does not require the Phase 2 PC controller in order to function.

If your motor driver has not been proven in Phase 1, stop here and fix that first.

---

## Files Used in This Lesson

### Working ESP bring-up runtime

[`Phase-3_AP_HOST_main.py`](Phase-3_AP_HOST_main.py)

This file:

- runs ENZO as Wi-Fi access point `ENZO_HOST`
- hosts the working mobile control page
- receives `/cmd?c=...` requests over HTTP
- drives the motor controller using the proven V2 motor commands
- repeats movement only while commands continue arriving
- enforces a **250 ms deadman** on the ESP

For this lesson it is copied to the ESP root **as `/main.py`**.

### Optional UI proof artefact

[`PH3_UI_HTML_EXPORT/enzo.host.html`](PH3_UI_HTML_EXPORT/enzo.host.html)

This standalone HTML file is a **dashboard/layout proof only**.

It displays W / A / S / D / STOP controls and logs button presses locally in the browser, but the current file does **not** send commands to ENZO over HTTP. It is not an alternative control path.

The actual working dashboard is embedded inside `Phase-3_AP_HOST_main.py` and is served directly by ENZO.

---

## Step 1 — Install the temporary Phase 3 runtime

1. Open [`Phase-3_AP_HOST_main.py`](Phase-3_AP_HOST_main.py) in Thonny.
2. Save it to the ESP root as exactly:

```text
/main.py
```

3. Reset ENZO.
4. Watch the serial output.

You should see ENZO report that its access point is up and show an IP address, normally:

```text
192.168.4.1
```

The Phase 3 file temporarily replaces the normal V1 `main.py`. That is intentional for this bring-up stage.

---

## Step 2 — Connect the phone to ENZO

On the phone:

1. Open Wi-Fi settings.
2. Connect to:

```text
ENZO_HOST
```

3. Use the password defined in the Phase 3 runtime:

```text
enzo1234
```

4. Ignore any **No internet** warning.

ENZO is acting as the local network and web server. Internet access is not required.

---

## Step 3 — Open the working dashboard

With the phone connected to `ENZO_HOST`, open a browser and go to:

```text
http://192.168.4.1
```

If the ESP printed a different AP address, use the address it printed instead.

The page you see is being served directly by ENZO from the HTML embedded in [`Phase-3_AP_HOST_main.py`](Phase-3_AP_HOST_main.py).

There is no separate HTML file to install on the phone for the working control path.

---

## Step 4 — Drive ENZO

Keep ENZO lifted for the first test.

- hold **W** → forward
- hold **S** → reverse
- hold **A** → pivot left
- hold **D** → pivot right
- release a movement control → STOP
- press **STOP** → STOP

The hosted dashboard resends an active movement command every **120 ms**.

The ESP deadman is **250 ms**. If valid commands stop arriving, the ESP commands STOP even if the browser fails to send a final `X`.

This is deliberate: motor safety remains on the receiver.

---

## Step 5 — Prove the deadman

With ENZO still lifted:

1. Hold a movement control and confirm the expected movement.
2. Release it and confirm immediate STOP.
3. Start movement again, then deliberately break the control path — for example close/kill the page or disconnect the phone from ENZO Wi-Fi.
4. Confirm the motors stop when command refresh disappears.

Do not continue if ENZO can continue driving after control is lost.

---

## What Phase 3 Teaches

Compare the control paths:

```text
Phase 2:
PC keyboard → USB serial → ESP → motor driver

Phase 3:
Phone browser → HTTP over ENZO Wi-Fi → ESP → motor driver
```

The transport changed. The principle did not:

- external input requests movement
- the ESP decides what motor command is applied
- the ESP enforces STOP when commands disappear

Phase 4 keeps that model but integrates it into the permanent V1 behaviour loop instead of replacing `main.py` with a drive-only bring-up runtime.

---

## Leaving Phase 3

The Phase 3 `main.py` is temporary.

Resetting ENZO while it is still installed simply runs Phase 3 again.

Before returning to normal V1 operation, restore the permanent V1 root runtime from:

[`../V1END_V2_START_BASELINE_CODE/main.py`](../V1END_V2_START_BASELINE_CODE/main.py)

Phase 4 also starts from that permanent V1 runtime model and integrates mobile control through application modules instead of replacing `main.py`.

---

## Lesson Complete When

- [ ] ENZO creates `ENZO_HOST`
- [ ] Phone connects directly to ENZO
- [ ] `http://192.168.4.1` loads the hosted dashboard
- [ ] W / A / S / D work as expected
- [ ] releasing control stops movement
- [ ] command loss triggers the ESP deadman STOP
- [ ] you understand that the standalone HTML export is a UI proof, not the working transport

When these are true, Phase 3 is complete.
