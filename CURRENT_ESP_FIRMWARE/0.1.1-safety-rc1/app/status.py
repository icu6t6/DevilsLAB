# app/status.py
state = {
    # Keep both keys: V2 wrote "uptime"; initial file had "uptime_ms"
    "uptime_ms": 0,
    "uptime": 0,

    "loop_count": 0,

    "battery_v": None,
    "battery_pct": None,
    "charging": None,

    "alerts": [],

    # V3 additive status surface
    "wifi_state": "OFF",     # OFF / START / ON / ERR
    "wifi_ip": "-",
    "wifi_err": "",
    "wifi_req_toggle": False,

    "dht_ok": False,
    "temp_c": None,
    "rh": None,

    "i2c_addrs": [],
    "v3_alive": 0,

    # IMU additive status surface
    "imu_ok": False,
    "imu_err": "",
}

