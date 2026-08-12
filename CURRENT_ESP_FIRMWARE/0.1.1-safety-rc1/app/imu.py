from machine import Pin, I2C
import struct
import time

SCL_PIN = 9
SDA_PIN = 8
MPU_ADDR = 0x68

PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
WHO_AM_I = 0x75

_i2c = None
_inited = False
_last_poll_ms = 0
_poll_interval_ms = 1000

_state = {
    "ok": False,
    "addr": MPU_ADDR,
    "ax": None,
    "ay": None,
    "az": None,
    "gx": None,
    "gy": None,
    "gz": None,
    "temp_c": None,
    "sample_age_ms": None,
    "err": "",
}


def init():
    global _i2c, _inited

    if _inited:
        return True

    try:
        _i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)

        who = _i2c.readfrom_mem(MPU_ADDR, WHO_AM_I, 1)[0]
        if who != 0x68:
            _state["ok"] = False
            _state["err"] = "whoami_mismatch"
            return False

        _i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, b"\x00")
        time.sleep_ms(100)

        _state["ok"] = True
        _state["err"] = ""
        _inited = True
        return True

    except Exception as e:
        _state["ok"] = False
        _state["err"] = str(e)
        return False


def boot_check():
    try:
        ok = init()
        if not ok:
            return False, _state.get("err", "init_failed")

        who = _i2c.readfrom_mem(MPU_ADDR, WHO_AM_I, 1)[0]
        if who != 0x68:
            return False, "whoami_mismatch"

        return True, ""
    except Exception as e:
        return False, str(e)


def poll(now_ms):
    global _last_poll_ms

    if not _inited:
        init()

    if not _inited:
        return

    if time.ticks_diff(now_ms, _last_poll_ms) < _poll_interval_ms:
        if _last_poll_ms:
            _state["sample_age_ms"] = time.ticks_diff(now_ms, _last_poll_ms)
        return

    try:
        data = _i2c.readfrom_mem(MPU_ADDR, ACCEL_XOUT_H, 14)
        ax, ay, az, temp_raw, gx, gy, gz = struct.unpack(">hhhhhhh", data)
        temp_c = (temp_raw / 340.0) + 36.53

        _state["ok"] = True
        _state["ax"] = ax
        _state["ay"] = ay
        _state["az"] = az
        _state["gx"] = gx
        _state["gy"] = gy
        _state["gz"] = gz
        _state["temp_c"] = round(temp_c, 2)
        _state["err"] = ""

        _last_poll_ms = now_ms
        _state["sample_age_ms"] = 0

    except Exception as e:
        _state["ok"] = False
        _state["err"] = str(e)


def get_snapshot(now_ms=None):
    return {
        "ok": _state["ok"],
        "addr": _state["addr"],
        "ax": _state["ax"],
        "ay": _state["ay"],
        "az": _state["az"],
        "gx": _state["gx"],
        "gy": _state["gy"],
        "gz": _state["gz"],
        "temp_c": _state["temp_c"],
        "sample_age_ms": _state["sample_age_ms"],
        "err": _state["err"],
    }

