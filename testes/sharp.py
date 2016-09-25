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

if len(sys.argv) < 3:
    print('Usage: ' + sys.argv[0] + ' <address> <port>')
    exit(0)
addr = convert(sys.argv[1])
port = convert(sys.argv[2])
it = 1
if len(sys.argv) == 4:
    it = convert(sys.argv[3])
adc = Adafruit_ADS1x15.ADS1015(address=addr, busnum=1)

GAIN = 1

print('Reading port ' + str(port) + 'ADS1x15 at ' + hex(addr) + ' values, press Ctrl-C to quit...')
print('| {0:^6} | {1:^6} |'.format(*([port] + ['Time'])))
#print('-' * 46)

while True:
    value = 0
    ltime = milli_time()
    try:
        for i in range(it):
            value += adc.read_adc(port, gain=GAIN)
    except IOError:
        print('Could not read sensor.')
        exit(-1)
    value /= it
    print('| {0:^6} | {1:^6} |'.format(*([value] + [milli_time() - ltime])))
    
    time.sleep(0.5)
