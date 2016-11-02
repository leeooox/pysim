import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Vco


def test_case1():
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)
    vout = []
    phase_out = []

    vco2 = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)
    vout2 = []

    for i in range(10000):
        vin = 1e-4*i
        vout.append(vco.inp(vin))
        vout2.append(vco2.inp(vin,3))

        phase_out.append(np.sin(vco.phase))
    #print vout 

    ax1 = plt.subplot(311)
    plt.plot(vout)
    plt.ylabel("square")

    plt.subplot(312,sharex=ax1,sharey=ax1)
    plt.plot(phase_out)
    plt.ylabel("sine")

    plt.subplot(313,sharex=ax1,sharey=ax1)
    plt.plot(vout2)
    plt.ylabel("square3")
    plt.ylim([-1.5,1.5])
    plt.show()

def test_case2():
    Ts = 1e-40
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)

def test_case3():
    vco = Vco("fc + Kv*x","fc,Kv",10e6,1e6)

def test_case4():
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts) 
    vco.set("fc + Kv*x","fc,Kv,Ts",10e6,1e6,1e-10)
    print vco._sample_period

def test_case5():
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts) 
    vco.set_phase(2)


if __name__ == "__main__":
    test_case5()
