import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import SigGen,Rand,Vco,Reg,Latch,Filter,Xor,EdgeMeasure


def test_BBCDR():
    Ts = 1.0/15e9

    vco = Vco("fc + Kv*x","fc,Kv,Ts",2.5e9,50e6,Ts)
    prbs_data = SigGen("prbs",2.502e9,Ts)
    reg1 = Reg()
    reg2 = Reg()
    reg3 = Reg()
    latch1 = Latch()

    xor1 = Xor()
    xor2 = Xor()

    int_filter = Filter("2*pi*40e9","s","Ts",Ts)

    vco_period = EdgeMeasure()
    in_period = EdgeMeasure()

    randg = Rand("gauss")

    # VCO noise
    N_dBc = -90.0 # -90dBc/Hz at 1MHz offset
    f_off = 1e6
    Kv = 50e6

    noise_var = np.power(10,N_dBc/10.0)*np.power(f_off/Kv,2)
    

    v1 = []
    v2 = []
    v3 = []
    v4 = []
    v5 = []


    for i in range(300000):
        in_ = prbs_data.inp(0.0) # set jitter to zero
        
        # Bang-bang PD
        reg1.inp(in_,vco.out)
        reg2.inp(reg1.out,vco.out)
        reg3.inp(in_,-vco.out)
        latch1.inp(reg3.out,-vco.out)
        xor1.inp(reg1.out,latch1.out)
        xor2.inp(reg2.out,latch1.out)

        pd_out = xor1.out-xor2.out

        # charge pump

        chp_out = 1e-6*pd_out

        #loop filter
        vco_in = int_filter.inp(chp_out) +chp_out*125e3
        vco_in += np.sqrt(noise_var/Ts)*randg.inp() # add VCO noise

        #VCO
        vco.inp(vco_in)

        #
        v1.append(vco_period.inp(vco.out))
        v2.append(in_period.inp(prbs_data.square))
        v3.append(int_filter.out)
        v4.append(pd_out)
        v5.append(prbs_data.out)

    ax1 = plt.subplot(411)
    plt.plot(v1)
    plt.subplot(412,sharex=ax1)
    plt.plot(v2)

    plt.subplot(413,sharex=ax1)
    plt.plot(v3)
    plt.subplot(414,sharex=ax1)
    plt.plot(v4)

    #plt.ylim([-0.5,2.5])
    plt.show()

def test_BBCDR2():
    Ts = 1.0/15e9
    print Ts

    prbs_data = SigGen("prbs",2.502e9,Ts)


    v1 = []



    for i in range(20000):
        in_ = prbs_data.inp(0.0) # set jitter to zero
        
        v1.append(prbs_data.out)

    ax1 = plt.subplot(111)
    plt.plot(v1)


    #plt.ylim([-0.5,2.5])
    plt.show()

test_BBCDR()
