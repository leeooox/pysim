import numpy as np

class Divider:
    def __init__(self):
        self.out = 0.0
        #internal var
        self._cycle_count =0
        self._state = 0
        self._prev_in =0.0
        self._high_count = 1
        self._low_count = 1

        self._prev_divide_val = 0
        self._divide_trans_count = -1 
        self._trans_warning_flag = 0
        self._divide_val_flag = 0


    def inp(self,in_,divide_value):
        if np.abs(np.floor(divide_value)-divide_value) >1e-2:
                err_msg = "error in Divider.inp:  divide value is far from integer\nin this case, divide value = %5.3f" %divide_val
                raise Exception(err_msg)
        
        divide_value = int(np.floor(divide_value))

        if self._prev_in == -1.0 and in_ != -1.0:
            self._cycle_count += 1

        if divide_value != self._prev_divide_val:
            self._divide_trans_count += 1

        self._prev_divide_val = divide_value
        
        if self._divide_trans_count>1 and self._trans_warning_flag ==0:
            print("warning: in Divider.inp  divide value transitioned more than once")
            print("  during one cycle of divider output")
            self._trans_warning_flag = 1
            
        if self._state == 0: # low state
            if self._cycle_count == self._low_count:
                if divide_value < 2:
                    if self._divide_val_flag == 0:
                        self._divide_val_flag = 1
                        print("Warning in Divider.inp:  divide_value must be > 1")
                        print("  in this case, divide_value = %d" %divide_value)
                        print("  setting divide value to 2 whenever it drops below 2")
                    divide_value = 2

                self._high_count = divide_value/2
                self._low_count = divide_value -  self._high_count
                self._divide_trans_count = 0
                self._cycle_count = 0
                self._state = 1
                self.out = in_
            else:
                self.out = -1.0
        else:
            if self._cycle_count == self._high_count:
                self._cycle_count = 0
                self._state = 0;
                self.out = -in_
            else:
                self.out = 1.0



        self._prev_in = in_
        return self.out
        
