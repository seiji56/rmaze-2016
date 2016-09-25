
import herkulex
import time

herkulex.connect("/dev/ttyAMA0", 115200)

FR  = herkulex.servo(0xfd)
FL  = herkulex.servo(16)
BR  = herkulex.servo(10)
BL  = herkulex.servo(20)
ALL = herkulex.servo(0xfe)

power = 1000
#rtime = 3.08
rtime = 20
calib = -50

ALL.torque_on()

ALL.set_servo_speed(1, 0x03)
ALL.set_led(0x06)
