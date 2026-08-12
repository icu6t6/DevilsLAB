# main.py (root)
import time
from machine import Pin, reset_cause
from app.config import PROJECT, SAFE_PIN
import app.status as status

FW_VERSION = "0.1.1-safety-rc1"

RESET_CAUSE = reset_cause()

status.state["project"] = PROJECT
status.state["ver"] = FW_VERSION
status.state["reset_cause"] = RESET_CAUSE

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
print("project=", PROJECT, "ver=", FW_VERSION, "reset_cause=", RESET_CAUSE)

if in_safe_mode():
    print("SAFE MODE: skipping app startup.")
else:
    print("starting application...")
    try:
        from app.tasks import run
        run()
    except Exception as e:
        print("APP CRASH:", repr(e))
        # Defense in depth: tasks.run() already does this in a finally block.
        # Retry here too in case startup failed before that wrapper took over.
        try:
            from app import drive_i2c as emergency_drive
            for _ in range(3):
                if emergency_drive.stop_all():
                    print("[SAFETY] emergency STOP confirmed after app crash")
                    break
                time.sleep_ms(50)
        except Exception as stop_error:
            print("[SAFETY] emergency STOP could not be confirmed:", repr(stop_error))
        time.sleep(1)




