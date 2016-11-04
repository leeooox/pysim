import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Filter

def test_case1():
    list1 = [1.0,-2.0,1.0]
    #double_accum = Filter("1",list1)
    Filter("3+4*z^-1+5*z^-2","6+7*z^-1+8*z^-2","Ts",1e-9)

def test_case2():
    int_filt = Filter("3+4*s+5*s^2","6+7*s+8*s^2","Ts",1e-9)

    print int_filt.inp(0.2)
    
    print int_filt.inp(0.3)
    int_filt.reset(0)
    print int_filt.inp(0.4)

def test_case3():
    int_filt = Filter("3 + 8.1*s^3 - 5.2*s^5","6.3+2.4*s^2+3.5*s^3","Ts",1e-9)


def test_case4():
    list1 = [1.0,-2.0,1.0]
    double_accum = Filter("1",list1)   
    first_diff =Filter("1-z^-1","1")

    v1 = []
    v2 = []
    v3 = []

    in_  = 1.0
    for i in range(1000):
        if i==200:
            in_ = -1.0
        elif i==400:
            in_ = 2.0
        elif i==700:
            double_accum.reset(0.0)
            first_diff.reset(0.0)
        # cascade
        double_accum.inp(in_)
        first_diff.inp(double_accum.out)
        v1.append(in_)
        v2.append(double_accum.out)
        v3.append(first_diff.out)

    ax1 = plt.subplot(311)
    plt.plot(v1)
    plt.subplot(312,sharex=ax1)
    plt.plot(v2)    
    plt.subplot(313,sharex=ax1)
    plt.plot(v3)    



    plt.show()
    
def test_case5():
    sample_per = 1e-6
    double_integ = Filter("K","s^2","K,Ts",1e5,sample_per)   
    diff =Filter("s","1","Ts",sample_per)

    v1 = []
    v2 = []
    v3 = []

    in_  = 1.0
    for i in range(1000):
        if i==200:
            in_ = -1.0
        elif i==400:
            in_ = 2.0
        elif i==700:
            double_integ.reset(0.0)
            diff.reset(0.0)
        # cascade
        double_integ.inp(in_)
        diff.inp(double_integ.out)
        v1.append(in_)
        v2.append(double_integ.out)
        v3.append(diff.out)

    ax1 = plt.subplot(311)
    plt.plot(v1)
    plt.subplot(312,sharex=ax1)
    plt.plot(v2)    
    plt.subplot(313,sharex=ax1)
    plt.plot(v3)    



    plt.show()
        
def test_case6():
    sample_per = 1e-6
    double_integ = Filter("K","s^2","K,Ts",1e5,sample_per)   
    diff =Filter("s","1","Ts",sample_per)

def test_case7():
    # a RC filter
    Ts = 1.0/4e3
    r = 10e3
    c = 100e-6

    RC_filter = Filter("1","1+r*c*s","r,c,Ts",r,c,Ts)

    vin = 0.0
    v1 = []
    v2 = []
    for i in range(-4000,20000):
        if i>0:
            vin =10.0
        RC_filter.inp(vin)
        v1.append(vin)
        v2.append(RC_filter.out)

    #t = np.arange
    t = np.arange(-4000,20000)*Ts
    plt.plot(t,v1,label="Va")
    plt.plot(t,v2,label="Vb")
    plt.grid()
    plt.ylim([-1,11])
    plt.legend(loc="best")
    plt.show()

test_case7()
