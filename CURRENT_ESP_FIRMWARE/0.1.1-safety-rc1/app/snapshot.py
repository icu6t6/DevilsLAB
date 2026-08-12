# app/snapshot.py
# T2 additive: structured "truth snapshot" export over REPL/serial.
#
# One-line format:
#   SNAP <json>
#
# Observation-only: reads app.status.state, never drives behaviour.

import time

try:
    from machine import UART
except Exception:
    UART = None

try:
    import ujson as json
except Exception:
    import json  # type: ignore

import app.status as status
from app import imu

SNAPSHOT_FIRST_DELAY_MS = 10000
SNAPSHOT_EVERY_MS = 60000

_seq = 0
_next_ms = 0
_uart = None
_uart_init_ok = False
_uart_init_attempted = False


def _ticks_ms():
    return time.ticks_ms()


def _ensure_uart():
    """
    UART transport currently disabled here.
    Snapshot still prints to REPL/console.
    """
    return False


def record_selftest(ok: bool):
    """Record boot-gate result into the shared status surface."""
    s = status.state
    s["boot_ok"] = bool(ok)
    s["safe_mode"] = not bool(ok)

    st = s.get("selftest", {})
    if not isinstance(st, dict):
        st = {}

    st["ok"] = bool(ok)

    if "ldr_adc" not in st:
        st["ldr_adc"] = None

    if "imu" not in st or not isinstance(st.get("imu"), dict):
        st["imu"] = {"ok": False, "err": ""}

    s["selftest"] = st


def record_ph4(ap_ip=None, url=None, http_ready=None, ok=None, err=None):
    """Record PH4 status into the shared status surface."""
    s = status.state
    ph4 = s.get("ph4", {})
    if not isinstance(ph4, dict):
        ph4 = {}

    if ap_ip is not None:
        ph4["ap_ip"] = str(ap_ip)
    if url is not None:
        ph4["url"] = str(url)
    if http_ready is not None:
        ph4["http_ready"] = bool(http_ready)
    if ok is not None:
        ph4["ok"] = bool(ok)
    if err is not None:
        ph4["err"] = str(err)

    s["ph4"] = ph4


def record_v3(ok=None, err=None, alive=None):
    """Record V3 observer layer status into the shared status surface."""
    s = status.state
    v3 = s.get("v3", {})
    if not isinstance(v3, dict):
        v3 = {}

    if ok is not None:
        v3["ok"] = bool(ok)
    if err is not None:
        v3["err"] = str(err)
    if alive is not None:
        try:
            v3["alive"] = int(alive)
        except Exception:
            v3["alive"] = alive

    s["v3"] = v3


def _wifi_block(s):
    return {
        "enabled": bool(s.get("wifi_enabled", False)),
        "state": str(s.get("wifi_state", "OFF")),
        "ip": str(s.get("wifi_ip", "-")),
        "err": str(s.get("wifi_err", "")),
        "req_toggle": bool(s.get("wifi_req_toggle", False)),
    }


def build_snapshot(now_ms=None):
    global _seq
    _seq += 1
    if now_ms is None:
        now_ms = _ticks_ms()

    s = status.state

    st = s.get("selftest", {})
    if not isinstance(st, dict):
        st = {}

    ph4 = s.get("ph4", {})
    if not isinstance(ph4, dict):
        ph4 = {}

    v3 = s.get("v3", {})
    if not isinstance(v3, dict):
        v3 = {}

    imu_selftest = st.get("imu", {})
    if not isinstance(imu_selftest, dict):
        imu_selftest = {}

    snap = {
        "type": "status_snapshot",
        "schema": "t2.snapshot.v0",
        "seq": _seq,
        "t_ms": int(now_ms),

        "project": str(s.get("project", "ENZO")),
        "ver": str(s.get("ver", "")),
        "reset_cause": s.get("reset_cause", None),

        "uptime_ms": int(s.get("uptime_ms", s.get("uptime", 0)) or 0),
        "loop_count": int(s.get("loop_count", 0) or 0),

        "boot_ok": bool(s.get("boot_ok", True)),
        "safe_mode": bool(s.get("safe_mode", False)),

        "selftest": {
            "ok": bool(st.get("ok", s.get("boot_ok", True))),
            "ldr_adc": st.get("ldr_adc", None),
            "imu": {
                "ok": bool(imu_selftest.get("ok", s.get("imu_ok", False))),
                "err": str(imu_selftest.get("err", s.get("imu_err", ""))),
            },
        },

        "ph4": {
            "ok": bool(ph4.get("ok", s.get("ph4_ok", False))),
            "ap_ip": ph4.get("ap_ip", "-"),
            "url": ph4.get("url", ""),
            "http_ready": bool(ph4.get("http_ready", s.get("ph4_ok", False))),
            "err": ph4.get("err", ""),
        },

        "v3": {
            "ok": bool(v3.get("ok", s.get("v3_ok", False))),
            "alive": int(v3.get("alive", s.get("v3_alive", 0)) or 0),
            "err": v3.get("err", ""),
        },

        "wifi": _wifi_block(s),
        "sensors": {
            "dht_ok": bool(s.get("dht_ok", False)),
            "temp_c": s.get("temp_c", None),
            "rh": s.get("rh", None),
            "ldr_adc": st.get("ldr_adc", None),
        },

        "i2c_addrs": s.get("i2c_addrs", []) or [],
        "imu": imu.get_snapshot(now_ms),
        "alerts": (s.get("alerts", []) or [])[-5:],

        "rails": {
            "logic_5v": {"en": None, "v": None, "a": None, "status": None},
            "dut_5v":   {"en": None, "v": None, "a": None, "status": None},
            "dut_3v3":  {"en": None, "v": None, "a": None, "status": None},
        },
    }

    return snap


def emit_snapshot(now_ms=None):
    try:
        snap = build_snapshot(now_ms)
        line = "SNAP " + json.dumps(snap)

        print(line)

        if _ensure_uart() and _uart is not None:
            try:
                _uart.write(line + "\n")
            except Exception as e:
                try:
                    print("[snapshot] UART write fail:", repr(e))
                except Exception:
                    pass

        return True
    except Exception as e:
        try:
            print("[snapshot] emit fail:", repr(e))
        except Exception:
            pass
        return False


def emit_if_due(now_ms=None):
    global _next_ms
    if now_ms is None:
        now_ms = _ticks_ms()

    if _next_ms == 0:
        _next_ms = time.ticks_add(now_ms, SNAPSHOT_FIRST_DELAY_MS)
        return False

    if time.ticks_diff(now_ms, _next_ms) >= 0:
        _next_ms = time.ticks_add(now_ms, SNAPSHOT_EVERY_MS)
        return emit_snapshot(now_ms)

    return False

