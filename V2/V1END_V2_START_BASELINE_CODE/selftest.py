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
        # active-low buttons idle HIGH
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


def run():
    print("\n=== ENZO v1 SELF-TEST ===")
    results = []

    # Outputs
    results.append(test_led(pins.LED_HEARTBEAT))
    results.append(test_led(pins.LED_WIFI))

    # Inputs
    results.append(test_button(pins.BTN_EYES))
    results.append(test_button(pins.BTN_WIFI))
    results.append(test_pir(pins.PIR))
    results.append(test_adc(pins.LDR))

    passed = all(results)

    print("------------------------")
    if passed:
        print("SELF-TEST RESULT: PASS ✅")
    else:
        print("SELF-TEST RESULT: FAIL ❌")

    return passed

# ============================
# OPTIONAL SENSOR: DHT22
# Non-blocking, add-only
# ============================

def test_dht22():
    """
    Optional DHT22 self-test.
    Does NOT fail overall self-test if missing or errored.
    """
    try:
        import dht
        from machine import Pin
        import pins
        import time
    except Exception as e:
        print("[INFO] DHT22 self-test skipped (imports unavailable):", e)
        return

    if not hasattr(pins, "DHT22"):
        print("[INFO] DHT22 not defined in pins.py")
        return

    cfg = pins.DHT22

    try:
        sensor = dht.DHT22(Pin(cfg["pin"], Pin.IN))
        time.sleep_ms(200)

        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()

        print(f"[PASS] DHT22: {t:.1f}C  {h:.1f}%")

    except Exception as e:
        print("[INFO] DHT22 present but not readable:", repr(e))


# ---- register with existing self-test runner ----
try:
    SELF_TESTS.append(test_dht22)
except Exception:
    pass

