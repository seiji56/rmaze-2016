#import movement as mv
#import sensory as sn

dst_sth = 400
col_sth = 500

MAP = []
sx = 0
sy = 0
rx = 0
ry = 0
rd = 0

def loadMap():
    global sx
    global sy
    global rx
    global ry
    global rd
    global MAP
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
    MAP = [[0 for y in range(sy)] for x in range(sx)]
    print MAP

    index = 5

    for y in range(sy):
        for x in range(sx):
            MAP[x][y] = m[index]
            index += 1

def printMap():
    global sx
    global sy
    global rx
    global ry
    global rd
    global MAP
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
            if (x, y) == (rx, ry):
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


def walkf(move, dst_sth, col_sth, stop):
    global rx
    global ry
    global rd
    walls = (wallr(), walll())
    ret = 0
    while ret < move[1] and (not stop or (walls == (wallr(), walll()) and not wallf())):
	if rd == 0:
	    ry -= 1
	elif rd == 1:
	    rx += 1
	elif rd == 2:
	    ry += 1
	elif rd == 3:
	    rx -= 1
	ret += 1
    return (move[0], ret)

def turnr(move, dst_sth):
    global rd
    rd += move[1]
    rd %= 4
    return move

def turnl(move, dst_sth):
    global rd
    rd -= move[1] + abs(move[1])*4
    rd %= 4
    return move

def wallat(side):
    global rx
    global ry
    global rd
    global MAP
    fin = (rd + side)%4
    
    if fin == 0:
        return MAP[rx][ry] & 0x01 != 0
    elif fin == 1:
        return MAP[rx + 1][ry] & 0x02 != 0
    elif fin == 2:
        return MAP[rx][ry + 1] & 0x01 != 0
    elif fin == 3:
        return MAP[rx][ry] & 0x02 != 0
    return True

def isblack():
    global rx
    global ry
    global MAP
    return MAP[rx][ry] & 0x04 != 0
