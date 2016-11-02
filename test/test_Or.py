import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Divider,Vco,Reg,Or


if __name__ == "__main__":
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)
    divider = Divider()

    vout1 = []
    vout2 = []
    vout3 = []
    vout4 = []
    vout5 = []
    vout6 = []

    reg1 = Reg()
    or1 = Or()
    or2 = Or()
    or3 = Or()





    for i in range(10000):
        
        vin = 1e-4*i
        vco.inp(vin) #frequency will gradually increase since in is a ramp
        divider.inp(vco.out,10) # divide down VCO frequency by a factor of 10


        reg1.inp(divider.out,vco.out) 
        or1.inp(divider.out,reg1.out)
        or2.inp(-divider.out,reg1.out)
        or3.inp(vco.out,-reg1.out,or1.out,or2.out)


        vout1.append(vco.out)
        vout2.append(divider.out)
        vout3.append(reg1.out)
        vout4.append(or1.out)
        vout5.append(-or2.out)
        vout6.append(or3.out)
       

    ax1 = plt.subplot(611)
    plt.plot(vout1)
    plt.subplot(612,sharex=ax1,sharey=ax1)
    plt.plot(vout2)
    plt.subplot(613,sharex=ax1,sharey=ax1)
    plt.plot(vout3)
    plt.subplot(614,sharex=ax1,sharey=ax1)
    plt.plot(vout4)
    plt.subplot(615,sharex=ax1,sharey=ax1)
    plt.plot(vout5)
    plt.subplot(616,sharex=ax1,sharey=ax1)
    plt.plot(vout6)


    plt.ylim([-1.5,1.5])
    plt.show()



