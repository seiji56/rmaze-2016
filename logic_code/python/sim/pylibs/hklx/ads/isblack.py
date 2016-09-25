import ads_lib

qtra = (2, 3)

def isblack(it = 10, thres = 500):
    val = ads_lib.getval(qtra[0], it)[qtra[1]]
    return val < thres
