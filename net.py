# app/net.py
import network
import time

_wlan = None


def status():
    global _wlan
    if _wlan is None:
        _wlan = network.WLAN(network.STA_IF)

    active = _wlan.active()
    connected = _wlan.isconnected()
    cfg = _wlan.ifconfig() if connected else None
    return active, connected, cfg

def off():
    global _wlan
    if _wlan is None:
        _wlan = network.WLAN(network.STA_IF)
    try:
        if _wlan.isconnected():
            _wlan.disconnect()
    except:
        pass
    _wlan.active(False)
    return True


def connect(ssid, password, timeout_ms=10000):
    global _wlan

    if _wlan is None:
        _wlan = network.WLAN(network.STA_IF)

    if not _wlan.active():
        _wlan.active(True)

    if _wlan.isconnected():
        print("WiFi already connected")
        return True

    print("Connecting to WiFi:", ssid)
    _wlan.connect(ssid, password)

    start = time.ticks_ms()
    while not _wlan.isconnected():
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            raise RuntimeError("WiFi connection timeout")
        time.sleep_ms(200)

    print("WiFi connected:", _wlan.ifconfig())
    return True


def disconnect():
    global _wlan
    if _wlan:
        _wlan.disconnect()
        print("WiFi disconnected")

