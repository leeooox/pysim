import numpy as np

class EdgeMeasure:
    def __init__(self):
        self.out = 0.0
        #internal var
        self._prev_in = -1.0
        self._time_val = 0.0
        self._out_of_range_flag = 0



    def inp(self,in_):
        if ((in_ < -1.0 or in_ > 1.0) and self._out_of_range_flag == 0):
            self._out_of_range_flag = 1
            print("Warning in EdgeMeasure.inp:   in is < -1.0 or > 1.0")
            print("  in this case, in = %5.3f" %in_)

        # rising edge triggered
        if (self._prev_in == -1.0 and in_ != -1.0):
            self.out = self._time_val + 1.0 - (in_ - self._prev_in)/2.0
            self._time_val = (in_ - self._prev_in)/2.0
        else:
            self._time_val += 1.0
            self.out = 0.0

        self._prev_in = in_

        return self.out
        
