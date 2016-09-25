from melexis import Melexis

print("Loading MLX lib...")

adddef = [0x0A, 0x0B, 0x0C, 0x0D, 0x0E]

mlx = []
for i in adddef:
    mlx += [Melexis(addr=i)]

def readtemp(sensor, it):
    temp = 0
    for i in range(it):
        temp += mlx[sensor].readObject()
    temp /= it
    return temp

def readamb(sensor, it):
    temp = 0
    for i in range(it):
        temp += mlx[sensor].readAmbient()
    temp /= it
    return temp

def readdiff(sensor, it):
    temp = 0
    for i in range(it):
        temp += mlx[sensor].getDifference()
    temp /= it
    return temp
