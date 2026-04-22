# 007 – RFID Status RGB

## What this does
Uses an RC522 RFID reader to check a scanned tag or card and give a simple RGB status response.

In this build:
- authorised UID → green flash
- unknown UID → red flash
- then the LED returns to off

## What this teaches
- using RFID input to drive output behaviour
- comparing scanned UIDs against an authorised value
- creating a simple access status indicator
- returning outputs to a known idle state
- using `try/finally` to leave hardware in a safe state when the script stops

## Parts
- ESP32
- RC522 RFID reader
- RFID card
- RFID fob
- RGB LED (common anode)
- 2 × 220Ω resistors
- jumper wires
- breadboard

## Wiring

### RC522 → ESP32
- SDA → GPIO5
- SCK → GPIO18
- MOSI → GPIO23
- MISO → GPIO19
- RST → GPIO22
- 3.3V → 3.3V
- GND → GND
- IRQ → not connected

### Status LED
This build uses red and green only.

- RGB common leg → 3.3V
- red leg → 220Ω → GPIO4
- green leg → 220Ω → GPIO21
- blue leg → not connected

## Wiring Diagram

![007 – RFID Status RGB](../../images/007.png)

## Important
The RC522 must be powered from **3.3V**, not 5V.

The `mfrc522.py` driver file must already be saved onto the **MicroPython device** before running this script.

This RGB LED is common anode, so:
- `0` = channel ON
- `1` = channel OFF

## Notes
This version uses a timed flash for each result and then returns the LED to off.

Stopping the script also turns the LED off cleanly.

## Authorised UID used in this build
```text
[35, 166, 153, 13, 17]
```

## Code

```python
from machine import Pin
from mfrc522 import MFRC522
import time

# Status LED pins (common anode RGB, using red + green only)
red = Pin(4, Pin.OUT)
green = Pin(21, Pin.OUT)

# RFID reader
rdr = MFRC522(sck=18, mosi=23, miso=19, rst=22, cs=5)

# Authorised UID (blue fob)
AUTHORIZED_UID = [35, 166, 153, 13, 17]

def led_off():
    red.value(1)
    green.value(1)

def show_red():
    red.value(0)
    green.value(1)

def show_green():
    red.value(1)
    green.value(0)

led_off()
print("RFID status ready")

last_uid = None
last_time = 0

try:
    while True:
        stat, _ = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:
            stat, raw_uid = rdr.anticoll()

            if stat == rdr.OK:
                now = time.ticks_ms()

                if raw_uid != last_uid or time.ticks_diff(now, last_time) > 1500:
                    print("UID:", raw_uid)

                    if raw_uid == AUTHORIZED_UID:
                        print("AUTHORISED")
                        show_green()
                    else:
                        print("UNKNOWN")
                        show_red()

                    time.sleep(1.0)   # show result for 1 second
                    led_off()

                    last_uid = raw_uid
                    last_time = now

        time.sleep(0.1)

finally:
    led_off()
```

## Test
- run the script
- present the authorised fob
- confirm the LED flashes green, then turns off
- present an unknown card or fob
- confirm the LED flashes red, then turns off
- stop the script
- confirm the LED returns to off

## What this enables next
→ 008 – RFID Servo Lock
