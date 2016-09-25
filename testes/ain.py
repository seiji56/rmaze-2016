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
    print('Usage: ' + sys.argv[0] + ' <address>')
    exit(0)
addr = convert(sys.argv[1])

adc = Adafruit_ADS1x15.ADS1015(address=addr, busnum=1)

GAIN = 1

print('Reading ADS1x15 at ' + hex(addr) + ' values, press Ctrl-C to quit...')
print('| {0:^6} | {1:^6} | {2:^6} | {3:^6} | {4:^6} |'.format(*(range(4) + ['Time'])))
print('-' * 46)

while True:
    values = [0]*4
    ltime = milli_time()
    try:
        for i in range(4):
            values[i] = adc.read_adc(i, gain=GAIN)
    except IOError:
        print('Could not read sensor.')
        exit(-1)
    for i in range(4):
        values[i]*=0.002
    print('| {0:^6} | {1:^6} | {2:^6} | {3:^6} | {4:^6}'.format(*(values + [milli_time() - ltime])))

    time.sleep(0.5)
