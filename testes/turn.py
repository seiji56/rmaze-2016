import herkulex
import time
import sys

herkulex.connect("/dev/ttyAMA0", 115200)

FR  = herkulex.servo(0xfd)
FL  = herkulex.servo(16)
BR  = herkulex.servo(10)
BL  = herkulex.servo(20)
ALL = herkulex.servo(0xfe)

power = 1000
rtime = 1
if len(sys.argv) > 1:
    rtime *= sys.argv[1]

ALL.torque_on()

FR.set_servo_speed(power, 0x06)
FL.set_servo_speed(power, 0x06)
BR.set_servo_speed(power, 0x06)
BL.set_servo_speed(power, 0x06)

time.sleep(rtime)

ALL.set_servo_speed(1, 0x06)
ALL.set_led(0x06)
