import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Vco,Rand


def test_case1():
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)
    v1 = []
    v2 = []
    v3 = []

    rand1 = Rand("gauss")

    for i in range(10000):

        if i == 5000:
            rand1.reset()
        elif i == 7000:
            rand1.set_seed(2)

        vin = 1e-4*i

        noise1 = 0.01*rand1.inp() + 0.2

        vco.inp(vin+noise1)

        v1.append(vin+noise1)
        v2.append(noise1)
        v3.append(vco.out)


    ax1 = plt.subplot(311)
    plt.plot(v1)
    plt.ylabel("in")

    plt.subplot(312,sharex=ax1)
    plt.plot(v2)
    plt.ylabel("noise")

    plt.subplot(313,sharex=ax1)
    plt.plot(v3)
    plt.ylabel("vco")
    #plt.ylim([-1.5,1.5])
    plt.show()


def test_case2():

    rand1 = Rand("gauss")
    vout = []
    for i in range(10000):
        if i == 5000:
            rand1.reset()
        elif i == 7000:
            rand1.set_seed(2)

        noise1 = 0.01*rand1.inp() + 0.2

        vout.append(noise1)

    plt.plot(vout)
    plt.show()


if __name__ == "__main__":
    test_case1()
