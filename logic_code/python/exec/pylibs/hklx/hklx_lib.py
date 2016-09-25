import time
import herkulex

print("Loading herkulex lib...")

adddef = [0xfd, 0x0A, 0x14, 0x10]
calib  = [0, 0, 0, 0]

herkulex.connect("/dev/ttyAMA0", 115200)

hklx = []

for addr in range(4):
    hklx += [herkulex.servo(adddef[addr])]

hklx += [herkulex.servo(0xfe)]
hklx[4].torque_on()

walkt = 3.08 
def walk(tiles, pwr, stop_on_sensor=False):
    clearerr()
    pwr *= tiles/abs(tiles)
    hklx[0].set_servo_speed(-pwr+calib[0], 0x06)
    hklx[1].set_servo_speed(-pwr+calib[1], 0x06)
    hklx[2].set_servo_speed(pwr+calib[2], 0x06)
    hklx[3].set_servo_speed(pwr+calib[3], 0x06)
    
    time.sleep(walkt*tiles)

    hklx[4].set_servo_speed(1, 0x06)

turnt = 1
def turn(times, pwr):
    clearerr()
    pwr *= tiles/abs(tiles)
    tiles = abs(tiles)
    hklx[0].set_servo_speed(pwr+calib[0], 0x06)
    hklx[1].set_servo_speed(pwr+calib[1], 0x06)
    hklx[2].set_servo_speed(pwr+calib[2], 0x06)
    hklx[3].set_servo_speed(pwr+calib[3], 0x06)
    
    time.sleep(turnt*times)

    hklx[4].set_servo_speed(1, 0x06)

latt = 1.74
def lateral(tiles, pwr):
    clearerr()
    pwr *= tiles/abs(tiles)
    tiles = abs(tiles)
    hklx[0].set_servo_speed(-pwr+calib[0], 0x06)
    hklx[1].set_servo_speed(pwr+calib[1], 0x06)
    hklx[2].set_servo_speed(pwr+calib[2], 0x06)
    hklx[3].set_servo_speed(-pwr+calib[3], 0x06)
    
    time.sleep(latt*tiles)

    hklx[4].set_servo_speed(1, 0x06)

def clearerr():
    herkulex.clear_errors()
    hklx[4].set_led(0x06)
