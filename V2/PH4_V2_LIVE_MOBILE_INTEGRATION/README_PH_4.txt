ENZO V2 — PH4 Integrated Mobile Control (Files)

What this package contains:
- app/drive_i2c.py
  Motor authority + deadman safety (STOP on silence).
- app/control_ap_http.py
  Wi-Fi AP + tiny HTTP server + embedded mobile UI.
- app/tasks.py
  Your tasks loop with PH4 integrated (init + tick calls).

How to install (Thonny):
1) Copy app/drive_i2c.py to the ESP at: /app/drive_i2c.py
2) Copy app/control_ap_http.py to the ESP at: /app/control_ap_http.py
3) Replace /app/tasks.py with the provided one.

How to use:
- Power ENZO normally. V1 features continue to run.
- On phone: Wi-Fi -> connect to ENZO_HOST (password: enzo1234)
- Open browser: http://192.168.4.1
- Hold buttons to move; release -> STOP.
