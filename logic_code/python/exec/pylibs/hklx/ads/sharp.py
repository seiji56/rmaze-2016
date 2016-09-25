import time
import ads_lib

def toval(raw, side):
    return raw

def distwall(side, it, extra = 0):
    values = [0]*3
    k = 0

    raw = ads_lib.getval(side, it)
    if raw == 0:
        return True
    if extra != 0:
        extra += [raw]
    
    val = toval(raw, side)

    for i in ads_lib.adddef[side][1:]:
        values[k] = val[i]
        k += 1

    return values # Left, middle, right

def distavg(side, it):
    values = distwall(side, it)
    return sum(values)/len(values)
    

def haswall(side, it=10, thres=[400, 400, 400], extra=0):
    cnt = 0

    values = distwall(side, it)
    if extra != 0:
        extra += [values]
    for i in range(3):
        if values[i] > thres[i]:
            cnt += 1
    return cnt > 1

def getbalanceang(it):
    bal = 0
    wallcnt = 0
    extra = []
    for i in range(4):
        if haswall(wall, it, extra):
            bal += extra[0][2] - extra[0][0]
            wallcnt += 1
    return bal/wallcnt

def getbalancelin(it):
    bal = (0, 0)
    bal[0] = distavg(3, it) - distavg(1, it)
    bal[1] = distavg(2, it) - distavg(0, it)
    return bal

