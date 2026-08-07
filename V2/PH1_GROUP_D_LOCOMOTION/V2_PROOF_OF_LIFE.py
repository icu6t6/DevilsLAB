from machine import Pin, I2C
import time
#Note:This proof-of-life script is a bring-up and validation tool only.
#It is run manually to confirm locomotion hardware and control paths, then removed.
#It does not persist, replace baseline firmware, or remain active during normal ENZO operation.
# I2C setup (V2 canonical)
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)
ADDR = 0x14

# Motor IDs (locked)
MOTOR_A = 0   # Left track
MOTOR_B = 1   # Right track

# Command bytes (from driver behaviour we confirmed)
CMD_RUN_CW   = 0x02
CMD_STOP     = 0x01

def send(cmd, motor, speed=0):
    i2c.writeto(ADDR, bytes([cmd, motor, speed]))

print("V2 proof-of-life: START")

# Run both tracks forward
send(CMD_RUN_CW, MOTOR_A, 200)
send(CMD_RUN_CW, MOTOR_B, 200)

time.sleep(2)

# Stop both tracks
send(CMD_STOP, MOTOR_A)
send(CMD_STOP, MOTOR_B)

print("V2 proof-of-life: STOP")
