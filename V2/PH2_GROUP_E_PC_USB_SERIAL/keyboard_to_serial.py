from pynput import keyboard
import serial
import time

# CHANGE THIS to your actual ENZO serial port.
PORT = "COM7"     # e.g. COM5 / COM7 on Windows
BAUD = 115200

# Must stay comfortably below FAILSAFE_MS = 250 in the ESP PH2 main.py.
REPEAT_S = 0.12

ser = serial.Serial(PORT, BAUD, timeout=0)
time.sleep(1)
print("Serial open on", PORT)

MOVE_KEYS = {
    keyboard.KeyCode.from_char('w'): b'W',
    keyboard.KeyCode.from_char('a'): b'A',
    keyboard.KeyCode.from_char('s'): b'S',
    keyboard.KeyCode.from_char('d'): b'D',
}

active_cmd = None


def send(cmd):
    ser.write(cmd)
    print("SEND:", cmd)


def on_press(key):
    global active_cmd

    if key in MOVE_KEYS:
        cmd = MOVE_KEYS[key]
        if active_cmd != cmd:
            active_cmd = cmd
            send(cmd)

    elif key == keyboard.Key.space:
        active_cmd = None
        send(b'X')


def on_release(key):
    global active_cmd

    if key in MOVE_KEYS:
        if active_cmd == MOVE_KEYS[key]:
            active_cmd = None
            send(b'X')

    elif key == keyboard.Key.space:
        active_cmd = None
        send(b'X')

    elif key == keyboard.Key.esc:
        active_cmd = None
        send(b'X')
        return False


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

try:
    while listener.running:
        if active_cmd is not None:
            send(active_cmd)
        time.sleep(REPEAT_S)
finally:
    try:
        send(b'X')
    except Exception:
        pass
    ser.close()
    listener.stop()
