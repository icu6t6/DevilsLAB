# app/tasks.py
from machine import Pin, ADC
import time

import app.status as status
from app import eyes_8led as eyes
import app.leds as leds
from app import selftest as st
from app import imu

# ----------------------------
# Pins / hardware
# ----------------------------

# Buttons (active-low, internal pull-ups)
EYES_BTN_PIN = 4
WIFI_BTN_PIN = 5
eyes_btn = Pin(EYES_BTN_PIN, Pin.IN, Pin.PULL_UP)
wifi_btn = Pin(WIFI_BTN_PIN, Pin.IN, Pin.PULL_UP)

# WiFi indicator LED (active-high)
# Wiring: GPIO12 -> resistor -> LED long leg, LED short leg -> GND
WIFI_LED_PIN = 12
wifi_led = Pin(WIFI_LED_PIN, Pin.OUT)
wifi_led.value(0)

# PIR motion sensor
PIR_PIN = 14

# --- LDR (light sensor) squint ---
# Wire: LDR_PIN is the ADC pin at the junction of LDR + resistor divider.
# Bright light -> LOWER ADC value (0..4095). Dark -> HIGHER.
LDR_PIN = 7
LDR_SAMPLE_MS = 200
# Hysteresis thresholds to stop flicker:
LDR_BRIGHT_ON = 700   # if below this -> start squint
LDR_BRIGHT_OFF = 900  # if above this -> stop squint
SQUINT_CAP_LEVEL = 1  # max brightness level while squinting (0..3)
pir = Pin(PIR_PIN, Pin.IN, Pin.PULL_DOWN)

# LDR ADC setup (optional)
ldr = None
try:
    ldr = ADC(Pin(LDR_PIN))
    try:
        ldr.atten(ADC.ATTN_11DB)
    except Exception:
        pass
except Exception as e:
    print("[tasks] LDR disabled:", e)
    ldr = None

# ----------------------------
# Behaviour tuning
# ----------------------------
DEBOUNCE_MS = 250
MOTION_HOLD_MS = 4000     # how long to stay "alert" after motion
PIR_IGNORE_MS = 15000     # ignore PIR for first 15s after boot (warmup)
BTN_OVERRIDE_MS = 8000    # after pressing eye button, PIR won't override for 8s

ALIVE_EVERY_MS = 1000

# Eye modes to cycle with the eye button
MODES = ["idle", "blink", "solid", "off", "angry", "happy"]


def _force_wifi_off(net_mod):
    """Hard-disable WiFi for SAFE MODE."""
    try:
        wifi_led.value(0)
    except Exception:
        pass
    try:
        if net_mod is not None:
            net_mod.off()
    except Exception:
        pass
    status.state["wifi_on"] = False
    status.state["wifi_enabled"] = False


