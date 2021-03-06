import numpy as np
import matplotlib.pyplot as plt
import os
os.sys.path.append("../.")
from pysim import Poly

def test_case1():
    poly1 = Poly([3,4,5])


    print poly1.coeff
    print poly1.exp
    print poly1.num_coeff

def test_case2():
    poly1 = Poly([-2,100,22])


    print poly1.coeff
    print poly1.exp
    print poly1.num_coeff

def test_case3():
    poly1 = Poly([-1.2e-12,-120,22])


    print poly1.coeff
    print poly1.exp
    print poly1.num_coeff

def test_case4():
    poly1 = Poly([-1.2e-9,-120,22])


    print poly1.coeff
    print poly1.exp
    print poly1.num_coeff

def test_case5():
    #poly1 = Poly("1+ f0*w0*s^2 + b*s^3","f0,w0,a,b",3,5,6,8)
    poly1 = Poly("1+ 2*pi*s^2 + b*s^3","f0,w0,a,b",3,5,6,8)

    #print poly1._get_ivar("1+s^2+s^(-1/2)","a,b")
    #print poly1._get_ivar("1+s^2+s^(-1/2)","s,b")
    #print poly1._get_ivar("1+2*s","s,b")
    #print poly1._get_ivar("1+2*s","a,b")
    #print poly1._get_ivar("2*s+2","a,b")

def test_case6():
    Ts = 1e-9
    poly1 = Poly("fc + Kv*s","fc,Kv,Ts",10,2,Ts)
    print poly1.coeff
    print poly1.exp
    print poly1.ivar

def test_case7():
    print "case7"
    poly1 = Poly("1+3")
    print poly1.coeff
    print poly1.exp

def test_case8():
    print "case8"
    poly1 = Poly("Fc+1","Fc",1e3)
    print poly1.coeff
    print poly1.exp
    print poly1.ivar

def test_case9():
    print "case9"
    poly1 = Poly("1-z^-1")

    print poly1.coeff
    print poly1.exp
    print poly1.ivar

def test_case10():
    print "case10"
    poly1 = Poly("1")

    print poly1.coeff
    print poly1.exp
    print poly1.ivar

def test_case11():
    print "case11"
    poly1 = Poly("1+2","Ts",1e-6) 

    print poly1.coeff
    print poly1.exp
    print poly1.ivar
def test_case12():
    print "case12"
    poly1 = Poly("s^2","K,Ts",1e5,1e-6) 

    print poly1.coeff
    print poly1.exp
    print poly1.ivar

def test_case13():
    poly1 = Poly("K","K,Ts",1e5,1e-6) 
    print poly1._get_ivar("K","K,Ts")
    print poly1.coeff
    print poly1.exp
    print poly1.ivar

test_case7()
test_case8()
test_case9()
test_case10()
test_case11()
test_case12()
test_case13()
