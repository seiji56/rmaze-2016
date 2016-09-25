import hklx.hklx_lib as hklx_lib
import hklx.align as align

import hklx.mlx.mlx_lib as mlx_lib

import hklx.ads.ads_lib as ads_lib
import hklx.ads.isblack as isblack
import hklx.ads.sharp as sharp

def execute(action):
    action[1] = 1
    if action[0] == 0:
        return hklx_lib.walk(action[1], 1000, True)
    elif action[0] == 1:
        return hklx_lib.turn(action[1], 1000)
    elif action[0] == 2:
        return hklx_lib.walk(-action[1], 1000, True)
    elif action[0] == 3:
        return hklx_lib.turn(-action[1], 1000)
    elif action[0] == 4:
        return hklx_lib.drop()
    return -1

def color():
    return isblack.isblack()

def distance(side):
    if sharp.haswall(side):
        return 0
    else:
        return 1

def align():
    align.align()

def zeroTimer():
    return