def _run():
    print("tasks.run() starting")

    # ----------------------------
    # Lazy imports for risky subsystems
    # ----------------------------
    net = None
    ph4_http = None
    ph4_drive = None
    snap = None
    v3 = None
    _V3_AVAILABLE = False

    try:
        import app.net as net
        print("[tasks] net import OK")
    except Exception as e:
        print("[tasks] net import fail:", repr(e))

    try:
        from app import control_ap_http as ph4_http
        print("[tasks] control_ap_http import OK")
    except Exception as e:
        print("[tasks] control_ap_http import fail:", repr(e))

    try:
        from app import drive_i2c as ph4_drive
        print("[tasks] drive_i2c import OK")
    except Exception as e:
        print("[tasks] drive_i2c import fail:", repr(e))

    try:
        import app.snapshot as snap
        print("[tasks] snapshot import OK")
    except Exception as e:
        print("[tasks] snapshot import fail:", repr(e))

    try:
        import app.v3 as v3
        _V3_AVAILABLE = True
        print("[tasks] v3 import OK")
    except Exception as e:
        print("[V3] module missing (continuing without V3):", e)
        _V3_AVAILABLE = False

    # ----------------------------
    # Init modules
    # ----------------------------
    try:
        leds.init()
    except Exception as e:
        print("leds.init fail:", e)

    try:
        imu.init()
        print("[tasks] imu init OK")
    except Exception as e:
        print("[tasks] imu init fail:", e)

    # Eyes init + boot animation (always attempted)
    try:
        eyes.init()
        try:
            eyes.startup_show()
        except Exception as e:
            print("eyes.startup_show fail:", e)
        eyes.set_mode("idle", level=1)
        print("EYE MODE: idle")
    except Exception as e:
        print("eyes.init/set fail:", e)

    # ----------------------------
    # BOOT GATE: self-test (PASS/FAIL)
    # ----------------------------
    boot_ok = True
    try:
        boot_ok = bool(st.run())
    except Exception as e:
        boot_ok = False
        print("[selftest] crash:", repr(e))

    status.state["boot_ok"] = boot_ok

    # SAFE MODE (C):
    # - No motors
    # - No Wi-Fi
    # - Diagnostics keep running
    safe_mode = not boot_ok
    status.state["safe_mode"] = safe_mode

    # T2: record boot gate result for snapshots
    if snap is not None:
        try:
            snap.record_selftest(boot_ok)
        except Exception:
            pass

    if safe_mode:
        print("[SAFE MODE] Self-test FAIL -> MOTORS + WiFi DISABLED")
        try:
            eyes.set_mode("angry", level=1)
        except Exception as e:
            print("[SAFE MODE] eyes.set_mode fail:", e)
        _force_wifi_off(net)
    else:
        status.state["wifi_enabled"] = True

    # ----------------------------
    # PH4 init (AP + HTTP receiver + motor deadman service)
    #   - Disabled in SAFE MODE
    # ----------------------------
    if (not safe_mode) and (ph4_drive is not None) and (ph4_http is not None):
        try:
            ph4_drive.init()
            ph4_http.init()
            print("[PH4] Integrated mobile control READY")
            status.state["ph4_ok"] = True

            if snap is not None:
                try:
                    ap_ip = getattr(ph4_http, "_ip", None)
                    if ap_ip:
                        snap.record_ph4(ap_ip=ap_ip, url=("http://%s" % ap_ip), http_ready=True, ok=True)
                    else:
                        snap.record_ph4(http_ready=True, ok=True)
                except Exception:
                    pass

        except Exception as e:
            print("[PH4] init fail (continuing without PH4):", e)
            try:
                ph4_drive.stop_all()
            except Exception:
                pass
            status.state["ph4_ok"] = False
            if snap is not None:
                try:
                    snap.record_ph4(http_ready=False, ok=False, err=repr(e))
                except Exception:
                    pass
    else:
        status.state["ph4_ok"] = False

    # ----------------------------
    # V3 init (additive, fail-safe)
    #   - Still allowed in SAFE MODE
    # ----------------------------
    if _V3_AVAILABLE and v3 is not None:
        try:
            v3.init()
            print("[V3] manager/observers init OK")
            status.state["v3_ok"] = True
            if snap is not None:
                try:
                    snap.record_v3(ok=True)
                except Exception:
                    pass
        except Exception as e:
            print("[V3] init fail (continuing without V3):", e)
            status.state["v3_ok"] = False
            if snap is not None:
                try:
                    snap.record_v3(ok=False, err=repr(e))
                except Exception:
                    pass
    else:
        status.state["v3_ok"] = False
        if snap is not None:
            try:
                snap.record_v3(ok=False, err="module_missing")
            except Exception:
                pass

    # ----------------------------
    # State
    # ----------------------------
    start_ms = time.ticks_ms()
    last_print_ms = 0

    # Buttons debounce
    last_press_ms = time.ticks_ms()
    last_eyes = 1
    last_wifi = 1

    # Eye mode index / restore
    mode_i = 0
    prev_mode_i = 0
    current_mode_i = 0

    # PIR edge detect + hold
    last_pir = 0
    motion_until = 0

    # When user pressed eye button, PIR must not override until this time
    user_override_until = 0

    # LDR squint state
    ldr_is_bright = False
    next_ldr_ms = time.ticks_ms()

    print("tasks.run() entering loop")

    while True:
        now_ms = time.ticks_ms()

        # ----------------------------
        # PH4 tick (non-blocking)
        #   - Disabled in SAFE MODE
        # ----------------------------
        if (not safe_mode) and (ph4_http is not None) and (ph4_drive is not None):
            try:
                ph4_http.tick()
            except Exception:
                pass

            try:
                ph4_drive.tick()
            except Exception:
                pass

        # ----------------------------
        # V3 tick (non-blocking, fail-safe)
        # ----------------------------
        if _V3_AVAILABLE and v3 is not None:
            try:
                v3.tick(now_ms)
            except Exception:
                pass

        # LDR -> squint cap
        if ldr is not None and time.ticks_diff(now_ms, next_ldr_ms) >= 0:
            next_ldr_ms = time.ticks_add(now_ms, LDR_SAMPLE_MS)
            try:
                raw = ldr.read()
                if not ldr_is_bright and raw <= LDR_BRIGHT_ON:
                    ldr_is_bright = True
                elif ldr_is_bright and raw >= LDR_BRIGHT_OFF:
                    ldr_is_bright = False
                if hasattr(eyes, "set_squint_level"):
                    eyes.set_squint_level(SQUINT_CAP_LEVEL if ldr_is_bright else None)
            except Exception as e:
                print("[tasks] LDR read error:", e)

        # IMU poll (internally rate-limited, no spam)
        try:
            imu.poll(now_ms)
        except Exception:
            pass

        uptime = time.ticks_diff(now_ms, start_ms)

        # Canonical surface update
        status.state["uptime"] = uptime
        status.state["uptime_ms"] = uptime
        status.state["loop_count"] = status.state.get("loop_count", 0) + 1

        # T2: emit structured snapshot
        if snap is not None:
            try:
                snap.emit_if_due(now_ms)
            except Exception:
                pass

        # Heartbeat LED
        try:
            leds.heartbeat()
        except Exception:
            pass

        # Eye animation tick
        try:
            eyes.tick()
        except Exception:
            pass

        # Eye button: cycle modes
        eyes_v = eyes_btn.value()
        if eyes_v == 0 and last_eyes == 1:
            if time.ticks_diff(now_ms, last_press_ms) > DEBOUNCE_MS:
                last_press_ms = now_ms

                mode_i = (mode_i + 1) % len(MODES)
                current_mode_i = mode_i

                try:
                    eyes.set_mode(MODES[current_mode_i], level=1)
                    print("EYE MODE:", MODES[current_mode_i])
                except Exception as e:
                    print("EYE MODE SET FAIL:", e)

                user_override_until = time.ticks_add(now_ms, BTN_OVERRIDE_MS)

        last_eyes = eyes_v

        # WiFi button: V3-managed request (observer/management boundary)
        wifi_v = wifi_btn.value()
        if wifi_v == 0 and last_wifi == 1:
            if time.ticks_diff(now_ms, last_press_ms) > DEBOUNCE_MS:
                last_press_ms = now_ms
                try:
                    if safe_mode:
                        print("WIFI BTN (request) [SAFE MODE: ignored]")
                        status.state["wifi_req_toggle"] = True
                        _force_wifi_off(net)
                    else:
                        print("WIFI BTN (request)")
                        status.state["wifi_req_toggle"] = True
                except Exception as e:
                    print("WIFI request fail:", e)

        last_wifi = wifi_v

        # PIR motion -> temporary "alert"
        if uptime > PIR_IGNORE_MS:
            if user_override_until == 0 or time.ticks_diff(now_ms, user_override_until) >= 0:
                pir_v = pir.value()

                if pir_v == 1 and last_pir == 0:
                    motion_until = time.ticks_add(now_ms, MOTION_HOLD_MS)
                    prev_mode_i = current_mode_i

                    try:
                        eyes.set_mode("solid", level=1)
                        print("MOTION!")
                    except Exception as e:
                        print("MOTION SET FAIL:", e)

                last_pir = pir_v

        if motion_until and time.ticks_diff(now_ms, motion_until) >= 0:
            motion_until = 0
            try:
                current_mode_i = prev_mode_i
                eyes.set_mode(MODES[current_mode_i], level=1)
                print("MOTION END ->", MODES[current_mode_i])
            except Exception as e:
                print("MOTION END SET FAIL:", e)

        # Once per second "ALIVE"
        if time.ticks_diff(uptime, last_print_ms) >= ALIVE_EVERY_MS:
            if safe_mode:
                print("ALIVE", uptime, status.state["loop_count"], "[SAFE MODE]")
            else:
                print("ALIVE", uptime, status.state["loop_count"])
            last_print_ms = uptime

        time.sleep_ms(10)


def _emergency_stop(attempts=3):
    """Best-effort bounded STOP used whenever the application loop exits."""
    try:
        from app import drive_i2c as emergency_drive
    except Exception as e:
        print("[SAFETY] motor module unavailable:", repr(e))
        return False

    for attempt in range(attempts):
        try:
            if emergency_drive.stop_all():
                print("[SAFETY] emergency STOP confirmed")
                return True
        except Exception as e:
            print("[SAFETY] STOP attempt failed:", repr(e))

        if attempt + 1 < attempts:
            time.sleep_ms(50)

    print("[SAFETY] emergency STOP could not be confirmed")
    return False


def run():
    try:
        return _run()
    finally:
        _emergency_stop()

