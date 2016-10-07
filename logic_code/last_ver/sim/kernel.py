#import movement as mv
#import sensory as sn

dst_sth = 400
col_sth = 500

MAP  = []
MAP2 = []
sx = 0
sy = 0
rx = 0
ry = 0
rx2 = 0
ry2 = 0
rd2 = 0
rd = 0
m  = 0

def loadMap():
    global sx
    global sy
    global rx
    global ry
    global rd
    global rx2
    global ry2
    global rd2
    global MAP
    global MAP2
    path = raw_input("Map file: ")
    m = open(path, 'r')
    m = m.read()
    m = m.split()
    m = [int(i) for i in m]
    sx = m[0]
    sy = m[1]
    rx = m[2]
    ry = m[3]
    rd = m[4]
    rx2 = m[5]
    ry2 = m[6]
    rd2 = m[7]
    MAP  = [[0 for y in range(sy)] for x in range(sx)]
    MAP2 = [[0 for y in range(sy)] for x in range(sx)]

    index = 8

    for y in range(sy):
        for x in range(sx):
            MAP[x][y]  = m[index]
            index += 1

    for y in range(sy):
        for x in range(sx):
            MAP2[x][y] = m[index]
            index += 1

def printMap():
    global sx
    global sy
    global rx
    global ry
    global rd
    global rx2
    global ry2
    global rd2
    global m
    global MAP
    global MAP2
    for y in range(sy):
        fl = ''
        sl = ''
        for x in range(sx):
            val = MAP[x][y]
            if val & 0x01 != 0:
                fl += '+--'
            else:
                fl += '+  '
            if val & 0x02 != 0:
                sl += '|'
            else:
                sl += ' '
            black = False
            if val & 0x04 != 0:
                sl += '\033[40m'
                black = True
            if (x, y) == (rx, ry) and m == 0:
                if rd == 0:
                    sl += '^'
                elif rd == 1:
                    sl += '>'
                elif rd == 2:
                    sl += 'v'
                elif rd == 3:
                    sl += '<'
            else:
                sl += ' '
            if val & 0x08:
                sl += 'R'
            else:
                sl += ' '
            if black:
                sl += '\033[00m'
        fl += '\t'
        sl += '\t'

        for x in range(sx):
            val = MAP2[x][y]
            if val & 0x01 != 0:
                fl += '+--'
            else:
                fl += '+  '
            if val & 0x02 != 0:
                sl += '|'
            else:
                sl += ' '
            black = False
            if val & 0x04 != 0:
                sl += '\033[40m'
                black = True
            if (x, y) == (rx2, ry2) and m == 1:
                if rd2 == 0:
                    sl += '^'
                elif rd2 == 1:
                    sl += '>'
                elif rd2 == 2:
                    sl += 'v'
                elif rd2 == 3:
                    sl += '<'
            else:
                sl += ' '
            if val & 0x08:
                sl += 'R'
            else:
                sl += ' '
            if black:
                sl += '\033[00m'

        print fl
        print sl

loadMap()
printMap()

def apply(move):
    move = list(move)
    #move[1] = 1
    if move[0] == 0:
        return walkf(move, dst_sth, col_sth, True)
    elif move[0] == 1:
        return turnr(move, dst_sth)
    elif move[0] == 3:
        return turnl(move, dst_sth)
    elif move[0] == 2:
        return walkb(move, dst_sth, col_sth, True)
        
def align():
    return

def wallf():
    return wallat(0)

def wallr():
    return wallat(1)

def wallb():
    return wallat(2)

def walll():
    return wallat(3)

def isramp():
    global rx
    global ry
    global MAP
    return MAP[rx][ry] & 0x08 != 0

def upramp():
    global m
    m = 1

def downramp():
    global m
    m = 0
    apply((1, 2))
    apply((0, 1))


def walkf(move, dst_sth, col_sth, stop):
    global rx
    global ry
    global rd
    global rx2
    global ry2
    global rd2
    global m

    walls = (wallr(), walll())
    ret = 0
    while ret < move[1] and (not stop or (walls == (wallr(), walll()) and not wallf())):
        if m == 0:
            if rd == 0:
                ry -= 1
            elif rd == 1:
                rx += 1
            elif rd == 2:
                ry += 1
            elif rd == 3:
                rx -= 1
        else:
            if rd2 == 0:
                ry2 -= 1
            elif rd2 == 1:
                rx2 += 1
            elif rd2 == 2:
                ry2 += 1
            elif rd2 == 3:
                rx2 -= 1
        ret += 1
    return (move[0], ret)

def walkb(move, dst_sth, col_sth, stop):
    global rx
    global ry
    global rd
    global rx2
    global ry2
    global rd2
    global m

    walls = (wallr(), walll())
    ret = 0
    while ret < move[1] and (not stop or walls == (wallr(), walll())):
        if m == 0:
            if rd == 0:
                ry += 1
            elif rd == 1:
                rx -= 1
            elif rd == 2:
                ry -= 1
            elif rd == 3:
                rx += 1
        else:
            if rd2 == 0:
                ry2 += 1
            elif rd2 == 1:
                rx2 -= 1
            elif rd2 == 2:
                ry2 -= 1
            elif rd2 == 3:
                rx2 += 1
        ret += 1
    return (move[0], ret)

def turnr(move, dst_sth):
    global rd
    global rd2
    global m
    if m == 0:
        rd += move[1]
        rd %= 4
    else:
        rd2 += move[1]
        rd2 %= 4
    return move

def turnl(move, dst_sth):
    global rd
    global rd2
    global m
    if m == 0:
        rd -= move[1] + abs(move[1])*4
        rd %= 4
    else:
        rd2 -= move[1] + abs(move[1])*4
        rd2 %= 4
    return move

def wallat(side):
    global rx
    global ry
    global rd
    global rx2
    global ry2
    global rd2
    global m
    global MAP
    global MAP2
    
    if m == 0:
        fin = (rd + side)%4
        
        if fin == 0:
            return MAP[rx][ry] & 0x01 != 0
        elif fin == 1:
            return MAP[rx + 1][ry] & 0x02 != 0
        elif fin == 2:
            return MAP[rx][ry + 1] & 0x01 != 0
        elif fin == 3:
            return MAP[rx][ry] & 0x02 != 0
    else:
        fin = (rd2 + side)%4
        
        if fin == 0:
            return MAP2[rx2][ry2] & 0x01 != 0
        elif fin == 1:
            return MAP2[rx2 + 1][ry2] & 0x02 != 0
        elif fin == 2:
            return MAP2[rx2][ry2 + 1] & 0x01 != 0
        elif fin == 3:
            return MAP2[rx2][ry2] & 0x02 != 0
 
    return True

def isblack():
    global rx
    global ry
    global rx2
    global ry2
    global m
    global MAP
    global MAP2
    if m == 0:
        return MAP[rx][ry] & 0x04 != 0
    else:
        return MAP2[rx2][ry2] & 0x04 != 0
