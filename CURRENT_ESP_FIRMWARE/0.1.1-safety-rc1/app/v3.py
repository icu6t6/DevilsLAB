# app/v3.py
# V3 integrated manager + observers:
# - OLED 5-line status surface (2 Hz) with auto-reinit / fail-soft drawing
# - DHT observer (every 5s)
# - Wi-Fi STA management (request-driven, NON-BLOCKING)
# - Wi-Fi status LED (GPIO12, active-high)
# Must be non-blocking and fail-safe.
#
# IMPORTANT:
# - PH4 owns SoftAP (AP_IF). We do NOT touch AP_IF here.
# - V3 manages STA_IF only, so AP + STA can coexist.

import time
from machine import Pin, I2C

import app.status as status
from app.config import WIFI_SSID, WIFI_PASS

# Optional: DHT
try:
    import dht
except Exception:
    dht = None

# Optional: OLED driver (you already copied app/SSD1306.py)
try:
    from app.SSD1306 import SSD1306_I2C
except Exception:
    SSD1306_I2C = None

# Optional: network (for STA_IF control)
try:
    import network
except Exception:
    network = None


# ---- V3 constants ----
OLED_ADDR = 0x3C
OLED_W = 128
OLED_H = 64

I2C_ID = 0
I2C_SDA = 8
I2C_SCL = 9
I2C_FREQ = 100_000

OLED_PERIOD_MS = 500       # 2 Hz
DHT_PERIOD_MS = 5000       # 0.2 Hz

# OLED/I2C bring-up retry cadence (self-healing)
OLED_RETRY_MS = 2000       # retry init every 2s if missing/failing
OLED_FAIL_REINIT_MS = 2000 # after repeated draw failures, reinit after 2s

DHT_PIN = 15               # matches your canonical mapping

WIFI_TIMEOUT_MS = 15000    # STA connect timeout
WIFI_POLL_MS = 250         # how often we poll STA connection state

# Wi-Fi status LED
WIFI_LED_PIN = 12          # active-high
WIFI_LED_ACTIVE_HIGH = True
WIFI_LED_BLINK_SLOW_MS = 500
WIFI_LED_BLINK_FAST_MS = 150


# ---- Internal state ----
_i2c = None
_i2c_addrs = []

_oled = None
_oled_ready = False
_next_oled_ms = 0
_next_oled_init_ms = 0
_last_oled_err = ""
_oled_fail_count = 0
_next_oled_reinit_ms = 0

_next_dht_ms = 0
_v3_tick = 0

_dht_ok = False
_dht_dev = None

_wifi_state = "OFF"        # OFF / START / POLL / ON / ERR
_wifi_ip = "-"
_wifi_err = ""
_wifi_deadline_ms = 0
_next_wifi_poll_ms = 0

_wlan_sta = None

_wifi_led = None
_wifi_led_on = False
_next_wifi_led_ms = 0


def _set_alert(msg):
    try:
        alerts = status.state.get("alerts", [])
        if msg not in alerts:
            alerts.append(msg)
        status.state["alerts"] = alerts
    except Exception:
        pass


def _wifi_status_str():
    # Display is locked to OFF/START/ON/ERR.
    # Internally we also use POLL.
    if _wifi_state == "POLL":
        return "START"
    return _wifi_state


def _ensure_surface_defaults():
    status.state.setdefault("wifi_state", "OFF")
    status.state.setdefault("wifi_ip", "-")
    status.state.setdefault("wifi_err", "")
    status.state.setdefault("wifi_req_toggle", False)

    status.state.setdefault("dht_ok", False)
    status.state.setdefault("temp_c", None)
    status.state.setdefault("rh", None)

    status.state.setdefault("i2c_addrs", [])
    status.state.setdefault("v3_alive", 0)


def _i2c_init_try():
    global _i2c, _i2c_addrs
    _i2c = I2C(I2C_ID, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=I2C_FREQ)
    time.sleep_ms(50)
    _i2c_addrs = [hex(a) for a in _i2c.scan()]
    status.state["i2c_addrs"] = _i2c_addrs


def _oled_init_try(now_ms):
    global _oled, _oled_ready, _next_oled_ms, _next_oled_init_ms
    global _last_oled_err, _oled_fail_count, _next_oled_reinit_ms

    _oled_ready = False
    _oled = None
    _last_oled_err = ""
    _oled_fail_count = 0
    _next_oled_reinit_ms = 0

    if SSD1306_I2C is None:
        _last_oled_err = "OLED driver missing (app/SSD1306.py)"
        _set_alert(_last_oled_err)
        _next_oled_init_ms = time.ticks_add(now_ms, OLED_RETRY_MS)
        return

    try:
        _i2c_init_try()
        _oled = SSD1306_I2C(OLED_W, OLED_H, _i2c, addr=OLED_ADDR)
        _oled_ready = True
        _next_oled_ms = time.ticks_add(now_ms, OLED_PERIOD_MS)

        # Immediate proof draw
        _oled.fill(0)
        _oled.text("ENZO V3", 0, 0, 1)
        _oled.text("OLED INIT OK", 0, 12, 1)
        _oled.show()

    except Exception as e:
        _last_oled_err = "OLED init fail: " + repr(e)
        _set_alert(_last_oled_err)
        _oled_ready = False
        _oled = None
        _next_oled_init_ms = time.ticks_add(now_ms, OLED_RETRY_MS)


