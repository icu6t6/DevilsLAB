# 011 – LCD Hello

## What this does
Brings up a 1602 I2C LCD and writes simple text to both display lines.

## What this teaches
- I2C wiring
- scanning for an I2C device address
- initialising a 1602 LCD over I2C
- writing text to the display
- understanding why powered LCDs can show solid blocks before code runs

## Parts
- ESP32 dev board
- 1602 I2C LCD
- jumper wires
- breadboard

## Wiring

### LCD → ESP32
- GND → GND
- VDD / VCC → VIN
- SDA → GPIO21
- SCL → GPIO22

## Wiring Diagram

![011 – LCD Hello](../../images/011_1602_I2C_LCD_AND_%20KEYPAD.png)

## I2C Address Check
Before running the LCD text script, scan for the display address.

```python
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

print("I2C scan:", i2c.scan())
```

## What we want
It should print a device address list, usually one address.

Examples:

```text
I2C scan: [39]
I2C scan: [63]
```

If you get an empty list:
- SDA and SCL may be swapped
- there may be a bad connection
- the backpack may not be responding
- the LCD power may be wrong

## Notes
A row of solid blocks usually means:
- the LCD has power
- the contrast is high enough to show characters
- but the display has not yet been properly initialised by code

That is usually a good sign, not a disaster.

In this build, the LCD address was:

```text
39 (0x27)
```

## Code

```python
from machine import Pin, I2C
from time import sleep_ms, sleep

I2C_ADDR = 0x27
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

def lcd_write(bits, mode):
    high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
    i2c.writeto(I2C_ADDR, bytes([high]))
    lcd_toggle_enable(high)
    i2c.writeto(I2C_ADDR, bytes([low]))
    lcd_toggle_enable(low)

def lcd_toggle_enable(bits):
    sleep_ms(1)
    i2c.writeto(I2C_ADDR, bytes([bits | ENABLE]))
    sleep_ms(1)
    i2c.writeto(I2C_ADDR, bytes([bits & ~ENABLE]))
    sleep_ms(1)

def lcd_init():
    lcd_write(0x33, LCD_CMD)
    lcd_write(0x32, LCD_CMD)
    lcd_write(0x06, LCD_CMD)
    lcd_write(0x0C, LCD_CMD)
    lcd_write(0x28, LCD_CMD)
    lcd_write(0x01, LCD_CMD)
    sleep_ms(5)

def lcd_string(message, line):
    message = str(message)
    message = message + (" " * (LCD_WIDTH - len(message)))
    message = message[:LCD_WIDTH]
    lcd_write(line, LCD_CMD)
    for char in message:
        lcd_write(ord(char), LCD_CHR)

lcd_init()
lcd_string("ENZO LABS", LCD_LINE_1)
lcd_string("LCD OK", LCD_LINE_2)

while True:
    sleep(1)
```

## Code Explanation
### 1. I2C setup
The ESP32 creates an I2C connection using:
- GPIO21 for SDA
- GPIO22 for SCL

The LCD address used here is `0x27`, which matches the scanned I2C address of `39`.

### 2. LCD control values
The script defines:
- LCD width = 16 characters
- command mode
- character mode
- line 1 address
- line 2 address
- backlight control
- enable pulse control

These values are used to send the correct instructions to the display.

### 3. `lcd_write(bits, mode)`
This function sends data to the LCD.

The LCD runs in 4-bit mode, so each byte is split into:
- upper 4 bits
- lower 4 bits

Each half is sent over I2C with the backlight enabled.

### 4. `lcd_toggle_enable(bits)`
This pulses the LCD enable line.

The LCD needs a short enable pulse to accept each command or character.

### 5. `lcd_init()`
This sets the LCD into the correct operating mode.

It:
- initialises 4-bit mode
- turns the display on
- sets entry mode
- clears the display

Without this step, the LCD may only show solid blocks.

### 6. `lcd_string(message, line)`
This writes text to one line of the LCD.

It:
- converts the message to a string
- pads or trims it to 16 characters
- selects the target line
- writes each character one by one

### 7. Final display output
After initialisation, the script writes:
- line 1: `ENZO LABS`
- line 2: `LCD OK`

The loop at the end keeps the script running so the display stays stable.

## Test
- wire the LCD as shown
- run the I2C scan
- confirm the LCD address appears
- run the main LCD script
- confirm the display shows:
  - `ENZO LABS`
  - `LCD OK`

## What this enables next
- keypad + LCD entry display
- keypad + LCD password lock
- ultrasonic + LCD distance display
