import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Divider,Vco


if __name__ == "__main__":
    Ts = 1e-9
    vco = Vco(1e7,1e6,Ts)
    div1 = Divider()

    vout_vco = []
    vout_div = []

    for i in range(10000):
        vin = 1e-4*i
        vco.inp(vin) #frequency will gradually increase since in is a ramp
        div1.inp(vco.out,10) # divide down VCO frequency by a factor of 10
        vout_vco.append(vco.out)
        vout_div.append(div1.out)


    ax1 = plt.subplot(211)
    plt.plot(vout_vco)
    plt.subplot(212,sharex=ax1,sharey=ax1)
    plt.plot(vout_div)
    plt.ylim([-1.5,1.5])
    plt.show()


