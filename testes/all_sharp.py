# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
import os
# Import the ADS1x15 module.
import Adafruit_ADS1x15

milli_time = lambda: int(round(time.time() * 1000))
# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
adc1 = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
adc2 = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
adc3 = Adafruit_ADS1x15.ADS1015(address=0x4a, busnum=1)
adc4 = Adafruit_ADS1x15.ADS1015(address=0x4b, busnum=1)
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print(' | {0:^6} | {1:^6} | {2:^6} | {3:^6} | {4:^6} | '.format(*(range(4) + ['Time'])))
print('-' * 48)
# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values1 = [0]*4
    values2 = [0]*4
    values3 = [0]*4
    values4 = [0]*4
    ltime   = milli_time()
    try:
        for i in range(4):
            # Read the specified ADC channel using the previously set gain value.
            values1[i] = adc1.read_adc(i, gain=GAIN)
            values2[i] = adc2.read_adc(i, gain=GAIN)
            values3[i] = adc3.read_adc(i, gain=GAIN)
            values4[i] = adc4.read_adc(i, gain=GAIN)
            # Note you can also pass in an optional data_rate parameter that controls
            # the ADC conversion time (in samples/second). Each chip has a different
            # set of allowed data rate values, see datasheet Table 9 config register
            # DR bit values.
            #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
            # Each value will be a 12 or 16 bit signed integer value depending on the
            # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    except IOError:
        print('Could not read a sensor.')
        exit(-1)
    # Print the ADC values.
    os.system("clear")
    print('1| {0:^6} | {1:^6} | {2:^6} | {3:^6} |        |'.format(*values1))
    print('2| {0:^6} | {1:^6} | {2:^6} | {3:^6} |        |'.format(*values2))
    print('3| {0:^6} | {1:^6} | {2:^6} | {3:^6} |        |'.format(*values3))
    print('4| {0:^6} | {1:^6} | {2:^6} | {3:^6} | {4:^6} |'.format(*(values4 + [milli_time() - ltime])))
    # Pause for half a second.
    time.sleep(0.5)
