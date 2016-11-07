import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import SigGen,Vco,Reg,Filter,And


def test_classical_synthesizer():
    Ts = 1.0/200e6

    vco = Vco("fc + Kv*x","fc,Kv,Ts",1.84e9,30e6,Ts)
    ref_clk = SigGen("square",20e6,Ts)
    reg1 = Reg()
    reg2 = Reg()
    and1 = And()
    
    rc_filter = Filter("1.0","1+1/(2*pi*fp)*s","fp,Ts",127.2e3,Ts)
    int_filter = Filter("2*pi*fp/10","s","fp,Ts",127.2e3,Ts)


    v1 = []
    v2 = []

    N = 90
    for i in xrange(200000):
        if i==160000:
            N += 1
        ref_clk.inp(0.0) # set jitter to zero
        
        #PFD
        reg1.inp(1.0,vco.out,-1.0,and1.out)
        reg2.inp(1.0,ref_clk.out,-1.0,and1.out)
        and1.inp(reg1.out,reg2.out)


        # charge pump
        chp_out = (reg2.out-reg1.out)*0.1989*np.pi

        #loop filter
        rc_filter.inp(chp_out)
        int_filter.inp(chp_out)
        vco_in = rc_filter.out + int_filter.out

        #VCO
        vco.inp(vco_in,N)

        #
        v1.append(N)
        v2.append(vco_in)
 
    ax1 = plt.subplot(211)
    plt.plot(v1)
    plt.subplot(212,sharex=ax1)
    plt.plot(v2)


    #plt.ylim([-0.5,2.5])
    plt.show()


test_classical_synthesizer()
