# app/state.py
from app.config import SCHEMA_VERSION

DEFAULT_STATE = {
    "schema": SCHEMA_VERSION,
    "uptime.ms": 0,
    "loop_count": 0,
    
    "sensors": {
        "temp_c": None,
        "hum_pct": None,
        "distance_cm": None,
    },
    
    "actuators": {
        "pwm_percent": 0,
        "led_pin": None,
    },
    
    "comms": {
        "last_cmd": None,
        "rx_lines": 0,
        "tx_lines": 0,
    },
    
    "status": {
        "last_error": None,
        "mode": "normal",
        }
    }
state = DEFAULT_STATE.copy()

def set_error(msg):
    start["status"]["last_error"] = msg
