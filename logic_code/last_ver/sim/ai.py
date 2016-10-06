from map_st import *
import kernel
import time

class AI:
    def __init__(self, ramp = True):
        self.memory = Map(10, 10)
        self.pos = [0, 0]
        self.d = 0
        self.queued = []
        self.checkramp = ramp

    def to_the(self, side):
        gdir = self.conv_tog(side)
        return self.s_to_coords(gdir)

    def s_to_coords(self, gdir):
        if gdir == 0:
            return [self.pos[0], self.pos[1] - 1]
        if gdir == 1:
            return [self.pos[0] + 1, self.pos[1]]
        if gdir == 2:
            return [self.pos[0], self.pos[1] + 1]
        if gdir == 3:
            return [self.pos[0] - 1, self.pos[1]]

    def conv_tog(self, side):
        return (side + self.d)%4

    def immediate(self):
        if self.memory.isblack(self.pos):
            return (2, 1)
        if not self.memory.wallto(self.pos,
                self.conv_tog(0)) and not self.memory.visited(
                        self.s_to_coords(self.conv_tog(0))):
            return (0, 1)
        if not self.memory.wallto(self.pos, 
                self.conv_tog(1)) and not self.memory.visited(
                        self.s_to_coords(self.conv_tog(1))):
            return (1, 1)
        if not self.memory.wallto(self.pos, 
                self.conv_tog(3)) and not self.memory.visited(
                        self.s_to_coords(self.conv_tog(3))):
            return (3, 1)
        return (1, 2)

    def method(self):
        if self.memory.isblack(self.pos):
            return 0
        for i in range(4):
            if not self.memory.wallto(self.pos,
                    self.conv_tog(i)) and not self.memory.visited(
                    self.s_to_coords(self.conv_tog(i))):
                return 0
        return 1

    def turnMove(self, d0, d1):
        print "Has to turn from",d0,"to",d1
        rcnt = (d1 - d0 + 4)%4
        if rcnt == 3:
            return (3, 1)
        else:
            return (1, rcnt)

    def apply(self, action):
        print "Applying:",action
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

    def PF(self, targ = -1):
        aclst = []
        path = self.memory.PF(self.pos, targ)
        print "Map found path:", path
        if len(path) == 0:
            return False
        td = self.d
        for i in range(0, len(path) - 1):
            diff = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
            nd = 0
            print "Diff:",diff
            if diff == (0, -1): 
                nd = 0
            elif diff == (1, 0):
                nd = 1
            elif diff == (0, 1):
                nd = 2
            elif diff == (-1, 0):
                nd = 3
            else:
                return (-1, -1)
            if td != nd:
                aclst = [self.turnMove(td, nd)] + aclst
                td = nd
            
            aclst = [(0, 1)] + aclst

        fcnt = 0 

        print "Brute aclist:",aclst

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
        if fcnt > 0:
            finlist = [(0, fcnt)] + finlist
        print "Generated action list:",finlist
        return finlist

    def scan_tile(self):
        walls = []
        walls += [kernel.wallf()]
        walls += [kernel.wallr()]
        walls += [kernel.wallb()]
        walls += [kernel.walll()]

        for i in range(4):
            print "Wall to",i,":",walls[i]

        for i in range(4):
            if i != 2:
                self.memory.setWallTo(self.pos, self.conv_tog(i), walls[i])
        self.memory.setBlack(self.pos, kernel.isblack())
        self.memory.setVisited(self.pos)
        self.memory.printMap()
        
        if kernel.isramp() and self.checkramp:
            self.memory.setBlack()
            self.apply((1, 1))
            self.apply((0, 1))

            secfloor = AI(False)
            secfloor.memory.setVisited((0, 0))
            secfloor.memory.setBlack((0, 0))
            secfloor.apply((0, 1))
            secfloor.memory.setVisited((0, -1))
            secfloor.memory.setWallu((0, -1), False)
            secfloor.memory.setWallr((0, -1), True)
            secfloor.memory.setWalll((0, -1), True)
            secfloor.memory.setWalld((0, -1), False)
            secfloor.apply((0, 1))
            secfloor.memory.setVisited((0, -2))
            secfloor.memory.setWallu((0, -2), True)
            secfloor.memory.setWallr((0, -2), False)
            secfloor.memory.setWalll((0, -2), True)
            secfloor.memory.setWalld((0, -2), False)

            kernel.upramp()
            secfloor.loop()
            kernel.downramp()

    def goback(self):
        if self.pos == [0, 0]:
            print "Already here!"
            return False
        print "Going back..."
        actions = self.PF([0, 0])
        if not actions:
            return False
        self.queued += actions
        return True

    def loop(self):
        over = False
        while not over:
            time.sleep(1)
            kernel.printMap()
            self.scan_tile()
            if len(self.queued) > 0:
                action = self.queued[0]
                print "que TODO:",action
                success = kernel.apply(action)
                self.apply(success)
                if success != action:
                    self.queued = self.queued[1:]
                else:
                    self.queued = []
            else:
                met = self.method()
                if met == 0:
                    action = self.immediate()
                    print "imm TODO:",action
                    success = kernel.apply(action)
                    self.apply(success)
                elif met == 1:
                    actions = self.PF()
                    if actions == False:
                        over = not self.goback()
                    else:
                        self.queued += actions
