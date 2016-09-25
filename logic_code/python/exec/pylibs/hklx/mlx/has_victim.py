import mlx_lib

adddef = [[0], [1, 2], [], [3, 4]]

def has_victim(side, it, thres):
    diffs = []
    for addr in adddef[side]:
        diffs += [mlx_lib.readdiff(addr, it)]
    return min(diffs) > thres
