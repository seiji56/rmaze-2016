import time
import sys
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)

gpio.setup(27, gpio.IN)
gpio.setup(22, gpio.IN)
gpio.setup(9, gpio.IN)
gpio.setup(10, gpio.OUT)
gpio.setup(11, gpio.OUT)

gpio.output(10, gpio.LOW)

while True:
    gpio.output(11, gpio.HIGH)

    time.sleep(.001)

    if gpio.input(27):
        print 'L'
    if gpio.input(22):
        print 'F'
    if gpio.input(9):
        print 'R'

    gpio.output(11, gpio.LOW)
    #time.sleep(.5)
