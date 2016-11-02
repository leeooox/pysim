import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Divider,Vco,Latch


if __name__ == "__main__":
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)
    divider = Divider()

    vout_vco = []
    vout_div = []
    vreg1_out = []
    vreg2_out = []

    latch1 = Latch()
    latch2 = Latch()
    latch3 = Latch()
    latch4 = Latch()

    for i in range(10000):
        
        vin = 1e-4*i
        vco.inp(vin) #frequency will gradually increase since in is a ramp
        divider.inp(vco.out,10) # divide down VCO frequency by a factor of 10


        latch1.inp(divider.out,vco.out) # first latch of register
        latch2.inp(latch1.out,-vco.out) # second latch of register; note clk is inverted




        latch3.inp(divider.out,vco.out,-1.0,latch2.out) # first latch of register
        latch4.inp(latch3.out,-vco.out,-1.0,latch2.out) # second latch of register
        

        vout_vco.append(vco.out)
        vout_div.append(divider.out)
        vreg1_out.append(latch2.out)
        vreg2_out.append(latch4.out)

    ax1 = plt.subplot(411)
    plt.plot(vout_vco)
    plt.subplot(412,sharex=ax1,sharey=ax1)
    plt.plot(vout_div)
    plt.subplot(413,sharex=ax1,sharey=ax1)
    plt.plot(vreg1_out)
    plt.subplot(414,sharex=ax1,sharey=ax1)
    plt.plot(vreg2_out)


    plt.ylim([-1.5,1.5])
    plt.show()



