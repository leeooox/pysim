import numpy as np

class EdgeMeasure:
    def __init__(self):
        self.out = 0.0
        #internal var
        self._prev_in = -1.0
        self._time_val = 0.0
        self._out_of_range_flag = 0



    def inp(self,_in):
        if ((_in < -1.0 or _in > 1.0) and self._out_of_range_flag == 0):
            self._out_of_range_flag = 1
            print("Warning in EdgeMeasure.inp:   in is < -1.0 or > 1.0")
            print("  in this case, in = %5.3f" %_in)

        # rising edge triggered
        if (self._prev_in == -1.0 and _in != -1.0):
            self.out = self._time_val + 1.0 - (_in - self._prev_in)/2.0
            self._time_val = (_in - self._prev_in)/2.0
        else:
            self._time_val += 1.0
            self.out = 0.0

        self._prev_in = _in

        return self.out
        
