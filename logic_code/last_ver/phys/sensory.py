import time
import os
import Adafruit_ADS1x15

milli_time = lambda: int(round(time.time() * 1000))

adcf = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
adcl = Adafruit_ADS1x15.ADS1015(address=0x4a, busnum=1)
adcr = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
adcb = Adafruit_ADS1x15.ADS1015(address=0x4b, busnum=1)

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
    return (distrf() + 0*distrm() + distrl())/2

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
