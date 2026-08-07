# app/leds.py
from machine import Pin
import time

# CHANGE THIS if your heartbeat LED is on a different pin
HB_PIN = 2

_led = None
_last_ms = 0
_state = 0

def init():
    global _led
    if _led is None:
        _led = Pin(HB_PIN, Pin.OUT)
        _led.value(0)

def heartbeat(period_ms=1000):
    """
    Simple non-blocking heartbeat blink.
    Does not depend on eyes/PIR/buttons.
    """
    global _last_ms, _state
    if _led is None:
        init()

    now = time.ticks_ms()
    if _last_ms == 0:
        _last_ms = now

    # toggle twice per period (on/off)
    if time.ticks_diff(now, _last_ms) >= (period_ms // 2):
        _last_ms = now
        _state ^= 1
        _led.value(_state)


