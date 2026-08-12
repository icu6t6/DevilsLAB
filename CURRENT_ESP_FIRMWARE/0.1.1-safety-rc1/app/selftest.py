"""
ENZO v1 — Self-Test Module

Purpose:
- Prove wiring correctness
- Catch missing / miswired peripherals
- Provide a single PASS / FAIL result

Run manually:
>>> import app.selftest as st
>>> st.run()
"""

from machine import Pin
import time

from app import pins
from app import imu
import app.status as status


def _print(ok, msg):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {msg}")
    return ok


def test_led(cfg, blink_ms=150):
    try:
        p = Pin(cfg["pin"], Pin.OUT)
        p.value(1)
        time.sleep_ms(blink_ms)
        p.value(0)
        return _print(True, cfg["desc"])
    except Exception as e:
        return _print(False, f"{cfg['desc']} ({e})")


def test_button(cfg):
    try:
        p = Pin(cfg["pin"], Pin.IN, Pin.PULL_UP)
        v = p.value()
        ok = v in (0, 1)
        return _print(ok, cfg["desc"])
    except Exception as e:
        return _print(False, f"{cfg['desc']} ({e})")


def test_pir(cfg):
    try:
        p = Pin(cfg["pin"], Pin.IN)
        v = p.value()
        ok = v in (0, 1)
        return _print(ok, cfg["desc"])
    except Exception as e:
        return _print(False, f"{cfg['desc']} ({e})")


def test_adc(cfg):
    try:
        adc = pins.make_adc(cfg)
        v = adc.read()
        ok = 0 <= v <= 4095
        return _print(ok, f"{cfg['desc']} (adc={v})")
    except Exception as e:
        return _print(False, f"{cfg['desc']} ({e})")


def test_imu():
    ok, err = imu.boot_check()

    s = status.state
    st = s.get("selftest", {})
    if not isinstance(st, dict):
        st = {}

    st["imu"] = {
        "ok": bool(ok),
        "err": str(err or ""),
    }
    s["selftest"] = st
    s["imu_ok"] = bool(ok)
    s["imu_err"] = str(err or "")

    if ok:
        print("[PASS] IMU HW123/MPU6050")
    else:
        print("[INFO] IMU self-test non-fatal:", err)

    return True


def test_motor_driver():
    """Required boot-gate check: both motor channels must accept STOP."""
    try:
        from app import drive_i2c as drive
        drive.init()
        return _print(True, "Motor driver 0x14 (both STOP writes accepted)")
    except Exception as e:
        return _print(False, "Motor driver 0x14 (%s)" % (e,))


def run():
    print("\n=== ENZO v1 SELF-TEST ===")
    results = []

    results.append(test_led(pins.LED_HEARTBEAT))
    results.append(test_led(pins.LED_WIFI))
    results.append(test_motor_driver())

    results.append(test_button(pins.BTN_EYES))
    results.append(test_button(pins.BTN_WIFI))
    results.append(test_pir(pins.PIR))
    results.append(test_adc(pins.LDR))

    # Non-fatal IMU observer check
    results.append(test_imu())

    passed = all(results)

    print("------------------------")
    if passed:
        print("SELF-TEST RESULT: PASS ✅")
    else:
        print("SELF-TEST RESULT: FAIL ❌")

    return passed

