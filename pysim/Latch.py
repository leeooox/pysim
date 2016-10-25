import numpy as np

class Latch:
    def __init__(self):
        self.out = -1.0
        #internal var
        self._outp =-1.0
        self._prev_clk = -1.0

        # the following is used only when reset is used
        self._prev_reset = -1.0
        self._clk_warning_flag = 0
        self._out_of_range_flag =0
        self._reset_transition_flag = 0 

    
    def init(_in):
        if ((_in != 1.0 and _in != -1.0) and self._out_of_range_flag == 0):
            self._out_of_range_flag = 1
            print("Warning in Latch.init:  input value is not 1.0 or -1.0")
            print("  in this case, input value = %5.3f" %_in)
        self._outp = _in
        self.out = _in

    def inp(self,_in,clk,_set=None,reset=None):
        if (not _set) and (not reset):
            self.out = self._outp
            self.inp_base(_in,clk)
        else:
            self.out = self._outp
            self.inp_base(_in,clk)
            self._outp = -self._outp
            self.inp_reset(_set)
            self._outp = -self._outp
            self.inp_reset(reset)

        return self.out



    def inp_reset(self,reset):
        if (reset != self._prev_reset and (self._prev_reset == 1.0 or self._prev_reset == -1.0)) :
        #reset transition
        #follow inp_base for reset low (-1.0), set low when reset is high (+1.0)
        #if (self._prev_reset == 1.0) transition from low - do nothing 
            if (self._prev_reset == -1.0): # transition to low - time according to reset
                if (self._outp == 1.0):
                    self._outp = -reset
                else:
                    self._outp = -1.0
        elif (reset == -1.0 or reset  == 1.0):
        #follow inp_base for reset low (-1.0), set low when reset is high (+1.0)
            if (reset == 1.0): # set outpput low
	            self._outp = -1.0;
        elif (self._reset_transition_flag == 0):
            self._reset_transition_flag = 1;
            print("Warning in 'Latch.inp_reset': reset transitions occurred in two consecutive samples")
            print("  or, reset is outp of its range:  -1.0 <= reset <= 1.0")
            print("  reset = %5.3f, prev_reset = %5.3f"%(reset,self._prev_reset))
            print("  probable issue:  need to have more samples per clock period")
        
        self._prev_reset = reset


    def inp_base(self,_in,clk):
        if (_in > 1.0 or _in < -1.0) and self._out_of_range_flag == 0:
            self._out_of_range_flag = 1
            print("Warning in Latch.inp:  in is constrained to be -1.0 <= in <= 1.0")
            print("  in this case, in = %5.3f" %_in);

        if (clk != self._prev_clk and (self._prev_clk == 1.0 or self._prev_clk == -1.0)): #clk transition
            # follow when clk is low (-1.0), hold when clk is high (+1.0)
            if self._prev_clk == 1.0: # transition from hold to follow
                self._outp = self._outp*clk if (_in !=self._outp) else self._outp 
            elif self._prev_clk == -1.0: # transition from follow to hold
                if _in == 1.0 and self._outp > 0.0:
	                self._outp = 1.0
                elif _in == -1.0 and  self._outp <= 0.0:
	                self._outp = -1.0
                else:
                    if self._outp <= 0.0: # in is transitioning from -1 to 1
                        self._outp = 1.0 if (clk<_in) else -1.0
                    else: # in is transitioning from 1 to -1
	                    self._outp = -1.0 if (clk<-_in)  else 1.0

        elif clk == -1.0 or clk  == 1.0 :
            # follow when clk is low (-1.0), hold when clk is high (+1.0)
            if (clk == -1.0): #follow
                self._outp = _in
            else: # hold
	            self._outp = 1.0 if (self._outp > 0.0) else -1.0
        elif self._clk_warning_flag == 0:
            print("Warning:  In 'Latch.inp': clk transitions occurred in two consecutive samples")
            print("  or, clk is out of its range:  -1.0 <= clk <= 1.0");
            print("  clk = %5.3f, prev_clk = %5.3f" %(clk,self._prev_clk))
            print("  probable issue:  need to have more samples per clock period")
            self._clk_warning_flag = 1

        self._prev_clk = clk

