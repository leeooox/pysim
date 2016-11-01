import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Amp

def test_case1():
    off =1
    A = 5
    B=4
    amp1 = Amp("off + A*s^2 +B*s^3","off,A,B,Max,Min",off,A,B,100,50)

    s = 2
    res1 = off + A*s**2 + B*s**3 
    res2 = amp1.inp(s)
    print res1,res2
    assert(res1==res2)


def test_case2():
    Ts = 1e-6
    amp1 = Amp("off + A*x","off,A,Max,Min",-0.5,3.0,2.0,0.0)
    vout1 = []
    vout2 = []
    
    for i in range(1000):
        in_ = (1.0/1000.0) * i
        amp1.inp(in_)
        vout1.append(in_)
        vout2.append(amp1.out)


    ax1 = plt.subplot(211)
    plt.plot(vout1)
    plt.subplot(212,sharex=ax1,sharey=ax1)
    plt.plot(vout2)    

    plt.ylim([-0.5,2.5])
    plt.show()



test_case2()
