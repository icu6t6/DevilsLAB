# 018 – Ultrasonic LED Bar Distance Display

## What this does

This module combines the two previous ENZO-Labs builds:

- **016 – Ultrasonic Read**
- **017 – LED Bar Graph Sweep**

The HC-SR04 ultrasonic sensor provides the input and the 10-segment LED bar provides the output.

Move an object closer to the sensor and more LEDs light. Move it farther away and fewer LEDs light.

This is the first step in this sequence where a measured sensor value directly controls a multi-output display.

---

## What this teaches

- Combining two already-proven circuits into one system
- Reading distance with an HC-SR04 ultrasonic sensor
- Protecting an ESP32 GPIO with a resistor voltage divider
- Filtering several sensor readings before using the result
- Converting a measured value into an output level
- Driving ten separate LED segments from GPIO
- Building on earlier modules instead of starting again

---

## Parts

This module builds directly on **017** and adds the ultrasonic circuit from **016**.

- ESP32 development board
- HC-SR04 ultrasonic sensor
- 10-segment LED bar graph
- 10 × **1 kΩ** resistors for the LED bar
- 1 × **1 kΩ** resistor for the ECHO divider
- 1 × **2 kΩ** resistor for the ECHO divider
- Breadboard
- Jumper wires
- USB cable / normal ESP32 bench power

---

## Wiring

Keep the complete LED bar circuit from **017** in place.

### LED bar

The ten LED segments use this GPIO order:

```text
Segment 1  -> GPIO13
Segment 2  -> GPIO12
Segment 3  -> GPIO14
Segment 4  -> GPIO27
Segment 5  -> GPIO26
Segment 6  -> GPIO25
Segment 7  -> GPIO33
Segment 8  -> GPIO32
Segment 9  -> GPIO23
Segment 10 -> GPIO22
```

Each segment uses its own **1 kΩ** resistor.

The opposite side of every LED segment returns to the common ground rail.

### Ultrasonic sensor

```text
HC-SR04 GND  -> common GND
HC-SR04 VCC  -> VIN / 5 V
HC-SR04 TRIG -> GPIO5

HC-SR04 ECHO
    -> 1 kΩ
    -> GPIO18 junction
    -> 2 kΩ
    -> GND
```

The ESP32, ultrasonic sensor and LED bar must share a common ground.

---

## Wiring Diagram

![018 Ultrasonic LED Bar Distance Display wiring diagram](../../images/018_led_bar_graph_sweep_ultrasonic.png)

The diagram continues directly from **017**. The added section is the HC-SR04 wiring and the ECHO voltage divider feeding GPIO18.

---

## Important

The HC-SR04 ECHO signal must **not** be connected directly to GPIO18.

This build uses:

```text
ECHO -> 1 kΩ -> GPIO18 junction -> 2 kΩ -> GND
```

The divider reduces the ECHO signal before it reaches the ESP32 input.

The resistor values used on the tested physical build are:

```text
LED bar resistors:       1 kΩ each
ECHO divider upper leg:  1 kΩ
ECHO divider lower leg:  2 kΩ
```

These resistor values were checked on the physical build with power removed.

If you are using a different ESP32 board, check its pin labels before copying the physical layout.

---

## Bring-up check

Before running the combined program:

1. Confirm the 017 LED bar still works.
2. Confirm every LED segment has its own 1 kΩ resistor.
3. Confirm the HC-SR04 shares ground with the ESP32.
4. Confirm TRIG goes to GPIO5.
5. Confirm ECHO passes through the 1 kΩ / 2 kΩ divider before GPIO18.
6. Confirm VCC goes to VIN / 5 V.
7. Check the breadboard for loose resistor legs or jumper wires.

A loose breadboard connection can cause dim, ghosting or missing LED segments.

---

## Code

