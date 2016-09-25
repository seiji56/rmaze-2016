from map import map
import pylibs.base_lib as kernel

VISITED=0x04
COLOR=0x08
CHECK=0x10

PULLBACK = 0x01
PATHFINDING = 0x02
IMMEDIATE = 0x03

class ai:
    def __init__(self, m=map(10), zero_t=True, init_pos=(0, 0, 0)):
        self.M = m
        self.d = 0
        self.donetop = False
        self.pos = init_pos

        print("Creating AI object...")
        tmpsize = self.M.getsz()*2 - 1
        print("Allocating temporary map for PF...")
        self.PFm = [[0 for j in range(tmpsize)] for i in range(tmpsize)]
        print("Allocated PF map.")
        if zero_t:
            kernel.zeroTimer()
            print("Zeroed timer.")
        print("Robot position is now " + str(self.pos))
    def __del__(self):
        print("Destroying AI object...")

    def loop(self):
        self.scan_tile()
        met = self.best_method()

        if met == PATHFINDING:
            path = []
            self.find_path(path)
            acts = []
            self.translate_path(acts, path)
            act = acts[0]
        elif met == IMMEDIATE:
            act = self.immediate()
        elif met == PULLBACK:
            act = (BACK, 1)
        else:
            print("Unknown method " + str(met))
            return

        apply(act, kernel.execute(act))

    def best_method(self):
        if self.M.at(self.pos[0], self.pos[1], self.pos[2]) & COLOR == 0:
            return PULLBACK

        available = []
        self.accessible(available, self.pos[0], self.pos[1], self.pos[2])

        disponible = 0
        for i in available:
            if self.M.at(i) & VISITED:
                disponible += 1

        if disponible > 0:
            return IMMEDIATE

        return PATHFINDING

    def apply(self, act, success):
        act[1] = success
        sz = self.M.getsz()

        if act[0] == BACK or act[0] == LEFT:
            act[1] = -act[1]
        if act[0] == BACK or act[0] == FRONT:
            tmp = self.d%4
            if tmp == 0 or tmp == 3:
                act[1] = -act[1]
            if tmp == 0 or tmp == 2:
                if self.pos[1] + act[1] > sz - 1 or self.pos[1] + act[1] < 1 - sz:
                    return False
                self.pos[1] += act[1]
            else:
                if self.pos[0] + act[1] > sz - 1 or self.pos[0] + act[1] < 1 - sz:
                    return False
                self.pos[0] += act[1]
        elif act[0] == RIGHT or act[0] == LEFT:
            self.d = (self.d + act[1] + 4)%4
        else:
            print("Unknown action " + act[0])
            return False
        
        return True

    def accessible(self, result, x, y, f):
        sz = self.M.getsz()
        if x > 1 - sz and self.M.wall(x, y, f, 3) == False:
            result += [(x - 1, y, f)]
        if x < sz - 1 and self.M.wall(x, y, f, 1) == False:
            result += [(x + 1, y, f)]
        if y > 1 - sz and self.M.wall(x, y, f, 0) == False:
            result += [(x, y - 1, f)]
        if y < sz - 1 and self.M.wall(x, y, f, 2) == False:
            result += [(x, y + 1, f)]

    #def accessible(self, result, coords):
    #    self.accessible(result, coords[0], coords[1], coords[2])

    def find_path(self, path):
        sz = self.M.getsz() - 1
        f = self.pos[2]
        for i in range(self.M.getsz()*2 - 1):
            for j in range(self.M.getsz()*2 - 1):
                self.PFm[i][j] = -1

        BFSQ = []
        self.PFm[self.pos[0] + sz][self.pos[1] + sz] = 0
        BFSQ.append((self.pos, 1))

        found = False
        foundramp = True
        unvisited = (0, 0, 0)
        ramp = (0, 0, 0)

        while len(BFSQ) > 0 and found == False:
            while len(BFSQ) > 0 and found == False:
                Next = BSFQ.popleft()
                dist = Next[1]
                Next = Next[0]

                self.PFm[Next[0] + sz][Next[1] + sz] = dist

                neighbors = []
                accessible(neighbors, Next)
                for i in range(len(neighbors)):
                    tmp = neighbors[i]

                    if self.M.at(tmp) & VISITED and PFm[tmp[0] + sz][tmp[1] +
                            sz] == -1 and self.M.at(tmp) & RAMP == 0:
                        BFSQ += [(tmp, dist + 1)]
                    elif self.M.at(tmp) & VISITED == 0:
                        found = True
                        unvisited = tmp
                        self.PFm[tmp[0] + sz][tmp[1] + sz] = dist + 1

                    if self.M.at(tmp) & RAMP != 0:
                        foundramp = True
                        ramp = tmp
                        self.PFm[tmp[0] + sz][tmp[1] + sz] = dist + 1
        if found:
            path += [unvisited]
        elif foundramp and donetop == false:
            path += [ramp]
        else:
            path += [(0, 0, f)]

        while self.PFm[path[-1][0] + sz][path[-1][1] + sz] != 1:
            possible = []
            self.accessible(possible, path[-1])

            for i in len(possible):
                tmp = possible[i]

                if self.PFm[path[-1][0] + sz][path[-1][1] + sz] == self.PFm[tmp[0] + sz][tmp[1] + sz] + 1:
                    path += [tmp]
                    break

    def translate_path(translated, path):
        tmppos = path[-1]
        tmpd = self.d
        while len(path) > 0:
            path.pop()
            if path[-1][1] == tmppos[1] - 1:
                if tmpd != 0:
                    if tmpd == 3:
                        translated += [(RIGHT, 1)]
                    else:
                        translated += [(LEFT, tmpd)]
                    tmpd = 0
                tmppos = path[-1]
            elif path[-1][0] == tmppos[0] + 1:
                if tmpd != 1:
                    if tmpd == 0:
                        translated += [(RIGHT, 1)]
                    else:
                        translated += [(LEFT, tmpd - 1)]
                    tmpd = 1
                tmppos = path[-1]
            elif path[-1][1] == tmppos[1] + 1:
                if tmpd != 2:
                    if tmpd == 3:
                        translated += [(LEFT, 1)]
                    else:
                        translated += [(RIGHT, 2 - tmpd)]
                    tmpd = 2
                tmppos = path[-1]
            elif path[-1][0] == tmppos[0] - 1:
                if tmpd != 3:
                    if tmpd == 0:
                        translated += [(LEFT, 1)]
                    else:
                        translated += [(RIGHT, 3 - tmpd)]
                    tmpd = 3
                tmppos = path[-1]
            translated += [(FRONT, 1)]
            
    def scan_tile(self):
        for i in range(4):
            self.M.setWall(self.pos[0], self.pos[1], self.pos[2], i, (kernel.distance((i - self.d + 4)%4)))
        self.M.mark(self.pos[0], self.pos[1], self.pos[2], VISITED, True)

        color = kernel.color()

        if color == 0:
            self.M.mark(self.pos[0], self.pos[1], self.pos[2], COLOR, False)
        elif color == 1:
            self.M.mark(self.pos[0], self.pos[1], self.pos[2], COLOR, True)
        else:
            self.M.mark(self.pos[0], self.pos[1], self.pos[2], COLOR, True)
            self.M.mark(self.pos[0], self.pos[1], self.pos[2], CHECK, True)

    def immediate(self):
        preferable = [0, 1, 3, 2]
        available = []
        accessible(available, self.pos)
        for i in range(4):
            pd = (4 + preferable[i] + d)%4
            if pd == 0:
                for j in available:
                    if self.pos[0] == j[0] and  self.pos[1] - 1 == j[0]:
                        return (FRONT, 1)
            elif pd == 1:
                for j in available:
                    if self.pos[0] + 1 == j[0] and self.pos[1] == j[0]:
                        return (RIGHT, 1)
            elif pd == 2:
                for j in available:
                    if self.pos[0] == j[0] and self.pos[1] + 1 == j[0]:
                        return (BACK, 1)
            else:
                for j in available:
                    if self.pos[0] - 1 == j[0] and self.pos[1]:
                        return (LEFT, 1)
        return(FRONT, 0)
                        
