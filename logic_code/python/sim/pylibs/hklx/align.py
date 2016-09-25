import hklx_lib
import ads.sharp as sharp

def align():
    angmul = 1
    linmul = 1
    angdis = sharp.getbalanceang()*angmul
    lindis = sharp.getbalancelin()*linmul

    hklx_lib.turn(angdis)
    hklx_lib.walk(lindis[1]/30, 500)
    hklx_lib.lateral(lindis[0]/30, 500)
