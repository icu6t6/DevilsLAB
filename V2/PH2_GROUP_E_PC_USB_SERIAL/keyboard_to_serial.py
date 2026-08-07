from pynput import keyboard
import serial
import time

# CHANGE THIS to your actual port
PORT = "COM7"     # e.g. COM5 / COM7
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=0)
time.sleep(1)
print("Serial open on", PORT)

MOVE_KEYS = {
    keyboard.KeyCode.from_char('w'): b'W',
    keyboard.KeyCode.from_char('a'): b'A',
    keyboard.KeyCode.from_char('s'): b'S',
    keyboard.KeyCode.from_char('d'): b'D',
}

def send(cmd):
    ser.write(cmd)
    # optional: print for visibility
    print("SEND:", cmd)

def on_press(key):
    if key in MOVE_KEYS:
        send(MOVE_KEYS[key])
    elif key == keyboard.Key.space:
        send(b'X')

def on_release(key):
    if key in MOVE_KEYS or key == keyboard.Key.space:
        send(b'X')
    if key == keyboard.Key.esc:
        print("Exiting.")
        ser.close()
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
