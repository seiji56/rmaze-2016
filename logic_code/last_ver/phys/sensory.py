import time
import os
import math
import Adafruit_ADS1x15
import adxl345
import RPi.GPIO as gpio

milli_time = lambda: int(round(time.time() * 1000))

adcf = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
adcl = Adafruit_ADS1x15.ADS1015(address=0x4a, busnum=1)
adcr = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
adcb = Adafruit_ADS1x15.ADS1015(address=0x4b, busnum=1)

accel = adxl345.ADXL345()

GAIN = 1

def distfr():
    return adcf.read_adc(0, gain=GAIN)

def distfm():
    return adcf.read_adc(2, gain=GAIN)

def distfl():
    return adcf.read_adc(1, gain=GAIN)


def distrf():
    return adcr.read_adc(2, gain=GAIN)

def distrm():
    return adcr.read_adc(1, gain=GAIN)

def distrb():
    return adcr.read_adc(0, gain=GAIN)


def distbr():
    return adcb.read_adc(0, gain=GAIN)

def distbm():
    return adcb.read_adc(0, gain=GAIN)

def distbl():
    return adcb.read_adc(0, gain=GAIN)


def distlf():
    return adcl.read_adc(1, gain=GAIN)

def distlm():
    return adcl.read_adc(2, gain=GAIN)

def distlb():
    return adcl.read_adc(0, gain=GAIN)


def distf():
    return (distfr() + 0*distfm() + distfl())/2

def distr():
    return (distrf() + 0*distrm() + distrb())/2

def distb():
    return (distbr() + 0*distbm() + distbl())/2

def distl():
    return (distlf() + 0*distlm() + distlb())/2


def wfr(sth):
    return distfr() > sth

def wfl(sth):
    return distfl() > sth


def wrf(sth):
    return distrf() > sth

def wrb(sth):
    return distrb() > sth


def wbr(sth):
    return distbr() > sth

def wbl(sth):
    return distbl() > sth


def wlf(sth):
    return distlf() > sth

def wlb(sth):
    return distlb() > sth

def wf(sth):
    return (distfr() + distfl())/2 > sth

def wl(sth):
    return (distlf() + distlb())/2 > sth

def wb(sth):
    return (distbr() + distbl())/2 > sth

def wr(sth):
    return (distrf() + distrb())/2 > sth

def color(sth):
    return False

base_all = 800
maxerr = 150
def shouldAlign(sth):
    if abs(latcorr(sth)) > maxerr:
        return True
    if abs(vertcorr(sth)) > maxerr:
        return True
    if abs(angcorr(sth)) > maxerr:
        return True
    return False

def latcorr(sth):
    corr = 0
    cnt = 0
    if wl(sth):
        corr += distl() - base_all
        cnt += 1
    if wr(sth):
        corr += base_all - distr()
        cnt += 1
    if cnt > 0:
        corr /= cnt
    if corr < -500:
        corr = -500
    elif corr > 500:
        corr = 500
    return corr

def vertcorr(sth):
    corr = 0
    cnt = 0
    if wb(sth):
        corr += distb() - base_all
        cnt += 1
    if wf(sth):
        corr += base_all - distf()
        cnt += 1
    if cnt > 0:
        corr /= cnt
    if corr < -500:
        corr = -500
    elif corr > 500:
        corr = 500
    return corr


def angcorr(sth):
    corr = 0
    cnt = 0
    if wl(sth):
        corr += distlf() - distlb()
        cnt += 1
    if wr(sth):
        corr += distrb() - distrf()
        cnt += 1
    if wf(sth):
        corr += distfr() - distfl()
        cnt += 1
    if wb(sth):
        corr += distbl() - distbr()
        cnt += 1
    if cnt > 0:
        corr /= cnt
    if corr < -500:
        corr = -500
    elif corr > 500:
        corr = 500
    return corr

maxrdeg = 10
def isramp():
    axes = accel.getAxes(True)
    modv = math.sqrt(axes['x']**2 + axes['y']**2 + axes['z']**2)
    dot = (-axes['z'])/modv
    maxrad = maxdeg*math.pi/180
    return math.acos(dot) > maxrad

gpio.setmode(gpio.BCM)

gpio.setup(27, gpio.IN)
gpio.setup(22, gpio.IN)
gpio.setup(9, gpio.IN)
gpio.setup(10, gpio.OUT)
gpio.setup(11, gpio.OUT)

gpio.output(10, gpio.LOW)

def hasvictim():
    gpio.output(11, gpio.HIGH)
    ret = -1
    if gpio.input(27):
        ret = 1
    elif gpio.input(22):
        ret = 0
    elif gpio.input(9):
        ret = 9
    return ret
