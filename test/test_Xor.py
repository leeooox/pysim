import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Divider,Vco,Reg,Xor


if __name__ == "__main__":
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)
    divider = Divider()

    vout_vco = []
    vout_div = []
    vreg1_out = []
    vxor1_out = []
    vxor_not_out = []
    vxor3_out = []

    reg1 = Reg()
    xor1 = Xor()
    xor2 = Xor()
    xor3 = Xor()





    for i in range(10000):
        
        vin = 1e-4*i
        vco.inp(vin) #frequency will gradually increase since in is a ramp
        divider.inp(vco.out,10) # divide down VCO frequency by a factor of 10


        reg1.inp(divider.out,vco.out) 
        xor1.inp(divider.out,reg1.out)
        xor2.inp(-divider.out,reg1.out)
        xor3.inp(divider.out,-reg1.out)


        vout_vco.append(vco.out)
        vout_div.append(divider.out)
        vreg1_out.append(reg1.out)
        vxor1_out.append(xor1.out)
        vxor_not_out.append(-xor2.out)
        vxor3_out.append(xor3.out)
       

    ax1 = plt.subplot(611)
    plt.plot(vout_vco)
    plt.subplot(612,sharex=ax1,sharey=ax1)
    plt.plot(vout_div)
    plt.subplot(613,sharex=ax1,sharey=ax1)
    plt.plot(vreg1_out)
    plt.subplot(614,sharex=ax1,sharey=ax1)
    plt.plot(vxor1_out)
    plt.subplot(615,sharex=ax1,sharey=ax1)
    plt.plot(vxor_not_out)
    plt.subplot(616,sharex=ax1,sharey=ax1)
    plt.plot(vxor3_out)


    plt.ylim([-1.5,1.5])
    plt.show()



