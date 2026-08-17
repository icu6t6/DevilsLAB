# app/eyes_8led.py
# Baseline: eyes_8led_updated.py
#
# Adds:
#   - Squint support: tasks can cap brightness when LDR says it's bright.
#   - Comet-style startup animation (blue -> red -> green -> purple).

from machine import Pin
import neopixel
import time

# ----------------------------
# Hardware
# ----------------------------
PIN = 16
NUM = 8

# Your eyes are two pixels within the 8-LED bar
LEFT_EYE = 1
RIGHT_EYE = 3

# ----------------------------
# Brightness model
# ----------------------------
# Levels are small integers so it stays comfy.
# 0 = off, 1 = very dim, 2 = dim (default), 3 = normal
MAX_LEVEL = 2

# Global brightness scalar (percentage). 25 = ~quarter brightness everywhere.
GLOBAL_BRIGHTNESS = 8

_np = None
_pin = PIN
_num = NUM

_mode = "idle"
_level = 2

# Squint brightness cap (None = disabled)
_squint_level = None

# Animation state
_phase = False  # used by idle/blink
_next_ms = 0

# Idle blink timings (open longer, close shorter)
IDLE_OPEN_MS = 3000
IDLE_CLOSED_MS = 120

# Blink mode timings
BLINK_OPEN_MS = 400
BLINK_CLOSED_MS = 150

# Colours
COLOR_OFF = (0, 0, 0)
COLOR_IDLE = (0, 0, 255)    # blue
COLOR_ANGRY = (255, 0, 0)   # red
COLOR_HAPPY = (0, 255, 0)   # green

BOOT_COLORS = [
    (0, 0, 255),      # blue
    (0, 0, 255),      # blue
    (0, 255, 0),      # green
    (0, 0, 255),    # blue
]


def _clamp_level(lvl: int) -> int:
    if lvl < 0:
        return 0
    if lvl > MAX_LEVEL:
        return MAX_LEVEL
    return lvl


def _effective_level() -> int:
    lvl = _level
    if _squint_level is not None:
        lvl = min(lvl, _squint_level)
    return _clamp_level(lvl)


def _scale(rgb, lvl: int):
    """Scale an RGB tuple by a small integer level."""
    lvl = _clamp_level(lvl)
    if lvl == 0:
        return (0, 0, 0)
    return (
        ((rgb[0] * lvl) * GLOBAL_BRIGHTNESS) // (MAX_LEVEL * 100),
        ((rgb[1] * lvl) * GLOBAL_BRIGHTNESS) // (MAX_LEVEL * 100),
        ((rgb[2] * lvl) * GLOBAL_BRIGHTNESS) // (MAX_LEVEL * 100),
    )


def init(pin: int = PIN, num: int = NUM):
    global _np, _pin, _num
    _pin = pin
    _num = num
    _np = neopixel.NeoPixel(Pin(_pin, Pin.OUT), _num)
    clear()


def clear():
    if _np is None:
        return
    for i in range(_num):
        _np[i] = (0, 0, 0)
    _np.write()


def set_squint_level(level=None):
    """Cap brightness while squinting.

    level: None disables squint, otherwise 0..MAX_LEVEL
    """
    global _squint_level
    if level is None:
        _squint_level = None
        return
    _squint_level = _clamp_level(int(level))


def set_mode(mode: str, level: int = 2):
    """Set the current eye mode.

    mode: idle | blink | solid | off | angry | happy
    level: 0..MAX_LEVEL
    """
    global _mode, _level, _phase, _next_ms
    _mode = mode
    _level = _clamp_level(int(level))
    _phase = False
    _next_ms = 0
    _draw_static()


def _draw_static():
    if _np is None:
        return
    for i in range(_num):
        _np[i] = COLOR_OFF
    lvl = _effective_level()
    if _mode == "off":
        pass
    elif _mode == "solid":
        _np[LEFT_EYE] = _scale(COLOR_IDLE, lvl)
        _np[RIGHT_EYE] = _scale(COLOR_IDLE, lvl)
    elif _mode == "angry":
        _np[LEFT_EYE] = _scale(COLOR_ANGRY, lvl)
        _np[RIGHT_EYE] = _scale(COLOR_ANGRY, lvl)
    elif _mode == "happy":
        _np[LEFT_EYE] = _scale(COLOR_HAPPY, lvl)
        _np[RIGHT_EYE] = _scale(COLOR_HAPPY, lvl)
    elif _mode == "idle":
        _np[LEFT_EYE] = _scale(COLOR_IDLE, lvl)
        _np[RIGHT_EYE] = _scale(COLOR_IDLE, lvl)
    elif _mode == "blink":
        _np[LEFT_EYE] = _scale(COLOR_IDLE, lvl)
        _np[RIGHT_EYE] = _scale(COLOR_IDLE, lvl)
    _np.write()


def startup_show():
    if _np is None:
        return
    tail = 3
    delay_ms = 35
    for color in BOOT_COLORS:
        for head in range(_num + tail):
            for i in range(_num):
                _np[i] = (0, 0, 0)
            for t in range(tail):
                pos = head - t
                if 0 <= pos < _num:
                    lvl = max(MAX_LEVEL - t, 1)
                    _np[pos] = _scale(color, lvl)
            _np.write()
            time.sleep_ms(delay_ms)
    set_mode("idle", level=_level)


def tick():
    global _phase, _next_ms
    if _np is None:
        return
    now = time.ticks_ms()
    if _mode in ("off", "solid", "angry", "happy"):
        return
    lvl = _effective_level()
    if _mode == "idle":
        if _next_ms == 0:
            _phase = True
            _next_ms = time.ticks_add(now, IDLE_OPEN_MS)
            _draw_idle(open_=True, lvl=lvl)
            return
        if time.ticks_diff(now, _next_ms) >= 0:
            _phase = not _phase
            _next_ms = time.ticks_add(now, IDLE_OPEN_MS if _phase else IDLE_CLOSED_MS)
            _draw_idle(open_=_phase, lvl=lvl)
    elif _mode == "blink":
        if _next_ms == 0:
            _phase = True
            _next_ms = time.ticks_add(now, BLINK_OPEN_MS)
            _draw_idle(open_=True, lvl=lvl)
            return
        if time.ticks_diff(now, _next_ms) >= 0:
            _phase = not _phase
            _next_ms = time.ticks_add(now, BLINK_OPEN_MS if _phase else BLINK_CLOSED_MS)
            _draw_idle(open_=_phase, lvl=lvl)


def _draw_idle(open_: bool, lvl: int):
    for i in range(_num):
        _np[i] = (0, 0, 0)
    if open_:
        _np[LEFT_EYE] = _scale(COLOR_IDLE, lvl)
        _np[RIGHT_EYE] = _scale(COLOR_IDLE, lvl)
    else:
        _np[LEFT_EYE] = (0, 0, 0)
        _np[RIGHT_EYE] = (0, 0, 0)
    _np.write()
