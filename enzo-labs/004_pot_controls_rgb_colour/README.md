# 004 – Pot Controls RGB Colour

## What this does
Uses a potentiometer to select which RGB LED colour is active.

## What this teaches
- analog input affecting output
- reading a live ADC value
- splitting an analog range into zones
- controlling outputs from input thresholds

## Parts
- ESP32
- RGB LED
- 3 × 220Ω resistors
- potentiometer
- breadboard
- jumper wires

## Wiring
Keep the RGB LED wiring from earlier circuits:
- red channel → GPIO2 through 220Ω
- green channel → GPIO5 through 220Ω
- blue channel → GPIO21 through 220Ω
- RGB common leg → 3.3V

Add potentiometer:
Facing the potentiometer:
- left leg → 3.3V
- middle leg → GPIO34
- right leg → GND

## Wiring Diagram

![Pot controls RGB colour](../images/004_pot_rgb_colour.png)

## Notes
Observed potentiometer behaviour in this build:
- clockwise → reading decreases toward 0
- anticlockwise → reading increases toward 4095

This RGB circuit is active-low:
- `0` = channel ON
- `1` = channel OFF

## LED Pin Test (optional)
Use this to confirm RGB wiring is correct before using the potentiometer:

```python
from machine import Pin
import time

red = Pin(2, Pin.OUT, value=1)
green = Pin(5, Pin.OUT, value=1)
blue = Pin(21, Pin.OUT, value=1)

while True:
    red.value(0); green.value(1); blue.value(1)
    print("RED")
    time.sleep(1)

    red.value(1); green.value(0); blue.value(1)
    print("GREEN")
    time.sleep(1)

    red.value(1); green.value(1); blue.value(0)
    print("BLUE")
    time.sleep(1)
```

Expected result:
- LED cycles Red → Green → Blue

## Code

```python
from machine import Pin, ADC
import time

red = Pin(2, Pin.OUT, value=1)
green = Pin(5, Pin.OUT, value=1)
blue = Pin(21, Pin.OUT, value=1)

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

while True:
    value = pot.read()

    if value < 1365:
        red.value(0)
        green.value(1)
        blue.value(1)
    elif value < 2730:
        red.value(1)
        green.value(0)
        blue.value(1)
    else:
        red.value(1)
        green.value(1)
        blue.value(0)

    print(value)
    time.sleep(0.1)
```

## Test
- turn potentiometer fully one way → one colour
- turn to middle → second colour
- turn fully the other way → third colour

## What this enables next
→ 005 – Pot controls RGB brightness (PWM)
