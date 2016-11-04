from Latch import Latch

class Reg:
    def __init__(self):
        self.out = -1.0

        # internal var
        self._out_of_range_flag =0

        self.lat1 = Latch()
        self.lat2 = Latch()

    def init(self,in_):
        if ((in_ != 1.0 and in_ != -1.0) and out_of_range_flag == 0):
            self._out_of_range_flag = 1
            print("Warning in Reg.init:  input value is not 1.0 or -1.0")
            print("  in this case, input value = %5.3f" %in_)
    
        self.lat1.init(in_)
        self.lat2.init(in_)
        self.out = in_

    def inp(self,in_,clk,set_=None,reset=None):
        self.lat1.inp(in_,clk,set_,reset)
        self.lat2.inp(self.lat1.out,-clk,set_,reset)
        self.out = self.lat2.out
        return self.out




