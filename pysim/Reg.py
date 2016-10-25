from Latch import Latch

class Reg:
    def __init__(self):
        self.out = -1.0

        # internal var
        self._out_of_range_flag =0

        self.lat1 = Latch()
        self.lat2 = Latch()

    def init(_in):
        if ((_in != 1.0 and _in != -1.0) and out_of_range_flag == 0):
            self._out_of_range_flag = 1
            print("Warning in Reg.init:  input value is not 1.0 or -1.0")
            print("  in this case, input value = %5.3f" %_in)
    
        self.lat1.init(_in)
        self.lat2.init(_in)
        self.out = _in

    def inp(self,_in,clk,_set=None,reset=None):
        self.lat1.inp(_in,clk,_set,reset)
        self.lat2.inp(self.lat1.out,-clk,_set,reset)
        self.out = self.lat2.out
        return self.out




