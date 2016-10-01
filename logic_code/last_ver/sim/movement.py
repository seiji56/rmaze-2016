import herkulex
import time
import sensory as sn

herkulex.connect("/dev/ttyAMA0", 115200)

FR  = herkulex.servo(0xfd)
FL  = herkulex.servo(16)
BR  = herkulex.servo(10)
BL  = herkulex.servo(20)
ALL = herkulex.servo(0xfe)

ALL.torque_on()

walkpow = 1000
walktime = 1.54
sensordfront = 0
sensordback = 0
walkcalib = -50
def walkf(move, dst_sth = 400, col_sth = 500, scstop = False):
    FR.set_servo_speed(-walkpow, 0x06)
    FL.set_servo_speed(walkpow + walkcalib, 0x06)
    BR.set_servo_speed(-walkpow, 0x06)
    BL.set_servo_speed(walkpow + walkcalib, 0x06)
    
    if scstop:
        tmp = 0#sn.wlf(dst_sth);
    else:
        time.sleep(walktime*move[1])

    ALL.set_servo_speed(1, 0x06)
    ALL.set_led(0x06)
    return move

rotpow = 1000
rottime = 1 # per 90 dg
def turnr(move):
    FR.set_servo_speed(rotpow, 0x06)
    FL.set_servo_speed(rotpow, 0x06)
    BR.set_servo_speed(rotpow, 0x06)
    BL.set_servo_speed(rotpow, 0x06)

    time.sleep(rottime*move[1])

    ALL.set_servo_speed(1, 0x06)
    ALL.set_led(0x06)
    return move

def turnl(move):
    FR.set_servo_speed(-rotpow, 0x06)
    FL.set_servo_speed(-rotpow, 0x06)
    BR.set_servo_speed(-rotpow, 0x06)
    BL.set_servo_speed(-rotpow, 0x06)

    time.sleep(rottime*move[1])

    ALL.set_servo_speed(1, 0x06)
    ALL.set_led(0x06)
    return move
