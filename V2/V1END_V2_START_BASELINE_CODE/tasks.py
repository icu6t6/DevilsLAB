# app/tasks.py
from machine import Pin, ADC
import time

import app.status as status
from app import eyes_8led as eyes
import app.leds as leds
import app.net as net
from app.config import WIFI_SSID, WIFI_PASS

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
# Most PIR modules already have a pull resistor onboard.
# If it's noisy, you can try Pin.PULL_DOWN here.
pir = Pin(PIR_PIN, Pin.IN, Pin.PULL_DOWN)

# LDR ADC setup (optional)
ldr = None
try:
    ldr = ADC(Pin(LDR_PIN))
    # 11dB gives widest range on ESP32 (approx 0-3.3V)
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
DEBOUNCE_MS       = 250
MOTION_HOLD_MS    = 4000     # how long to stay "alert" after motion
PIR_IGNORE_MS     = 15000    # ignore PIR for first 15s after boot (warmup)
BTN_OVERRIDE_MS   = 8000     # after pressing eye button, PIR won't override for 8s

ALIVE_EVERY_MS    = 1000

# Eye modes to cycle with the eye button
MODES = ["idle", "blink", "solid", "off", "angry", "happy"]

def run():
    print("tasks.run() starting")

    # ----------------------------
    # Init modules
    # ----------------------------
    try:
        leds.init()
    except Exception as e:
        print("leds.init fail:", e)

    try:
        eyes.init()
        # fancy boot animation (blocking, ~ couple seconds)
        try:
            eyes.startup_show()
        except Exception as e:
            print("eyes.startup_show fail:", e)
        # start in idle, DIM (you wanted level=2 vibe)
        eyes.set_mode("idle", level=1)
        print("EYE MODE: idle")
    except Exception as e:
        print("eyes.init/set fail:", e)

    # ----------------------------
    # State
    # ----------------------------
    start_ms = time.ticks_ms()
    last_print_ms = 0

    # Buttons debounce
    last_press_ms = time.ticks_ms()
    last_eyes = 1
    last_wifi = 1
    wifi_on = False

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

    while True:
        now_ms = time.ticks_ms()

        # LDR -> squint cap (runs in all modes; keeps eyes comfy in bright light)
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
                # Don't crash the whole app if ADC glitches
                print("[tasks] LDR read error:", e)
        uptime = time.ticks_diff(now_ms, start_ms)

        status.state["uptime"] = uptime
        status.state["loop_count"] = status.state.get("loop_count", 0) + 1

        # ----------------------------
        # Heartbeat LED (independent)
        # ----------------------------
        try:
            leds.heartbeat()
        except Exception as e:
            # don't spam prints
            pass

        # ----------------------------
        # Eye animation tick (ALWAYS OK)
        # ----------------------------
        try:
            eyes.tick()
        except Exception:
            pass

        # ----------------------------
        # Eye button: cycle modes (EVENT-BASED)
        # ----------------------------
        eyes_v = eyes_btn.value()
        if eyes_v == 0 and last_eyes == 1:
            # rising edge of press (active-low)
            if time.ticks_diff(now_ms, last_press_ms) > DEBOUNCE_MS:
                last_press_ms = now_ms

                mode_i = (mode_i + 1) % len(MODES)
                current_mode_i = mode_i

                try:
                    eyes.set_mode(MODES[current_mode_i], level=1)
                    print("EYE MODE:", MODES[current_mode_i])
                except Exception as e:
                    print("EYE MODE SET FAIL:", e)

                # prevent PIR from overriding right after a button press
                user_override_until = time.ticks_add(now_ms, BTN_OVERRIDE_MS)

        last_eyes = eyes_v

        # ----------------------------
        # WiFi button (optional, safe)
        # ----------------------------
        wifi_v = wifi_btn.value()
        if wifi_v == 0 and last_wifi == 1:
            if time.ticks_diff(now_ms, last_press_ms) > DEBOUNCE_MS:
                last_press_ms = now_ms
                try:
                    # if your net.py has toggle/start/stop, adjust here
                    print("WIFI BTN")

                    if not wifi_on:
                        net.connect(WIFI_SSID, WIFI_PASS)
                        wifi_on = True
                        wifi_led.value(1)
                        print("WIFI: ON")
                    else:
                        net.off()
                        wifi_on = False
                        wifi_led.value(0)
                        print("WIFI: OFF")

                except Exception as e:
                    print("WIFI action fail:", e)

        last_wifi = wifi_v

        # ----------------------------
        # PIR motion -> temporary "alert" (EVENT-BASED)
        # ----------------------------
        # Ignore PIR while warming up
        if uptime > PIR_IGNORE_MS:
            # Also ignore PIR if user just pressed button recently
            if user_override_until == 0 or time.ticks_diff(now_ms, user_override_until) >= 0:

                pir_v = pir.value()

                # Detect motion START (0 -> 1)
                if pir_v == 1 and last_pir == 0:
                    motion_until = time.ticks_add(now_ms, MOTION_HOLD_MS)

                    # remember what mode we were in, so we can restore it
                    prev_mode_i = current_mode_i

                    try:
                        eyes.set_mode("solid", level=1)  # "alert look"
                        print("MOTION!")
                    except Exception as e:
                        print("MOTION SET FAIL:", e)

                last_pir = pir_v

        # Restore previous mode when motion hold expires
        if motion_until and time.ticks_diff(now_ms, motion_until) >= 0:
            motion_until = 0
            try:
                current_mode_i = prev_mode_i
                eyes.set_mode(MODES[current_mode_i], level=1)
                print("MOTION END ->", MODES[current_mode_i])
            except Exception as e:
                print("MOTION END SET FAIL:", e)

        # ----------------------------
        # Once per second "ALIVE"
        # ----------------------------
        if time.ticks_diff(uptime, last_print_ms) >= ALIVE_EVERY_MS:
            print("ALIVE", uptime, status.state["loop_count"])
            last_print_ms = uptime

        time.sleep_ms(10)



