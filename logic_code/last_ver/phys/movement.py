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

def align(tout = 1):
    start = time.time()
    while time.time() - start < tout:
        setPow([0, 0, 0, 0], sn.latcorr(), sn.angcorr())
    stop()

def stop():
    ALL.set_servo_speed(1, 0x06)
    ALL.set_led(0x06)

def setPow(pots, latcorr = 0, angcorr = 0):
    FR.set_servo_speed(pots[0] + latcorr + angcorr, 0x06)
    FL.set_servo_speed(pots[1] + latcorr + angcorr, 0x06)
    BR.set_servo_speed(pots[2] - latcorr + angcorr, 0x06)
    BL.set_servo_speed(pots[3] - latcorr + angcorr, 0x06)
    ALL.set_led(0x06)

walkpow = 1000
walktime = 1.54
sensordfront = 0
sensordback = 0
walkcalib = -50
expft = .5
def walkf(move, dst_sth = 400, col_sth = 500, scstop = False, scuse = False):
    start = time.time()
    basepow = [-walkpow, walkpow + walkcalib,
            -walkpow, walkpow + walkcalib]
    setPow(basepow, sn.latcorr(), sn.angcorr())
    
    if scstop and scuse:
        wallstate = [sn.wl(dst_sth), sn.wr(dst_sth)] #l, r
        tmpws = [sn.wl(dst_sth), sn.wr(dst_sth)]
        t_start = start
        t_curr = 0
        while t_curr < move[1] and sn.wl(dst_sth) == wallstate[0] and not sn.wf(
                dst_sth) and sn.wl(dst_sth) == wallstate[2] and sn.color(col_sth
                        ):
            while time.time() - t_start < walktime:
                setPow(basepow, sn.latcorr(), sn.angcorr())
                sm = 0
                cnt = 0
                if sn.wlf() != tmpws[0]:
                    sm += time.time() - expft
                    tmpws[0] = sn.wlf()
                if sn.wrf() != tmpws[1]:
                    sm += time.time() - expft
                    tmpws[1] = sn.wrf()
                if cnt > 0:
                    t_start = sm/cnt
            t_curr += 1
    elif scstop:
        wallstate = [sn.wl(dst_sth), sn.wr(dst_sth)] #l, r
        t_curr = 0
        while t_curr < move[1] and sn.wl(dst_sth) == wallstate[0] and not sn.wf(
                dst_sth) and sn.wl(dst_sth) == wallstate[2] and sn.color(col_sth
                        ):
            while time.time() - t_start < walktime:
                setPow(basepow, sn.latcorr(), sn.angcorr())
            t_curr += 1
    elif scuse:
        tmpws = [sn.wl(dst_sth), sn.wr(dst_sth)]
        t_curr = 0
        while t_curr < move[1] and not sn.wf(dst_sth) and not sn.color(col_sth):
            while time.time() - t_start < walktime:
                setPow(basepow, sn.latcorr(), sn.angcorr())
                sm = 0
                cnt = 0
                if sn.wlf() != tmpws[0]:
                    sm += time.time() - expft
                    tmpws[0] = sn.wlf()
                if sn.wrf() != tmpws[1]:
                    sm += time.time() - expft
                    tmpws[1] = sn.wrf()
                if cnt > 0:
                    t_start = sm/cnt
            t_curr += 1

    else:
        t_curr = 0
        while t_curr < move[1] and not sn.wf(dst_sth) and sn.color(col_sth):
            while time.time() - t_start < walktime:
                setPow(basepow, sn.latcorr(), sn.angcorr())
            t_curr += 1

    stop()
    return move

rotpow = 1000
rottime = 1 # per 90 dg
def turnr(move):
    basepow = [rotpow for i in range(4)]
    setPow(basepow, 0, 0)

    time.sleep(rottime*move[1])

    stop()
    return move

def turnl(move):
    basepow = [-rotpow for i in range(4)]
    setPow(basepow, 0, 0)

    time.sleep(rottime*move[1])

    stop()
    return move
