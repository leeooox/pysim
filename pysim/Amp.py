import numpy as np
from Poly import Poly

class Amp:
    def __init__(self,*args,**kwargs):
        self.out = 0.0
        self.poly_gain = Poly(*args,**kwargs)

    def set(*args,**kwargs):
        self.poly_gain.set(*args,**kwargs)

    def inp(self,in_):
        self.out = np.sum(self.poly_gain.coeff*np.power(in_,self.poly_gain.exp))
        self.out = np.min([self.out,self.poly_gain.max_])
        self.out = np.max([self.out,self.poly_gain.min_])
        return self.out



