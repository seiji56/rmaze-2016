import movement as mv
import sensory as sn

dst_sth = 400
col_sth = 500

def apply(move):
    move = list(move)
    #move[1] = 1
    if move[0] == 0:
        return mv.walkf(move, dst_sth, col_sth, True)
    elif move[0] == 1:
        return mv.turnr(move)
    elif move[0] == 3:
        return mv.turnl(move)
    elif move[0] == 2:
        return mv.walkb(move, dst_sth, col_sth, True)
        
def align():
    return

def wallf():
    return sn.wf(dst_sth)

def wallr():
    return sn.wr(dst_sth)

def wallb():
    return sn.wb(dst_sth)

def walll():
    return sn.wl(dst_sth)

def isblack():
    return sn.color(col_sth)
