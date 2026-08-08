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

_i2c = None
_last_rx_ms = 0
_last_cmd = "X"


def init():
    global _i2c, _last_rx_ms, _last_cmd
    if _i2c is None:
        _i2c = I2C(I2C_ID, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=I2C_FREQ)
    _last_rx_ms = time.ticks_ms()
    _last_cmd = "X"
    stop_all()


def _send(cmd, motor, speed=0):
    try:
        _i2c.writeto(ADDR, bytes([cmd, motor, speed]))
    except Exception:
        # A later deadman window will retry STOP if comms remain silent.
        pass


def stop_all():
    _send(CMD_STOP, MOTOR_LEFT)
    _send(CMD_STOP, MOTOR_RIGHT)


def forward():
    _send(FWD_CMD, MOTOR_LEFT, SPEED)
    _send(FWD_CMD, MOTOR_RIGHT, SPEED)


def reverse():
    _send(REV_CMD, MOTOR_LEFT, SPEED)
    _send(REV_CMD, MOTOR_RIGHT, SPEED)


def pivot_left():
    # Left backwards, right forwards
    _send(REV_CMD, MOTOR_LEFT, SPEED)
    _send(FWD_CMD, MOTOR_RIGHT, SPEED)


def pivot_right():
    # Right backwards, left forwards
    _send(FWD_CMD, MOTOR_LEFT, SPEED)
    _send(REV_CMD, MOTOR_RIGHT, SPEED)


def _apply_cmd_now(c: str) -> bool:
    c = (c or "").upper()
    if c == "W":
        forward()
        return True
    if c == "S":
        reverse()
        return True
    if c == "A":
        pivot_left()
        return True
    if c == "D":
        pivot_right()
        return True
    if c == "X" or c == " ":
        stop_all()
        return True
    return False


def set_cmd(c: str) -> bool:
    """
    Called by input adapters (HTTP, USB, etc.)
    Updates last_rx timestamp and applies the command immediately.
    """
    global _last_rx_ms, _last_cmd
    ok = _apply_cmd_now(c)
    if ok:
        _last_rx_ms = time.ticks_ms()
        _last_cmd = (c or "X").upper()
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
    if time.ticks_diff(now, _last_rx_ms) > FAILSAFE_MS:
        # Retry STOP once per deadman window for as long as commands stay silent.
        stop_all()
        _last_cmd = "X"
        _last_rx_ms = now
