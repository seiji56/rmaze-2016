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

    def printMap(self):
        for y in range(0, 2*self.sy + 1):
            line = ''
            for x in range(0, 2*self.sx + 1):
                tile = self.M[x][y]
                line += '+'
                line += '-' if tile.wallu else ' '
            print line
            line = ''
            for x in range(0, 2*self.sx+ 1):
                tile = self.M[x][y]
                line += '|' if tile.walll else ' '
                line += 'v' if tile.visited else ' '
            print line

    def PF(self, init, targ = -1):
        path = []
        curr = 1
        done = False
        found_target = False
        spec = type(targ) is list
        target = [-1, -1, -1]
        self.PFM = [[0 for y in range(-self.sy, self.sy + 1)] for x in range(-self.sx, 
            self.sx + 1)]
 
        self.PFM[init[0] + self.sx][init[1] + self.sy] = 1
        while not done and not found_target:
            done = True
            for x in range(1, 2*self.sx):
                for y in range(1, 2*self.sy):
                    if (not spec and not self.M[x][y].visited and self.PFM[x][y]
                            == curr) or (spec and self.PFM[x][y] == curr and [x,
                                    y] == targ):
                        print "Found target at",(x, y)
                        target = [x, y, curr]
                        found_target = True
                    if self.PFM[x][y] == curr:
                        print "For",(x,y)
                        if self.PFM[x][y - 1] == 0 and not self.wallu((x -
                            self.sx, y - self.sy)
                                ) and not self.M[x][y - 1].isblack:
                            self.PFM[x][y - 1] = curr + 1
                            print "Ok at",(x, y - 1)
                            done = False
                        if self.PFM[x + 1][y] == 0 and not self.wallr((x -
                            self.sx, y - self.sy)
                                ) and not self.M[x + 1][y].isblack:
                            self.PFM[x + 1][y] = curr + 1
                            print "Ok at",(x + 1, y)
                            done = False
                        if self.PFM[x][y + 1] == 0 and not self.walld((x -
                            self.sx, y - self.sy)
                                ) and not self.M[x][y + 1].isblack:
                            self.PFM[x][y + 1] = curr + 1
                            print "Ok at",(x, y + 1)
                            done = False
                        if self.PFM[x - 1][y] == 0 and not self.walll((x -
                            self.sx, y - self.sy)
                                ) and not self.M[x - 1][y].isblack:
                            self.PFM[x - 1][y] = curr + 1
                            print "Ok at",(x - 1, y)
                            done = False
            curr += 1
        if target[0] != -1 and target[1] != -1 and target[2] != -1:
            curr = target[2]
            path += [(target[0] - self.sx, target[1] - self.sy)]
            x, y = target[:2]
            for val in range(curr, 0, -1):
                if self.PFM[x][y - 1] == val - 1 and not self.wallu((x - 
                    self.sx, y - self.sy)):
                    x, y = x, y - 1
                    path = [(x - self.sx, y - self.sy)] + path
                elif self.PFM[x + 1][y] == val - 1 and not self.wallr((x -
                    self.sx, y - self.sy)):
                    x, y = x + 1, y
                    path = [(x - self.sx, y - self.sy)] + path
                elif self.PFM[x][y + 1] == val - 1 and not self.walld((x -
                    self.sx, y - self.sy)):
                    x, y = x, y + 1
                    path = [(x - self.sx, y - self.sy)] + path
                elif self.PFM[x - 1][y] == val - 1 and not self.walll((x -
                    self.sx, y - self.sy)):
                    x, y = x - 1, y
                    path = [(x - self.sx, y - self.sy)] + path
        for y in range(0, 2*self.sy + 1):
            line = ""
            for x in range(0, 2*self.sx + 1):
                line += " "
                line += str(self.PFM[x][y])
            print line
        return path

    def visited(self, tile):
        return self.M[tile[0] + self.sx][tile[1] + self.sy].visited

    def setVisited(self, tile, val = True):
        self.M[tile[0] + self.sx][tile[1] + self.sy].visited = val

    def isblack(self, tile):
        return self.M[tile[0] + self.sx][tile[1] + self.sy].isblack

    def setBlack(self, tile, val = True):
        self.M[tile[0] + self.sx][tile[1] + self.sy].isblack = val

    def wallu(self, tile):
        return self.M[tile[0] + self.sx][tile[1] + self.sy].wallu

    def setWallu(self, tile, val):
        if val:
            print "Wall UP set"
        self.M[tile[0] + self.sx][tile[1] + self.sy].wallu = val

    def wallr(self, tile):
        return self.M[tile[0] + self.sx + 1][tile[1] + self.sy].walll

    def setWallr(self, tile, val):
        if val:
            print "Wall RIGHT set"
        self.M[tile[0] + self.sx + 1][tile[1] + self.sy].walll = val

    def walld(self, tile):
        return self.M[tile[0] + self.sx][tile[1] + self.sy + 1].wallu

    def setWalld(self, tile, val):
        if val:
            print "Wall DOWN set"
        self.M[tile[0] + self.sx][tile[1] + self.sy + 1].wallu = val
        
    def walll(self, tile):
        return self.M[tile[0] + self.sx][tile[1] + self.sy].walll

    def setWalll(self, tile, val):
        if val:
            print "Wall LEFT set"
        self.M[tile[0] + self.sx][tile[1] + self.sy].walll = val

    def wallto(self, tile, side):
        if side == 0:
            return self.wallu(tile)
        if side == 1:
            return self.wallr(tile)
        if side == 2:
            return self.walld(tile)
        if side == 3:
            return self.walll(tile)

    def setWallTo(self, tile, side, val):
        if side == 0:
            self.setWallu(tile, val)
        elif side == 1:
            self.setWallr(tile, val)
        elif side == 2:
            self.setWalld(tile, val)
        elif side == 3:
            self.setWalll(tile, val)
