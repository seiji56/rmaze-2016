import time
import sys
sys.path.insert(0, '../libs/')
from melexis import Melexis

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

mlx = Melexis(addr=addr)

print('Reading MLX at ' + hex(addr) + ' temp. difference, press Ctrl-C to quit...')

while True:
    ltime = milli_time()
    try:
        tmp2 = mlx.readObject()
        temperature = mlx.getDifference()
    except IOError:
        print('Could not read sensor.')
        exit(-1)
    print ('Diff. is: ' + str(temperature) + ' degrees read in ' + str(milli_time() - ltime) + ' ms')
    time.sleep(0.5)
