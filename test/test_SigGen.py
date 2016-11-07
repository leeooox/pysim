import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import SigGen,Rand


def test_case1():
    Ts = 1e-9
    freq = 1e6
    list1 = [1,-1,-1]
    sine1 = SigGen("sine",freq,Ts)
    sine2 = SigGen("sine",freq,Ts)
    prbs1 = SigGen("prbs",freq,Ts,list1,0)
    prbs2 = SigGen("prbs",freq,Ts)
    rand1 = Rand("gauss")

    v1 = []
    v2 = []
    v3 = []
    v4 = []

    for i in range(20000):
        if i == 5000:
            sine1.reset()
        sine1.inp(0.0)
        sine2.inp(0.25)
        prbs1.inp(0.0)
        prbs2.inp(0.0001*rand1.inp())

        v1.append(sine1.out)
        v2.append(sine2.out)
        v3.append(prbs1.out)
        v4.append(prbs2.out)

    ax1 = plt.subplot(411)
    plt.plot(v1)
    plt.subplot(412,sharex=ax1,sharey=ax1)
    plt.plot(v2)
    plt.subplot(413,sharex=ax1,sharey=ax1)
    plt.plot(v3)
    plt.subplot(414,sharex=ax1,sharey=ax1)
    plt.plot(v4)
    plt.ylim([-1.5,1.5])



    plt.show()

test_case1()
