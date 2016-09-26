mapv = {}
mapsz = [0, 0]
mappos = [0, 0, 0]

actions = []

def load_map(path):
    global mappos
    global mapsz
    global mapv
    mapfile = open(path, 'r')
    content = mapfile.read()
    content = content.split()
    print ("Splitted content is: " + str(content))
    sx = int(content[0])
    sy = int(content[1])
    px = int(content[2])
    py = int(content[3])
    rot = int(content[4])
    mapsz = [sx, sy]
    mappos = [px, py, rot]

    contentptr = 5

    for y in range(sy):
        for x in range(sx):
            mapv[(x, y)] = int(content[contentptr])
            contentptr += 1

load_map("map.map")

def print_act():
    for i in actions:
        print(i)

def sumv(v1, v2):
    return [sum(x) for x in zip(v1, v2)]

def wall_rel(side):
    global mappos
    #print side,':',haswall((side + mappos[2])%4)
    return haswall((side + mappos[2])%4)

def walk(cnt, stop):
    global actions
    global mappos
    global mapv
    knt = 0
    wallr = wall_rel(3)
    walll = wall_rel(1)
    print mapv[(1, 0)]
    print stop, wall_rel(3) == wallr, wall_rel(1) == walll, wall_rel(0) == False
    while stop == False or (wall_rel(3) == wallr and wall_rel(1) == walll and
            wall_rel(0) == False and cnt > knt):
        if mappos[2] == 0:
            mappos[1] -= 1
        elif mappos[2] == 1:
            mappos[0] += 1
        elif mappos[2] == 2:
            mappos[1] += 1
        elif mappos[2] == 3:
            mappos[0] -= 1
        knt += 1
    if knt > 0:
        actions += ['F' + str(knt) if cnt >= 0 else 'B' + str(knt)]
    return knt

def turn(cnt):
    global actions
    global mappos
    actions += ['R' + str(cnt) if cnt >= 0 else 'L' + str(-cnt)]
    mappos[2] = (mappos[2] + cnt + abs(cnt)*4)%4
    return abs(cnt)

def drop():
    global actions
    actions += ['D1']
    return 1

def isblack():
    global mappos
    global mapv
    return (mapv[tuple(mappos[:2])] & 8) != 0

def haswall(side):
    global mappos
    global mapv

    #print "side:",side

    if side == 0:
        return (mapv[tuple(mappos[:2])] & 1) != 0
    elif side == 1:
        return (mapv[tuple(sumv(mappos[:2], [1, 0]))] & 2) != 0
    elif side == 2:
        return (mapv[tuple(sumv(mappos[:2], [0, 1]))] & 1) != 0
    elif side == 3:
        return (mapv[tuple(mappos[:2])] & 2) != 0
    return True

def execute(action):
    print("Executing " + str(action))
    if action[0] == 0:
        return walk(action[1], True)
    elif action[0] == 1:
        return turn(action[1])
    elif action[0] == 2:
        return walk(-action[1], True)
    elif action[0] == 3:
        return turn(-action[1])
    elif action[0] == 4:
        return drop()
    return -1

def color():
    return isblack() == False

def distance(side):
    if haswall(side):
        return 0
    else:
        return 1

def align():
    align()

def zeroTimer():
    return
