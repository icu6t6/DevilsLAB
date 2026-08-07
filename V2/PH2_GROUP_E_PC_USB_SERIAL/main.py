# main.py — V2 Phase 2: USB Serial WASD drive (deterministic) + reverse
# PC -> USB serial -> ESP -> I2C motor driver
#
# Keys:
#   W = forward
#   S = reverse
#   A = left turn
#   D = right turn
#   X or Space = stop
#
# Safety:
#   - If no RX for FAILSAFE_MS: STOP

from machine import Pin, I2C
import sys, select, time

# ----------------------------
# Motor driver (V2 proof-of-life)
# ----------------------------
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)
ADDR = 0x14

MOTOR_LEFT = 0   # Motor A
MOTOR_RIGHT = 1  # Motor B

CMD_STOP = 0x01
CMD_RUN_CW = 0x02
CMD_RUN_CCW = 0x03

SPEED = 200

# Direction mapping used by the tested ENZO build.
# If forward/reverse are physically inverted on your build, swap these two.
FWD_CMD = CMD_RUN_CCW
REV_CMD = CMD_RUN_CW


def send(cmd, motor, speed=0):
    i2c.writeto(ADDR, bytes([cmd, motor, speed]))


def stop_all():
    send(CMD_STOP, MOTOR_LEFT)
    send(CMD_STOP, MOTOR_RIGHT)


def forward():
    send(FWD_CMD, MOTOR_LEFT, SPEED)
    send(FWD_CMD, MOTOR_RIGHT, SPEED)


def reverse():
    send(REV_CMD, MOTOR_LEFT, SPEED)
    send(REV_CMD, MOTOR_RIGHT, SPEED)


def left():
    # Left track stops, right track drives forward.
    send(CMD_STOP, MOTOR_LEFT)
    send(FWD_CMD, MOTOR_RIGHT, SPEED)


def right():
    # Right track stops, left track drives forward.
    send(FWD_CMD, MOTOR_LEFT, SPEED)
    send(CMD_STOP, MOTOR_RIGHT)


# ----------------------------
# Serial RX (stdin)
# ----------------------------
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

FAILSAFE_MS = 250
last_rx = time.ticks_ms()

print("WASD DRIVE READY (W forward, S reverse, X/space stop)")

stop_all()

while True:
    # Deadman stop if comms go quiet.
    if time.ticks_diff(time.ticks_ms(), last_rx) > FAILSAFE_MS:
        stop_all()
        last_rx = time.ticks_ms()

    if poll.poll(0):
        ch = sys.stdin.read(1)
        if ch:
            last_rx = time.ticks_ms()
            c = ch.upper()

            if c == 'W':
                forward()
            elif c == 'S':
                reverse()
            elif c == 'A':
                left()
            elif c == 'D':
                right()
            elif c == 'X' or c == ' ':
                stop_all()

    time.sleep_ms(5)
