# T1 ENZO V1 — Software Setup

## 1) Install tools

- Install **Thonny IDE**
- Download **MicroPython firmware** for the ESP32-S3

---

## 2) Flash MicroPython with Thonny

1. Plug the ESP32-S3 into the PC by USB.
2. In Thonny open **Tools → Options → Interpreter**.
3. Select **MicroPython (ESP32)** and the correct serial / COM port.
4. Choose **Install or update MicroPython**.
5. Select the ESP32-S3 firmware and flash it.

### If Thonny will not connect

Try this sequence:

1. Close Thonny.
2. Unplug the ESP.
3. Open Thonny and wait for it to finish loading.
4. Plug the ESP back in.
5. Select the correct port again.

Also try another USB cable or USB port if required.

---

## 3) Copy the ENZO V1 firmware to the ESP

The public V1 firmware source is here:

[ENZO V1 firmware files](../material/v1/firmware/)

The repository stores the source files together for easy access. On the ESP, ENZO uses a root `main.py` plus an `/app` package.

### ESP file layout for the normal V1 runtime

```text
/
├── main.py
├── boot.py                  # MicroPython may already provide this
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── eyes_8led.py
│   ├── leds.py
│   ├── net.py
│   ├── state.py
│   ├── status.py
│   └── tasks.py
└── actuators/
    └── __init__.py          # intentionally empty V1 placeholder package
```

Copy the files with **exactly those names**.

Useful source links:

- [`main.py`](../material/v1/firmware/main.py) → ESP root `/main.py`
- [`config.py`](../material/v1/firmware/config.py) → `/app/config.py`
- [`eyes_8led.py`](../material/v1/firmware/eyes_8led.py) → `/app/eyes_8led.py`
- [`leds.py`](../material/v1/firmware/leds.py) → `/app/leds.py`
- [`net.py`](../material/v1/firmware/net.py) → `/app/net.py`
- [`state.py`](../material/v1/firmware/state.py) → `/app/state.py`
- [`status.py`](../material/v1/firmware/status.py) → `/app/status.py`
- [`tasks.py`](../material/v1/firmware/tasks.py) → `/app/tasks.py`
- [`__init__.py`](../material/v1/firmware/__init__.py) → `/app/__init__.py`

Create `/actuators/__init__.py` as an empty file if it is not already present. The package is intentionally empty in the V1 baseline.

### Why `eyes_8led.py` matters

The live V1 `tasks.py` imports:

```python
from app import eyes_8led as eyes
```

The runtime file must therefore be named **`eyes_8led.py`**. Do not rename it to `eyes.py`.

---

## 4) Configure Wi-Fi if you want to use the V1 Wi-Fi button

The public [`config.py`](../material/v1/firmware/config.py) deliberately contains placeholder values:

```python
WIFI_SSID = "yourSSIDhere"
WIFI_PASS = "yourPassworHere"
```

If you want the V1 Wi-Fi button to connect to your network, replace those two values with your own SSID and password **in your private ESP copy** before testing Wi-Fi.

Do not publish your real Wi-Fi password back to a public repository.

If you leave the placeholders unchanged, the rest of V1 can still be tested, but a Wi-Fi connection attempt will fail or time out because no matching network credentials were supplied.

---

## 5) Boot the normal V1 runtime

1. Confirm `main.py` is at the ESP root.
2. Confirm the `/app` files are present with the exact names above.
3. Reset the ESP or press **Ctrl-D** for a soft reboot.

On a normal boot, root `main.py` starts the application by importing:

```python
from app.tasks import run
run()
```

### Expected early behaviour

With the relevant hardware connected, you should see the V1 runtime start without import errors and then observe the normal V1 behaviours such as:

- heartbeat activity
- NeoPixel eye startup / idle behaviour
- button handling
- PIR handling after its warm-up period
- LDR response

Do not move on to robot power integration if the firmware is failing with import errors.

---

## 6) Build Module Group A on USB bench power

Once the firmware is installed, continue to:

[Module Group A — ESP Core Stack](ESP_BUILD_GUIDE_MODULE_GROUP_A.md)

Module A is deliberately built and tested on USB first. Wire and test one section at a time.

Do **not** solder, move wires, or change connections while the ESP is powered.

---

## 7) Optional self-test

The normal V1 runtime does **not** import `selftest.py` or `pins.py` during boot.

If you want to use the optional self-test, also copy:

- [`selftest.py`](../material/v1/firmware/selftest.py) → `/app/selftest.py`
- [`pins.py`](../material/v1/firmware/pins.py) → `/app/pins.py`

Then, from the MicroPython REPL, run:

```python
import app.selftest as st
st.run()
```

Treat this as an additional diagnostic aid, not a replacement for the staged physical checks in Module A.

---

## 8) After Module A

When the ESP stack is working correctly on USB bench power, continue to:

[Module Group B — Power System](MODULE_GROUP_B_POWER_SYSTEM_FINAL_v2.md)

Build and validate the robot power system with the ESP disconnected before integrating the finished Module A stack.

The [Wiring Reference](WIRING_REFERENCES_T1_ENZO_v1_COMBINED.md) is the reference to use during final integration.
