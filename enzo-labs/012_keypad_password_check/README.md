# 012 – Keypad Password Check

## What this does
Uses a 4x4 membrane keypad to enter a fixed password and check whether it is correct.

In this build:
- keypad presses are read
- `*` clears the current entry
- `#` submits the current entry
- correct password = success
- wrong password = denied

## What this teaches
- storing keypad input
- building a string from multiple key presses
- clearing input
- submitting input for checking
- simple password / PIN logic

## Parts
- ESP32 dev board
- 4x4 membrane keypad
- jumper wires
- breadboard

## Wiring
This module reuses the keypad wiring from **010 – Keypad Read**.

### Keypad → ESP32
- pin 1 → GPIO13
- pin 2 → GPIO12
- pin 3 → GPIO14
- pin 4 → GPIO27
- pin 5 → GPIO26
- pin 6 → GPIO25
- pin 7 → GPIO33
- pin 8 → GPIO32

## Wiring Diagram

![012 – Keypad Password Check](../../images/010_keypad_read.png)

## Notes
This module uses the same hardware wiring as 010.

The output for this version is shown in the REPL / serial output, not on a display.

Password used in this build:
- `1234`

Key behaviour:
- `*` clears the current entry
- `#` submits the current entry for checking

## Code

```python
from machine import Pin
import time

row_pins = [Pin(13, Pin.OUT), Pin(12, Pin.OUT), Pin(14, Pin.OUT), Pin(27, Pin.OUT)]
col_pins = [
    Pin(26, Pin.IN, Pin.PULL_DOWN),
    Pin(25, Pin.IN, Pin.PULL_DOWN),
    Pin(33, Pin.IN, Pin.PULL_DOWN),
    Pin(32, Pin.IN, Pin.PULL_DOWN),
]

keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

PASSWORD = "1234"
entry = ""

def scan_keypad():
    for r in range(4):
        for row in row_pins:
            row.value(0)

        row_pins[r].value(1)
        time.sleep_us(50)

        for c in range(4):
            if col_pins[c].value():
                return keys[r][c]

    return None

last_key = None

print("Keypad password check ready")
print("Use * to clear, # to submit")

while True:
    key = scan_keypad()

    if key is not None and key != last_key:
        print("Pressed:", key)

        if key == "*":
            entry = ""
            print("CLEARED")

        elif key == "#":
            if entry == PASSWORD:
                print("ACCESS OK")
            else:
                print("DENIED")
            entry = ""

        else:
            entry += key
            print("ENTRY:", entry)

        last_key = key

    if key is None:
        last_key = None

    time.sleep(0.1)
```

## Test
- wire the keypad exactly as in 010
- run the script
- press keys and confirm they are added to the entry
- press `*` and confirm the entry clears
- enter `1234` and press `#`
- confirm `ACCESS OK`
- enter a wrong code and press `#`
- confirm `DENIED`

## Definition of done
- keypad reads correctly
- entry builds correctly
- `*` clears the input
- `#` submits the input
- correct password = success
- wrong password = fail

## What this enables next
- keypad + LCD entry display
- keypad servo lock
- keypad + LCD password lock
