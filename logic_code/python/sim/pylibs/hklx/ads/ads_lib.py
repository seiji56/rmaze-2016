import Adafruit_ADS1x15

print("Loading ads lib...")

adddef = [[0x49, 1, 2, 0],
        [0x48, 2, 1, 0],
        [0x4B, 0, 1, 2],
        [0x4A, 0, 2, 1]]

ads = []
for i in range(4):
    ads += [Adafruit_ADS1x15.ADS1015(address=adddef[i][0], busnum=1)]
    try:
        ads[-1].read_adc(0, gain=1)
    except IOError:
        print("Error initializing lib. ADS " + hex(adddef[i][0]) + " is not reachable")
        exit(-1)

def getval(side, it, mul=1):
    values = [0]*4

    try:
        for i in range(it):
            for k in range(4):
                values[k] = ads[side].read_adc(k, gain=1)
        for k in range(4):
            values[k] /= it
            values[k] *= mul
    except IOError:
        print("Tried and could not read ADS at " + hex(address))
        return 0

    return values

def getvolt(side, it):
    return getval(side, it, 0.002)

