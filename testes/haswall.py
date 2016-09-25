import time
import Adafruit_ADS1x15
import sys

addr = 0

def convert( aString ):
    if aString.startswith("0x") or aString.startswith("0X"):
        return int(aString,16)
    elif aString.startswith("0"):
        return int(aString,8)
    else:
        return int(aString)

milli_time = lambda: int(round(time.time() * 1000))

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' <side:0-4>')
    exit(0)

side = convert(sys.argv[1])

sth = [400, 400, 400]
adddef = [[0x49, 1, 2, 0], [0x48, 2, 1, 0], [0x4b, 0, 1, 2], [0x4a, 0, 2, 1]] # Address, left, center, right

adc = Adafruit_ADS1x15.ADS1015(address=adddef[side][0], busnum=1)

GAIN = 1
#print('-' * 46)

while True:
    values = [0]*3
    ltime = milli_time()
    try:
        k = 0
        for i in adddef[side][1:]:
            values[k] += adc.read_adc(i, gain=GAIN)
            k+=1
    except IOError:
        print('Could not read sensor.')
        exit(-1)
    w = 0
    for i in range(3):
        if values[i] > sth[i]:
            w+=1
    
    print('| {0:^6} | {1:^6} |'.format(*([str(w > 1)] + [w])))
    
    time.sleep(0.5)
