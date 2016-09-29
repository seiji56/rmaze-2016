from map_st import *
import kernel

class AI:
    def __init__(self):
        self.memory = Map(10, 10)
        self.pos = [0, 0]
        self.d = 0
        self.queued = []

    def to_the(self, side):
        gdir = self.conv_tog(side)
        return s_to_coords(gdir)

    def s_to_coords(self, gdir):
        if gdir == 0:
            return [self.pos[0] - 1, self.pos[1]]
        if gdir == 1:
            return [self.pos[0], self.pos[1] + 1]
        if gdir == 2:
            return [self.pos[0] + 1, self.pos[1]]
        if gdir == 3:
            return [self.pos[0], self.pos[1] - 1]

    def conv_tog(self, side):
        return (side + self.d)%4

    def immediate(self):
        if self.memory.isblack(self.pos):
            return (2, 1)
        if not self.memory.wallto(self.pos, conv_tog(0)):
            return (0, 1)
        if not self.memory.wallto(self.pos, conv_tog(1)):
            return (1, 1)
        if not self.memory.wallto(self.pos, conv_tog(3)):
            return (3, 1)

    def method(self):
        if self.memory.isblack(self.pos):
            return 0
        for i in range(4):
            if not self.memory.wallto(self.pos, 
                    i) and not self.memory.visited(s_to_coords(i)):
                return 0
        return 1

    def turnMove(self, d0, d1):
        rcnt = (d1 - d0 + 4)%4
        if rcnt == 3:
            return (3, 1)
        else:
            return (1, rcnt)

    def apply(self, action):
        if action[0] == 0 or action[0] == 2:
            for i in range(action[1]):
                self.pos = self.to_the(action[0])
        if action[0] == 1:
            self.d += action[1]
            self.d %= 4
        if action[0] == 3:
            self.d += action[1]*4
            self.d -= action[1]
            self.d %= 4

    def PF(self):
        aclst = []
        path = self.memory.PF(self.pos)
        if len(path) == 0:
            return False
        for i in range(0, len(path) - 1):
            diff = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
            td = 0
            if diff == (0, -1): 
                td = 0
            elif diff == (1, 0):
                td = 1
            elif diff == (0, 1):
                td = 2
            elif diff == (-1, 0):
                td = 3
            else:
                return (-1, -1)
            if td != self.d:
                aclst = [turnMove(self.d, td)] + aclst
            
            aclst = [(0, 1)] + aclst

        fcnt = 0

        finlist = []

        for i in aclst:
            if i != (0, 1) and fcnt > 0:
                finlist = [(0, fcnt)] + finlist
                finlist = [i] + finlist
                fcnt = 0
            elif i == (0, 1):
                fcnt += 1
            else:
                finlist = [i] + finlist
        
        return finlist

    def scan_tile(self):
        walls = []
        walls += [kernel.wallf()]
        walls += [kernel.wallr()]
        walls += [kernel.wallb()]
        walls += [kernel.walll()]

        for i in range(4):
            self.memory.setWallTo(self.pos, conv_tog(i), walls[i])
        self.memory.setBlack(self.pos, kernel.isblack())
        #
        #if kernel.isramp():
        #    secfloor = AI()
        #    secfloor.memory.setWallu(True)
        #    secfloor.memory.setWallr(False)
        #    secfloor.memory.setWalll(True)
        #    secfloor.memory.setWalld(True)
        #    kernel.goramp()

    def goback(self):
        return False

    def loop(self):
        over = False
        while not over:
            scan_tile()
            if len(queued) > 0:
                action = queued[0]
                success = kernel.apply(action)
                self.apply(success)
                if success != action:
                    queued = queued[1:]
                else:
                    queued = []

            met = self.method()
            if met == 0:
                action = immediate()
                success = kernel.apply(action)
                self.apply(success)
            elif met == 1:
                actions = PF()
                if actions == False:
                    over = not goback()
                else:
                    self.queued += actions
