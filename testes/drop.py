import herkulex
import time

herkulex.connect("/dev/ttyAMA0", 115200)

DROP  = herkulex.servo(50)

ALL = herkulex.servo(0xfe)

#power = 1000
power = 1000

init_a = -512
end_a = 512
ALL.torque_on()

DROP.set_servo_angle(0, 1, 0x08)
time.sleep(1)
DROP.set_servo_angle(-95, 1, 0x08)
time.sleep(1)
DROP.set_servo_speed(1, 0x06)
ALL.set_led(0x06)
