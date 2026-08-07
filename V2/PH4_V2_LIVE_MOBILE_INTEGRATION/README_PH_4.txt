ENZO V2 — PH4 Integrated Mobile Control

PH4 is the point where the temporary bring-up runtimes stop.

The permanent V1 root main.py is used again. Mobile driving is added inside the existing V1 application structure so the normal V1 behaviours continue to run.

SOURCE FILES IN THIS PH4 FOLDER

- drive_i2c.py
  https://github.com/icu6t6/DevilsLAB/blob/main/V2/PH4_V2_LIVE_MOBILE_INTEGRATION/drive_i2c.py
  Motor authority + 250 ms deadman safety.

- control_ap_http.py
  https://github.com/icu6t6/DevilsLAB/blob/main/V2/PH4_V2_LIVE_MOBILE_INTEGRATION/control_ap_http.py
  ENZO Wi-Fi AP + non-blocking HTTP receiver + embedded mobile dashboard.

- tasks.py
  https://github.com/icu6t6/DevilsLAB/blob/main/V2/PH4_V2_LIVE_MOBILE_INTEGRATION/tasks.py
  V1 tasks loop with PH4 init/tick calls integrated.

IMPORTANT — RESTORE THE PERMANENT MAIN.PY FIRST

If you completed Phase 2 or Phase 3, the ESP may still have a temporary lesson main.py at its root.

Before installing PH4, restore the permanent V1 main.py from:

https://github.com/icu6t6/DevilsLAB/blob/main/V2/V1END_V2_START_BASELINE_CODE/main.py

Save that file to the ESP as:

/main.py

Do not use the Phase 2 or Phase 3 temporary main.py for PH4.

INSTALL PH4 FILES WITH THONNY

1) Copy drive_i2c.py to the ESP at:

/app/drive_i2c.py

2) Copy control_ap_http.py to the ESP at:

/app/control_ap_http.py

3) Replace the existing V1 tasks.py with the PH4 tasks.py at:

/app/tasks.py

4) Leave the rest of the V1 runtime in place.

5) Reset ENZO.

WHAT SHOULD HAPPEN

The permanent root main.py starts app.tasks.run() exactly as V1 did.

The PH4 tasks.py then:

- starts the normal V1 LEDs / eyes / PIR / LDR / button behaviour
- initialises the motor service
- starts ENZO_HOST and the HTTP server
- calls the HTTP and deadman tick functions inside the existing V1 loop

You should see output including:

[PH4] Integrated mobile control READY

HOW TO USE MOBILE CONTROL

1) On the phone, connect Wi-Fi to:

ENZO_HOST

Password:

enzo1234

2) Open a browser at:

http://192.168.4.1

3) Hold W / A / S / D to drive.

4) Release a movement control to STOP.

5) Use the STOP control whenever required.

SAFETY MODEL

The browser refreshes an active movement command every 120 ms.

The ESP motor service uses a 250 ms deadman. If valid commands disappear, drive_i2c.py commands STOP.

Motor authority therefore remains on the ESP rather than in the browser.

PH4 FIRST TEST

Keep ENZO lifted off the ground for the first test.

Confirm:

- normal V1 eye behaviour still runs
- heartbeat still runs
- PIR / LDR / buttons still behave normally
- ENZO_HOST appears
- the dashboard loads
- W / A / S / D move the expected tracks
- release stops movement
- losing the control connection triggers STOP

PH4 IS COMPLETE WHEN

Mobile control works while the existing V1 behaviour loop continues to operate.

At that point the integrated PH4 runtime is the V2 end state.

For a complete copy of that end state, use:

https://github.com/icu6t6/DevilsLAB/tree/main/V2/V2_END_BASELINE_CODE
