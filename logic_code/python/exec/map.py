WALL_H = 0x01
WALL_V = 0x02

class map:
    def __init__(self, s):
        self.sz = s
        print("Creating map object...")
        s = 2*self.sz - 1

        print("Allocating map...")

        self.M = [[[0, 0] for j in range(s)] for i in range(s)]

    def __del__(self):
        print("Map object deleted.")

    def at(self, x, y, f):
        return self.M[x - 1 + self.sz][y - 1 + self.sz][f]

    #def at(self, coords):
    #    return self.at(coords[0], coords[1], coords[2])

    def set(self, x, y, f, v):
        self.M[x - 1 + self.sz][y - 1 + self.sz][f] = v

    #def set(self, coords, v):
    #    self.set(coords[0], coords[1], coords[2], v)

    def mark(self, x, y, f, m, v):
        if v:
            self.M[x - 1 + self.sz][y - 1 + self.sz][f] |= m
        else:
            self.M[x - 1 + self.sz][y - 1 + self.sz][f] &= ~m

    #def mark(self, coords, m, v):
    #    self.mark(coords[0], coords[1], coords[2], m, v)

    def setWall(self, x, y, f, d, v):
        if d == 0:
            if y - 1 + self.sz == 0:
                return
            if v:
                self.M[x - 1 + self.sz][y - 1 + self.sz][f] |= WALL_H
            else:
                self.M[x - 1 + self.sz][y - 1 + self.sz][f] &= ~WALL_H
        elif d == 1:
            if x + 1 - self.sz == 0:
                return
            if v:
                self.M[x + self.sz][y - 1 + self.sz][f] |= WALL_V
            else:
                self.M[x + self.sz][y - 1 + self.sz][f] &= ~WALL_V
        elif d == 2:
            if y + 1 - self.sz == 0:
                return
            if v:
                self.M[x - 1 + self.sz][y + self.sz][f] |= WALL_H
            else:
                self.M[x - 1 + self.sz][y + self.sz][f] &= ~WALL_H
        elif d == 3:
            if y - 1 + self.sz == 0:
                return
            if v:
                self.M[x - 1 + self.sz][y - 1 + self.sz][f] |= WALL_V
            else:
                self.M[x - 1 + self.sz][y - 1 + self.sz][f] &= ~WALL_V
        else:
            return

    #def setWall(self, coords, d, v):
    #    self.setWall(coords[0], coords[1], coords[2], d, v)

    def wall(self, x, y, f, d):
        if d == 0:
            if y - 1 + self.sz == 0:
                return True
            return self.M[x - 1 + self.sz][y - 1 + self.sz][f] & WALL_H != 0
        elif d == 1:
            if x + 1 - self.sz == 0:
                return True
            return self.M[x + self.sz][y - 1 + self.sz][f] & WALL_V != 0
        elif d == 2:
            if y + 1 - self.sz == 0:
                return True
            return self.M[x - 1 + self.sz][y + self.sz][f] & WALL_H != 0
        elif d == 3:
            if y - 1 + self.sz == 0:
                return True
            return self.M[x - 1 + self.sz][y - 1 + self.sz][f] & WALL_V != 0
        else:
            return False

    #def wall(self, coords, d):
    #    return self.wall(coords[0], coords[1], coords[2], d)

    def search(self, results, m, v):
        for x in range(1 - self.sz, self.sz):
            for y in range(1 - self.sz, self.sz):
                for f in range(2):
                    if self.at(x, y, f) & m == v & m:
                        results += [(x, y, f)]

    def getsz(self):
        return self.sz
