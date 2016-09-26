from map import map
from ai import *
import time

def main():
    AI = ai(map(10))
    while True:
        print AI.pos
        kernel.print_act()
        AI.loop()
        time.sleep(1)
main()
