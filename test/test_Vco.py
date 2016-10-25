import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Vco


if __name__ == "__main__":
    vco = Vco(1e7,1e6,1e-9)
    vout = []
    phase_out = []

    vco2 = Vco(1e7,1e6,1e-9)
    vout2 = []

    for i in range(10000):
        vin = 1e-4*i
        vout.append(vco.inp(vin))
        vout2.append(vco2.inp(vin,3))

        phase_out.append(np.sin(vco.phase))
    #print vout 

    ax1 = plt.subplot(311)
    plt.plot(vout)

    plt.subplot(312,sharex=ax1,sharey=ax1)
    plt.plot(phase_out)

    plt.subplot(313,sharex=ax1,sharey=ax1)
    plt.plot(vout2)
    plt.ylim([-1.5,1.5])
    #np.savetxt("pyvout.txt",vout)
    plt.show()