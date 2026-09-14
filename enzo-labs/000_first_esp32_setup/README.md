# 000 – First ESP32 Setup (Never Used One Before)

If this is your first ESP32, start here before Module 001.

This guide gets the ENZO-Labs board from **fresh out of the packet** to a working MicroPython prompt in Thonny. You do not need to know Python, serial ports or firmware flashing first.

---

## What you need

- ESP32 development board
- USB cable that supports **data**, not charge-only
- Windows, macOS or Linux computer
- internet connection for the first setup
- Thonny Python IDE

ENZO-Labs was built around this common board style:

- ESP32 dev board
- ESP-WROOM-32 module
- 30-pin layout
- CP2102 USB-to-serial interface

[View the ENZO-Labs example board](../../images/ESP32DevBoard.jpg)

If your board says ESP32-S3, ESP32-C3, ESP32-C6 or something else, stop and check its exact firmware and pin layout before following the wiring in later modules.

---

## What the software is

### Thonny

Thonny is the program on your computer where you will write, run and save Python code.

Download it from:

https://thonny.org/

### MicroPython

MicroPython is the small Python system that runs **on the ESP32 itself**.

The board must have suitable MicroPython firmware installed before ENZO-Labs code can run.

Official ESP32/WROOM firmware page:

https://micropython.org/download/ESP32_GENERIC/

For a normal ESP-WROOM-32 board like the ENZO-Labs example, use the **generic ESP32 / WROOM stable Release firmware**. Do not choose a Preview build for your first setup.

---

## Step 1 – Install Thonny

1. Download Thonny from `thonny.org`.
2. Install it normally.
3. Open Thonny.

You should see:

- an editor area at the top
- a **Shell** area at the bottom

The Shell is where the ESP32 can talk back to you.

---

## Step 2 – Connect the ESP32

1. Plug the ESP32 into the computer with the USB cable.
2. Wait a few seconds.
3. In Thonny, open **Run → Select interpreter**.
4. Choose **MicroPython (ESP32)**.
5. Select the serial/COM port belonging to the ESP32.

On Windows it will usually look like:

`COM3`, `COM4`, `COM5`, etc.

If only one ESP32 is connected, automatic port detection may also work.

### No port appears?

First try a different USB cable. Charge-only cables are extremely common and can power the board while carrying no data.

If Windows still does not detect the ENZO-Labs CP2102 board, install the Silicon Labs **CP210x USB-to-UART VCP driver**, then reconnect the board.

---

## Step 3 – Install MicroPython if needed

If the Shell already gives you a MicroPython prompt like:

```text
>>>
```

then MicroPython may already be installed. Continue to Step 4.

If not, use Thonny's MicroPython firmware installer from the interpreter/backend setup screen.

For the ENZO-Labs ESP-WROOM-32 style board:

- target: **ESP32 / WROOM / generic ESP32**
- firmware: **stable Release**
- erase the board first when the installer offers that option

The official MicroPython generic firmware target is `ESP32_GENERIC`.

Do **not** choose ESP32-S3, ESP32-C3 or another chip family just because the name looks newer. The firmware must match the chip on the board.

When flashing finishes, reconnect/select the ESP32 interpreter if Thonny asks you to.

---

## Step 4 – If flashing will not start

Many boards enter the bootloader automatically. If yours does not, try this:

1. Hold the button marked **BOOT** or **IO0**.
2. Press and release **EN**, **RESET** or **RST**.
3. Release **BOOT**.
4. Start the firmware install again.

You usually only need this when firmware flashing cannot connect to the board.

---

## Step 5 – Prove the board is talking to Thonny

When the board is connected correctly, the Thonny Shell should show the MicroPython prompt:

```text
>>>
```

Click in the Shell and type:

```python
print("ENZO-Labs ESP32 ready")
```

Press Enter.

You should see:

```text
ENZO-Labs ESP32 ready
```

Now type:

```python
import sys
print(sys.implementation)
```

You should get MicroPython information back from the board.

At this point the computer, USB connection, serial link, Thonny and MicroPython are all working together.

---

## Step 6 – Run your first script

In the main Thonny editor, enter:

```python
import time

print("ESP32 setup passed")

for count in range(1, 6):
    print("count", count)
    time.sleep(1)

print("done")
```

Press **F5** or choose **Run → Run current script**.

The Shell should count from 1 to 5 and finish with:

```text
done
```

That is enough for setup. You do not need to wire anything yet.

---

## Computer file vs ESP32 file

Thonny can save files in two different places:

- **This computer** – your normal copy on the PC
- **MicroPython device** – the ESP32's internal flash storage

For learning, keep a copy of your work on the computer.

A file named `main.py` saved on the ESP32 runs automatically when the board starts. Do not save random experiments as `main.py` unless a module specifically tells you to.

---

## Useful controls when something gets stuck

- **Ctrl+C** – stop a running MicroPython program
- **Ctrl+D** – soft reboot the MicroPython board from the REPL
- unplug/replug USB – simple hard reconnect
- **BOOT + RESET/EN** sequence – use when flashing cannot enter the bootloader

If Thonny says the port is busy, close any other serial terminal or program that may already be connected to the ESP32.

---

## Common first-time problems

### Board powers up but Thonny cannot see it

Most likely causes:

- charge-only USB cable
- wrong COM/serial port selected
- CP2102 driver missing
- another program already using the port

### Firmware install fails part-way through

Try:

- another USB cable or USB port
- the BOOT + RESET/EN sequence above
- closing other serial programs
- retrying at a slower flashing speed if the installer offers one

### Shell shows no `>>>`

Try:

1. click the Shell
2. press `Ctrl+C`
3. press `Ctrl+D`
4. reconnect the interpreter if necessary

### Code runs but later hardware does nothing

That is no longer a basic board-setup problem. Check the module wiring, GPIO numbers, component orientation and resistor values for the lesson you are building.

---

## Definition of done

You are ready for Module 001 when all of these are true:

- ESP32 appears as a serial/COM device
- Thonny is using **MicroPython (ESP32)**
- the board has suitable ESP32/WROOM MicroPython firmware
- the Shell shows `>>>`
- `print("ENZO-Labs ESP32 ready")` works
- the 1-to-5 test script runs without errors

Once those pass, continue to:

[001 – RGB LED (3 Channel Output)](../001_rgb_led/README.md)

---

## Official references

- Thonny: https://thonny.org/
- Thonny MicroPython support: https://github.com/thonny/thonny/wiki/MicroPython
- MicroPython ESP32/WROOM firmware: https://micropython.org/download/ESP32_GENERIC/
- MicroPython ESP32 getting started: https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
