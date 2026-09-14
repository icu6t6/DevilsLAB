# ENZO V1 Firmware (Canonical)

This directory is the public Free V1 firmware source for the Waveshare ESP32-S3-DEV-KIT-N8R8. Its entry-point version is `0.1.0`.

Follow [Software Setup](../../../docs/SOFTWARE_SETUP_T1_ENZO_v1_USER.md) for the required ESP layout: root `main.py`, the normal `/app` files, and an empty `/actuators` package. Do not copy this source directory blindly as the ESP filesystem root.

`CURRENT_ESP_FIRMWARE/` and `V2/` contain later sources. `pins.py` and `selftest.py` are optional legacy reference/diagnostic files; normal V1 boot does not import them. No OLED, DHT, diagnostics UI or autonomy is required for Free V1.

Start with [Start Here](../../../docs/README_START_HERE_T1_ENZO_v1-2.md). The [root licence](../../../LICENSE) states the V1 non-commercial permissions and exact scope.