def _short_err(s, max_len=14):
    if not s:
        return "-"
    s = str(s)
    s = s.replace(" ", "")
    s = s.replace("status=", "st=")
    if len(s) <= max_len:
        return s
    return s[:max_len]


def _oled_tick(now_ms):
    global _next_oled_ms, _v3_tick, _oled_fail_count, _next_oled_reinit_ms, _oled_ready

    if not _oled_ready or _oled is None:
        if time.ticks_diff(now_ms, _next_oled_init_ms) >= 0:
            _oled_init_try(now_ms)
        return

    if _next_oled_reinit_ms and time.ticks_diff(now_ms, _next_oled_reinit_ms) >= 0:
        _oled_init_try(now_ms)
        return

    if time.ticks_diff(now_ms, _next_oled_ms) < 0:
        return
    _next_oled_ms = time.ticks_add(now_ms, OLED_PERIOD_MS)

    try:
        _oled.fill(0)

        _oled.text("ENZO V3", 0, 0, 1)

        ws = status.state.get("wifi_state", "OFF")
        _oled.text("WIFI: " + str(ws), 0, 12, 1)

        # Line 3: show IP when ON, otherwise show error (so we can debug)
        if ws == "ON":
            ip = status.state.get("wifi_ip", "-")
            line3 = "IP: " + str(ip)
        elif ws == "ERR":
            err = status.state.get("wifi_err", "")
            line3 = "ERR: " + _short_err(err, 14)
        else:
            line3 = "IP: -"
        _oled.text(line3, 0, 24, 1)

        if status.state.get("dht_ok", False):
            t = status.state.get("temp_c", None)
            h = status.state.get("rh", None)
            if t is None or h is None:
                th = "T/H: --.-C --%"
            else:
                th = "T/H: %.1fC %d%%" % (float(t), int(h))
        else:
            th = "T/H: --.-C --%"
        _oled.text(th, 0, 36, 1)

        alive = status.state.get("loop_count", 0)
        _oled.text("ALIVE: " + str(alive), 0, 48, 1)

        _oled.show()

        _v3_tick += 1
        status.state["v3_alive"] = _v3_tick
        _oled_fail_count = 0

    except Exception as e:
        _oled_fail_count += 1
        _set_alert("OLED draw fail: " + repr(e))
        _next_oled_reinit_ms = time.ticks_add(now_ms, OLED_FAIL_REINIT_MS)
        _oled_ready = False


def _dht_init_try():
    global _dht_ok, _dht_dev
    _dht_ok = False
    _dht_dev = None
    try:
        if dht is not None:
            _dht_dev = dht.DHT22(Pin(DHT_PIN))
            _dht_ok = True
    except Exception as e:
        _set_alert("DHT init fail: " + repr(e))
        _dht_ok = False


def _dht_tick(now_ms):
    global _next_dht_ms

    if not _dht_ok or _dht_dev is None:
        status.state["dht_ok"] = False
        return

    if time.ticks_diff(now_ms, _next_dht_ms) < 0:
        return

    _next_dht_ms = time.ticks_add(now_ms, DHT_PERIOD_MS)

    try:
        _dht_dev.measure()
        t = _dht_dev.temperature()
        h = _dht_dev.humidity()
        status.state["temp_c"] = t
        status.state["rh"] = h
        status.state["dht_ok"] = True
    except Exception as e:
        status.state["dht_ok"] = False
        _set_alert("DHT read fail: " + repr(e))


def _wifi_init_try():
    global _wlan_sta
    _wlan_sta = None

    if network is None:
        _set_alert("network module missing; STA unavailable")
        return

    try:
        _wlan_sta = network.WLAN(network.STA_IF)
        _wlan_sta.active(False)
    except Exception as e:
        _wlan_sta = None
        _set_alert("STA init fail: " + repr(e))


def _wifi_disconnect():
    global _wifi_state, _wifi_ip, _wifi_err, _wifi_deadline_ms
    try:
        if _wlan_sta is not None:
            try:
                _wlan_sta.disconnect()
            except Exception:
                pass
            try:
                _wlan_sta.active(False)
            except Exception:
                pass
    except Exception:
        pass

    _wifi_state = "OFF"
    _wifi_ip = "-"
    _wifi_err = ""
    _wifi_deadline_ms = 0


def _wifi_start_connect(now_ms):
    global _wifi_state, _wifi_ip, _wifi_err, _wifi_deadline_ms

    if _wlan_sta is None:
        _wifi_state = "ERR"
        _wifi_err = "STA_unavail"
        _wifi_ip = "-"
        return

    try:
        _wlan_sta.active(True)
        _wlan_sta.connect(WIFI_SSID, WIFI_PASS)
        _wifi_state = "POLL"
        _wifi_err = ""
        _wifi_ip = "-"
        _wifi_deadline_ms = time.ticks_add(now_ms, WIFI_TIMEOUT_MS)
    except Exception as e:
        _wifi_state = "ERR"
        _wifi_err = repr(e)
        _wifi_ip = "-"


