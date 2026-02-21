
## 1) Install tools
- Install **Thonny IDE**
- Download **MicroPython firmware** for ESP32-S3

## 2) Flash MicroPython (via Thonny)
1. Plug ESP in by USB
2. Thonny → Tools → Options → Interpreter
3. Select “MicroPython (ESP32)” and the correct COM port
4. Click “Install or update MicroPython”
5. Select the ESP32-S3 firmware file and flash

## 3) If Thonny won’t connect (common)
Reliable sequence:
1. Close Thonny
2. Unplug ESP
3. Open Thonny and wait
4. Plug ESP back in
5. Pick COM port again

Also try:
- Another USB cable
- Another USB port

## 4) Upload project files to the ESP
In Thonny:
- View → Files
- Copy files from “This computer” to “MicroPython device”
- Ensure file names match exactly

### File Structure Setup (Required)
After flashing MicroPython, you must manually place the ENZO project files onto the device.

Copy `main.py` from the ENZO v1 files to the **root** of the MicroPython device, alongside the existing `boot.py`.

Create the following folders on the device if they do not already exist:

/app
/actuators

The `app/` folder must contain:

app/
├── config.py
├── eyes.py
├── leds.py
├── net.py
├── state.py
├── status.py
├── tasks.py
└── __init__.py

The `actuators/` folder must contain:

actuators/
└── __init__.py

**File and folder names must match exactly.**
Missing folders or misplaced files will prevent the firmware from running correctly.

## 5) Run and reboot
- Run `main.py` (or press **Run**)
- Soft reboot: **Ctrl-D**

## Post-Setup Expectations
After copying the files and rebooting the device, ENZO should start automatically via `main.py`.

On successful startup, you should observe:
- The ESP32 runs without import errors
- The heartbeat/status LEDs behave as defined
- The NeoPixel “eyes” perform their startup animation
- The system enters a stable idle state without crashing or rebooting

If ENZO does not start:
- Confirm `main.py` is in the root
- Confirm `app/` and `actuators/` folders exist
- Confirm all filenames match exactly

Do not proceed to hardware power integration until this software-only startup behaves as expected.

## 6) Optional — Run the ENZO Self-Test (Recommended)

ENZO includes a built-in self-test module to verify wiring correctness before relying on normal behaviour.

### What the self-test checks
- Heartbeat LED
- WiFi LED
- Eye button
- WiFi button
- PIR motion sensor
- LDR (ADC input)

### What this helps catch
- Miswired pins
- Missing components
- Incorrect pull-ups or pull-downs

### When to run the self-test
- After the software boots successfully
- After completing Module Group A wiring
- Before troubleshooting unexpected behaviour
- Any time hardware wiring has been changed

### How to run the self-test
1. Power ENZO normally
2. Open the MicroPython REPL (via Thonny or serial)
3. At the `>>>` prompt, enter:

```python
import app.selftest as st
st.run()
```

### Interpreting results
Each check prints either:
- `[PASS] <description>`
- `[FAIL] <description>`

At the end:
- **SELF-TEST RESULT: PASS** — all tested hardware is responding correctly
- **SELF-TEST RESULT: FAIL** — one or more peripherals are missing or miswired

If a test fails:
- Recheck wiring against the Pin Truth Map
- Correct the issue
- Run the self-test again

The self-test does not modify system state and is safe to run multiple times.
