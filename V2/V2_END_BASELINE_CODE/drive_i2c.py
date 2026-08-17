# app/drive_i2c.py
# V2 PH4 motor service (I2C driver + deadman safety)
#
# - Safe authority lives here: if comms go quiet -> STOP
# - Input adapters (USB/HTTP/etc) only call set_cmd()

from machine import Pin, I2C
import time

# Known-good I2C setup (your V2 proof-of-life + PH2/PH3)
I2C_ID = 0
SDA_PIN = 8
SCL_PIN = 9
I2C_FREQ = 100_000
ADDR = 0x14

MOTOR_LEFT = 0
MOTOR_RIGHT = 1

CMD_STOP = 0x01
CMD_RUN_CW = 0x02
CMD_RUN_CCW = 0x03

SPEED = 200

# If forward is physically backwards, swap these two:
FWD_CMD = CMD_RUN_CCW
REV_CMD = CMD_RUN_CW

FAILSAFE_MS = 250
STOP_RETRY_MS = 50

_i2c = None
_last_rx_ms = 0
_last_cmd = "X"
_stop_pending = False
_last_stop_attempt_ms = 0
_last_error = ""


def init():
    global _i2c, _last_rx_ms, _last_cmd
    if _i2c is None:
        _i2c = I2C(I2C_ID, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=I2C_FREQ)
    _last_rx_ms = time.ticks_ms()
    _last_cmd = "X"
    if not stop_all():
        raise RuntimeError("motor driver 0x14 did not accept STOP")
    return True


def _send(cmd, motor, speed=0):
    global _last_error
    if _i2c is None:
        _last_error = "motor I2C is not initialized"
        return False
    try:
        _i2c.writeto(ADDR, bytes([cmd, motor, speed]))
        return True
    except Exception as e:
        _last_error = repr(e)
        return False


def stop_all():
    global _stop_pending, _last_cmd, _last_stop_attempt_ms, _last_error
    _last_error = ""
    left_ok = _send(CMD_STOP, MOTOR_LEFT)
    right_ok = _send(CMD_STOP, MOTOR_RIGHT)
    ok = left_ok and right_ok
    _last_stop_attempt_ms = time.ticks_ms()
    _stop_pending = not ok
    if ok:
        _last_cmd = "X"
    return ok


def _motion_pair(left_cmd, right_cmd):
    """Apply both motor writes or fail closed and request a confirmed STOP."""
    global _stop_pending, _last_error
    _last_error = ""
    left_ok = _send(left_cmd, MOTOR_LEFT, SPEED)
    right_ok = _send(right_cmd, MOTOR_RIGHT, SPEED)
    if left_ok and right_ok:
        _stop_pending = False
        return True

    # A partial command is unsafe. Attempt STOP immediately; tick() keeps
    # retrying if either STOP write also fails.
    motion_error = _last_error or "motor movement write was not accepted"
    _stop_pending = True
    if stop_all():
        # Keep the movement failure available to the HTTP error response even
        # though the immediate recovery STOP succeeded.
        _last_error = motion_error
    return False


def forward():
    return _motion_pair(FWD_CMD, FWD_CMD)


def reverse():
    return _motion_pair(REV_CMD, REV_CMD)


def pivot_left():
    # Left backwards, right forwards
    return _motion_pair(REV_CMD, FWD_CMD)


def pivot_right():
    # Right backwards, left forwards
    return _motion_pair(FWD_CMD, REV_CMD)


def _apply_cmd_now(c: str) -> bool:
    c = (c or "").upper()
    if c == "W":
        return forward()
    if c == "S":
        return reverse()
    if c == "A":
        return pivot_left()
    if c == "D":
        return pivot_right()
    if c == "X" or c == " ":
        return stop_all()
    return False


def set_cmd(c: str) -> bool:
    """
    Called by input adapters (HTTP, USB, etc.)
    Updates last_rx timestamp and applies the command immediately.
    """
    global _last_rx_ms, _last_cmd, _last_error
    normalized = (c or "").upper()

    if normalized not in ("W", "A", "S", "D", "X", " "):
        _last_error = "invalid command"
        return False

    # Do not accept more movement while a previous STOP is unconfirmed.
    # A repeated dashboard request can move again after tick() confirms STOP.
    if _stop_pending and normalized not in ("X", " "):
        if stop_all():
            _last_error = "previous STOP was pending; retry movement command"
        return False

    ok = _apply_cmd_now(c)
    if ok:
        _last_rx_ms = time.ticks_ms()
        _last_cmd = "X" if normalized in ("X", " ") else normalized
    return ok


def tick():
    """
    Called frequently by tasks loop.
    Enforces deadman STOP when input goes quiet.
    """
    global _last_rx_ms, _last_cmd
    if _i2c is None:
        return

    now = time.ticks_ms()

    # A failed STOP remains pending until both motors acknowledge STOP.
    if _stop_pending:
        if time.ticks_diff(now, _last_stop_attempt_ms) >= STOP_RETRY_MS:
            stop_all()
        return

    if _last_cmd != "X" and time.ticks_diff(now, _last_rx_ms) > FAILSAFE_MS:
        stop_all()
        _last_rx_ms = now


def last_error():
    return _last_error