def _wifi_poll(now_ms):
    global _wifi_state, _wifi_ip, _wifi_err

    if _wifi_state != "POLL":
        return

    if time.ticks_diff(now_ms, _wifi_deadline_ms) >= 0:
        _wifi_state = "ERR"
        try:
            st = _wlan_sta.status() if _wlan_sta is not None else None
        except Exception:
            st = None
        _wifi_err = "timeout" if st is None else ("st=" + str(st))
        _wifi_ip = "-"
        return

    try:
        if _wlan_sta is not None and _wlan_sta.isconnected():
            _wifi_state = "ON"
            try:
                _wifi_ip = _wlan_sta.ifconfig()[0]
            except Exception:
                _wifi_ip = "-"
            _wifi_err = ""
    except Exception as e:
        _wifi_state = "ERR"
        _wifi_err = repr(e)
        _wifi_ip = "-"


def _wifi_led_init_try():
    global _wifi_led, _wifi_led_on, _next_wifi_led_ms
    _wifi_led = None
    _wifi_led_on = False
    _next_wifi_led_ms = 0
    try:
        _wifi_led = Pin(WIFI_LED_PIN, Pin.OUT)
        # default OFF
        _wifi_led.value(1 if (not WIFI_LED_ACTIVE_HIGH) else 0)
    except Exception as e:
        _wifi_led = None
        _set_alert("WiFi LED init fail: " + repr(e))


def _wifi_led_set(on):
    global _wifi_led_on
    _wifi_led_on = bool(on)
    if _wifi_led is None:
        return
    val = 1 if _wifi_led_on else 0
    if not WIFI_LED_ACTIVE_HIGH:
        val = 0 if val else 1
    try:
        _wifi_led.value(val)
    except Exception:
        pass


def _wifi_led_tick(now_ms, disp_state):
    global _next_wifi_led_ms, _wifi_led_on

    if _wifi_led is None:
        return

    # Solid modes
    if disp_state == "ON":
        _wifi_led_set(True)
        return
    if disp_state == "OFF":
        _wifi_led_set(False)
        return

    # Blink modes
    if disp_state == "ERR":
        period = WIFI_LED_BLINK_FAST_MS
    else:
        # START (includes internal POLL)
        period = WIFI_LED_BLINK_SLOW_MS

    if _next_wifi_led_ms == 0:
        _next_wifi_led_ms = time.ticks_add(now_ms, period)
        _wifi_led_set(True)
        return

    if time.ticks_diff(now_ms, _next_wifi_led_ms) >= 0:
        _next_wifi_led_ms = time.ticks_add(now_ms, period)
        _wifi_led_set(not _wifi_led_on)


def _wifi_tick(now_ms):
    global _next_wifi_poll_ms, _wifi_state, _wifi_ip, _wifi_err

    req = False
    try:
        if status.state.get("wifi_req_toggle", False):
            status.state["wifi_req_toggle"] = False
            req = True
    except Exception:
        pass

    if req:
        if _wifi_state in ("OFF", "ERR"):
            _wifi_state = "START"
            _wifi_err = ""
            _wifi_ip = "-"
            _wifi_start_connect(now_ms)
        else:
            _wifi_disconnect()

    if time.ticks_diff(now_ms, _next_wifi_poll_ms) >= 0:
        _next_wifi_poll_ms = time.ticks_add(now_ms, WIFI_POLL_MS)
        _wifi_poll(now_ms)

    # Publish
    disp = _wifi_status_str()
    status.state["wifi_state"] = disp
    status.state["wifi_ip"] = _wifi_ip
    status.state["wifi_err"] = _wifi_err

    # Drive LED from canonical V3 state
    _wifi_led_tick(now_ms, disp)


def init():
    global _next_oled_ms, _next_dht_ms, _next_wifi_poll_ms, _v3_tick
    global _wifi_state, _wifi_ip, _wifi_err, _wifi_deadline_ms
    global _next_oled_init_ms

    _ensure_surface_defaults()
    now = time.ticks_ms()

    _wifi_led_init_try()
    _wifi_init_try()
    _dht_init_try()

    _next_oled_init_ms = now
    _oled_init_try(now)

    _next_oled_ms = time.ticks_add(now, OLED_PERIOD_MS)
    _next_dht_ms = time.ticks_add(now, DHT_PERIOD_MS)
    _next_wifi_poll_ms = time.ticks_add(now, WIFI_POLL_MS)
    _v3_tick = 0

    _wifi_state = "OFF"
    _wifi_ip = "-"
    _wifi_err = ""
    _wifi_deadline_ms = 0
    status.state["wifi_state"] = _wifi_status_str()
    status.state["wifi_ip"] = _wifi_ip
    status.state["wifi_err"] = _wifi_err

    # Ensure LED matches initial state
    _wifi_led_tick(now, "OFF")


def tick(now_ms):
    _wifi_tick(now_ms)
    _dht_tick(now_ms)
    _oled_tick(now_ms)


