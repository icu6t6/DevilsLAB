# app/config.py

PROJECT = "Deskbot"
SCHEMA_VERSION = 1

WIFI_SSID = "yourSSIDhere"
WIFI_PASS = "yourPassworHere"


# Board profile (esp32s3 devkit)
BOARD = "esp32s3_devkit"

BOARD_PROFILES = {
    "esp32s3_devkit":{
        # BOOT button is usually GPIO0 onthis board.
        # Onboard RGB/LED is often on GPIO48; GPIO 2 is a common fallback.
        "LED_PINS": [2],
        "PWM_PIN": 5,
        "SAFE_PIN": -1,
        "LED_ACTIVE_LOW": True,
        
        "HEARTBEAT_ON_MS": 1000,
        "HEARTBEAT_OFF_MS": 2000,
        
        "BOOT_MS": 3000,
        "BOOT_ON_MS": 150,
        "BOOT_OFF_MS": 150,
        }
    }
P = BOARD_PROFILES[BOARD]
LED_PINS = P["LED_PINS"]
PWM_PIN = P["PWM_PIN"]
SAFE_PIN = P["SAFE_PIN"]
LED_ACTIVE_LOW   = P.get("LED_ACTIVE_LOW", False)
HEARTBEAT_ON_MS  = P.get("HEARTBEAT_ON_MS", 1000 // 2)
HEARTBEAT_OFF_MS = P.get("HEARTBEAT_OFF_MS", 2000 // 2)

# Loop timing

LOOP_HZ = 20
LOOP_DELAY_MS = int(1000 / LOOP_HZ)

HEARTBEAT_MS = 1000
TELEMETERY_MS = 1000

# Features
ENABLE_USB = True
ENABLE_LOGGING = False
ENABLE_WATCHDOG = False

DEBUG = True
