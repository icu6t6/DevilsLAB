# main.py (root)
import time
from machine import Pin, reset_cause
from app.config import PROJECT, SAFE_PIN

FW_VERSION = "0.1.0"

def in_safe_mode():
    # Hold BOOT (GPIO0) while resetting to prevent running the app
    if SAFE_PIN < 0:
        return False
    try:
        p = Pin(SAFE_PIN, Pin.IN, Pin.PULL_UP)
        return p.value() == 0
    except Exception:
        return False

print("\n=== ESP32_3S Bot Controller ===")
print("project=", PROJECT, "ver=", FW_VERSION, "reset_cause=", reset_cause())

if in_safe_mode():
    print("SAFE MODE: skipping app startup.")
else:
    print("starting application...")
    try:
        from app.tasks import run
        run()
    except Exception as e:
        print("APP CRASH:", repr(e))
        time.sleep(1)
