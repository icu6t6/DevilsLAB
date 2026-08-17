"""
ENZO v1 — Pin Truth Map (CANON)

If a pin is not defined here, it does not exist.
All firmware must import from this file.
"""

from machine import Pin, ADC

# ============================
# INPUTS
# ============================
# ============================
# OPTIONAL SENSORS (ADD-ONLY)
# ============================

DHT22 = {
    "pin": 15,
    "desc": "DHT22 temperature/humidity sensor (data)",
}

# Buttons (active-low, internal pull-ups)
BTN_EYES = {
    "pin": 4,
    "mode": Pin.IN,
    "pull": Pin.PULL_UP,
    "active_low": True,
    "desc": "Eye mode cycle button",
}

BTN_WIFI = {
    "pin": 5,
    "mode": Pin.IN,
    "pull": Pin.PULL_UP,
    "active_low": True,
    "desc": "WiFi toggle button",
}

# PIR motion sensor
PIR = {
    "pin": 14,
    "mode": Pin.IN,
    "pull": Pin.PULL_DOWN,
    "desc": "PIR motion sensor output",
}

# LDR (ADC via resistor divider)
LDR = {
    "pin": 7,
    "adc": True,
    "atten": ADC.ATTN_11DB,   # full range ~0–3.3V
    "desc": "LDR light sensor (ADC)",
}

# ============================
# OUTPUTS
# ============================

# Heartbeat / status LED
LED_HEARTBEAT = {
    "pin": 2,
    "mode": Pin.OUT,
    "active_high": True,
    "desc": "Heartbeat LED",
}

# WiFi indicator LED
LED_WIFI = {
    "pin": 12,
    "mode": Pin.OUT,
    "active_high": True,
    "desc": "WiFi status LED",
}

# NeoPixel eyes bar
EYES = {
    "pin": 16,
    "pixels": 8,
    "desc": "8-LED NeoPixel eye bar",
}

# ============================
# SAFE / CONTROL
# ============================

SAFE = {
    "pin": -1,   # -1 = not wired in v1
    "desc": "Optional SAFE pin (hold at reset)",
}

# ============================
# HELPERS
# ============================

def make_pin(cfg):
    """Instantiate a digital Pin from a config dict."""
    return Pin(cfg["pin"], cfg["mode"], cfg.get("pull", None))


def make_adc(cfg):
    """Instantiate an ADC from a config dict."""
    adc = ADC(Pin(cfg["pin"]))
    try:
        adc.atten(cfg.get("atten", ADC.ATTN_11DB))
    except Exception:
        pass
    return adc


