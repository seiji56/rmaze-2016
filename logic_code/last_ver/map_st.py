class node:
    def __init__(self):
        self.wallu = False
        self.walll = False
        self.visited = False
        self.isblack = False
        #self.vicu = False
        #self.vicd = False
        #self.vicl = False
        #self.vicr = False

class Map:
    def __init__(self, sx, sy):
        self.M = [[node() for y in range(-sy, sy + 1)] for x in range(-sx,
            sx + 1)]
        self.sx = sx
        self.sy = sy

        self.PFM = [[0 for y in range(-sy, sy + 1)] for x in range(-sx, 
            sx + 1)]

    def PF(self, init):
        path = []
        curr = 1
        done = False
        target = [-1, -1, -1]
        self.PFM[x + sx][y + sy] = 1
        while not done:
            done = True
            for x in range(1, 2 * self.sx):
                for y in range(1, 2 * self.sy):
                    if not self.M[x][y].visited and self.PFM[x][y] == curr:
                        target = [x, y, curr]
                    if self.PFM[x][y] == curr:
                        if self.PFM[x][y - 1] == 0 and not self.wallu((x, y)
                                ) and not self.M[x][y - 1].isblack:
                            self.PFM[x][y - 1] = curr + 1
                            done = False
                        if self.PFM[x + 1][y] == 0 and not self.wallr((x, y)
                                ) and not self.M[x + 1][y].isblack:
                            self.PFM[x + 1][y] = curr + 1
                            done = False
                        if self.PFM[x][y + 1] == 0 and not self.walld((x, y)
                                ) and not self.M[x][y + 1].isblack:
                            self.PFM[x][y + 1] = curr + 1
                            done = False
                        if self.PFM[x - 1][y] == 0 and not self.walll((x, y)
                                ) and not self.M[x - 1][y].isblack:
                            self.PFM[x - 1][y] = curr + 1
                            done = False
                    curr += 1
        if target[0] != -1 and target[1] != -1 and target[2] != -1:
            curr = target[2]
            path += tuple(target[:2])
            x, y = target[:2]
            for val in range(curr, 0, 0):
                if self.PFM[x][y - 1] == val - 1 and not self.wallu((x, y)):
                    x, y = x, y - 1
                    path = [(x - sx, y - sy)] + path
                elif self.PFM[x + 1][y] == val - 1 and not self.wallr((x, y)):
                    x, y = x + 1, y
                    path = [(x - sx, y - sy)] + path
                elif self.PFM[x][y +1] == val - 1 and not self.walld((x, y)):
                    x, y = x, y + 1
                    path = [(x - sx, y - sy)] + path
                elif self.PFM[x - 1][y] == val - 1 and not self.walll((x, y)):
                    x, y = x - 1, y
                    path = [(x - sx, y - sy)] + path
        return path

    def visited(self, tile):
        return self.M[tile[0]][tile[1]].visited

    def setVisited(self, tile, val = True):
        self.M[tile[0]][tile[1]].visited = val

    def isblack(self, tile):
        return self.M[tile[0]][tile[1]].isblack

    def setBlack(self, tile, val = True):
        self.M[tile[0]][tile[1]].isblack = val

    def wallu(self, tile):
        return self.M[tile[0]][tile[1]].wallu

    def setWallu(self, tile, val):
        self.M[tile[0]][tile[1]].wallu = val

    def wallr(self, tile):
        return self.M[tile[0] + 1][tile[1]].walll

    def setWallr(self, tile, val):
        self.M[tile[0] + 1][tile[1]].walll = val

    def walld(self, tile):
        return self.M[tile[0]][tile[1] + 1].wallu

    def setWalld(self, tile, val):
        self.M[tile[0]][tile[1] + 1].wallu = val
        
    def walll(self, tile):
        return self.M[tile[0]][tile[1]].walll

    def setWalll(self, tile, val):
        self.M[tile[0]][tile[1]].walll = val

    def wallto(self, tile, side):
        if side == 0:
            return self.wallu(tile)
        if side == 1:
            return self.wallr(tile)
        if side == 2:
            return self.walkd(tile)
        if side == 3:
            return self.walll(tile)

    def setWallTo(self, tile, side, val):
        if side == 0:
            setWallu(tile, val)
        elif side == 1:
            setWallr(tile, val)
        elif side == 2:
            setWalld(tile, val)
        elif side == 3:
            setWalll(tile, val)