```python
from machine import Pin, time_pulse_us
from time import sleep, sleep_us

# Ultrasonic pins
TRIG_PIN = 5
ECHO_PIN = 18

# LED bar GPIO order
led_pins = [
    13,
    12,
    14,
    27,
    26,
    25,
    33,
    32,
    23,
    22
]

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

leds = []

for pin_num in led_pins:
    pin = Pin(pin_num, Pin.OUT)
    pin.value(0)
    leds.append(pin)

trig.value(0)
sleep(1)

print("018 Ultrasonic LED Bar Distance Display")
print("Filtered distance test")
print("Close object = more LEDs")
print("Far object = fewer LEDs")


def single_distance_cm():
    trig.value(0)
    sleep_us(2)

    trig.value(1)
    sleep_us(10)

    trig.value(0)

    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return None

    distance_cm = (duration * 0.0343) / 2

    # Ignore silly values for this module's useful range
    if distance_cm < 2 or distance_cm > 150:
        return None

    return round(distance_cm, 1)


def filtered_distance_cm():
    readings = []

    for _ in range(5):
        value = single_distance_cm()

        if value is not None:
            readings.append(value)

        sleep(0.04)

    if len(readings) == 0:
        return None

    readings.sort()

    # Use middle reading to reject random jumps
    middle_index = len(readings) // 2
    return readings[middle_index]


def distance_to_led_count(distance_cm):
    if distance_cm is None:
        return 0

    if distance_cm > 100:
        return 0

    led_count = 10 - int(distance_cm // 10)

    if led_count < 0:
        led_count = 0

    if led_count > 10:
        led_count = 10

    return led_count


def show_bar(count):
    for index, led in enumerate(leds):
        if index < count:
            led.value(1)
        else:
            led.value(0)


while True:
    distance = filtered_distance_cm()
    led_count = distance_to_led_count(distance)

    show_bar(led_count)

    if distance is None:
        print("No stable echo -> LEDs:", led_count)
    else:
        print("Distance:", distance, "cm -> LEDs:", led_count)

    sleep(0.25)
```

---

## Code Explanation

### 1. Set up the sensor and LED outputs

`TRIG_PIN` is GPIO5 and `ECHO_PIN` is GPIO18.

The ten GPIO numbers from 017 are stored in `led_pins`, then converted into output `Pin` objects and stored in `leds`.

Every LED starts OFF.

### 2. Take one ultrasonic reading

`single_distance_cm()` sends the short trigger pulse required by the HC-SR04.

`time_pulse_us()` measures how long the ECHO signal stays HIGH.

That time is converted into centimetres:

```python
distance_cm = (duration * 0.0343) / 2
```

Readings below 2 cm or above 150 cm are ignored for this module.

### 3. Filter the reading

`filtered_distance_cm()` takes five readings.

Valid readings are sorted and the middle reading is used.

This helps reject an occasional random jump instead of allowing one bad reading to immediately change the LED bar.

### 4. Convert distance into LED count

`distance_to_led_count()` turns distance into a value from 0 to 10.

The closer the object is, the more LEDs are shown.

Each 10 cm distance band removes another LED. Readings above 100 cm show zero LEDs.

### 5. Update the bar

`show_bar()` walks through all ten LED outputs.

LEDs below the requested count are switched ON and the rest are switched OFF.

The main loop repeats the process continuously:

```text
measure -> filter -> convert -> display
```

---

## Test

1. Run the code in MicroPython.
2. Confirm the serial output begins printing distance readings.
3. Put an object in front of the HC-SR04.
4. Move the object closer to the sensor.
5. Confirm more LED segments light.
6. Move the object farther away.
7. Confirm fewer LED segments light.
8. Move through several distances and check that the response is repeatable.
9. Move beyond about 100 cm and confirm the bar goes out.

If distance readings work but the bar does not, check the LED circuit from **017**.

If the LED bar works but does not react to distance, check the ultrasonic circuit from **016**.

---

## Definition of done

018 is complete when:

- the ESP32 boots normally
- the HC-SR04 returns usable distance readings
- GPIO18 is protected by the 1 kΩ / 2 kΩ ECHO divider
- all ten LED segments can be controlled
- closer objects produce more lit segments
- farther objects produce fewer lit segments
- readings above 100 cm produce an empty bar
- the response remains stable during repeated movement tests

---

## What this enables next

018 joins a sensor input and a multi-output display into one small working system.

The same pattern can later be used for:

- proximity displays
- obstacle indication
- warning zones
- threshold-based behaviour
- sensor-driven control logic

The important progression is:

```text
input -> measurement -> filtering -> decision -> output
```

That pattern is reusable far beyond this one ultrasonic sensor and LED bar.