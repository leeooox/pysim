import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Divider,Vco,EdgeMeasure

if __name__ == "__main__":
    Ts = 1e-9
    vco = Vco("fc + Kv*x","fc,Kv,Ts",10e6,1e6,Ts)
    divider = Divider()

    vout1 = []
    vout2 = []
    vout3 = []
    vout4 = []

    edge_time1 = EdgeMeasure()
    edge_time2 = EdgeMeasure()





    for i in range(10000):
        
        vin = 1e-4*i
        vco.inp(vin) #frequency will gradually increase since in is a ramp
        divider.inp(vco.out,10) # divide down VCO frequency by a factor of 10


        vout1.append(vco.out)
        vout2.append(divider.out)
        vout3.append(edge_time1.inp(vco.out))
        vout4.append(edge_time2.inp(divider.out))
       

    ax1 = plt.subplot(411)
    plt.plot(vout1)
    plt.subplot(412,sharex=ax1,sharey=ax1)
    plt.plot(vout2)
    plt.subplot(413,sharex=ax1,sharey=ax1)
    plt.plot(vout3)
    plt.subplot(414,sharex=ax1,sharey=ax1)
    plt.plot(vout4)


    #plt.ylim([-1.5,1.5])
    plt.show()



