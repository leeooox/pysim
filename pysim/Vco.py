import numpy as np
import matplotlib.pyplot as plt

class Vco:

    def __init__(self,fc,Kv,Ts):
        # this simplified as 1st order VCO
        self.fc = fc # Vco center frequency
        self.Kv = Kv # Kvco value
        self.sample_period = Ts # this Ts
        
        self.out = 0.0 # voltage
        self.phase = 0.0 # phase as internal

        # internal private var
        self._prev_phase = 0.0
        self._clk_state = 1 # int
        self._divide_scale = -1.0 # for what?
        

        self._prev_divide_val = 0 # int
        self._divide_trans_count = -1 # int
        self._trans_warning_flag = 0 #
        self._divide_val_warning_flag = 0 #
        self._out_of_range_flag = 0 #



        if self.sample_period < 1e-30:
            print("error in Vco Constructor:  sample_period can't be < 1e-30")

    def inp(self,_in,divide_val=1):
        if divide_val == 1:
            return self.inp_nodiv(_in)
        else:
            if np.abs(np.floor(divide_val)-divide_val) >1e-2:
                #print("error in Vco.inp:  divide value is far from integer")
                #print(" in this case, divide value = %5.3f" %divide_val)
                err_msg = "error in Vco.inp:  divide value is far from integer\nin this case, divide value = %5.3f" %divide_val
                raise Exception(err_msg)

            return self.inp_div(_in,divide_val)


    def inp_nodiv(self,_in):
        '''@in, is a double value, which is Vco Vctrl voltage value
        '''

        self.phase = self._prev_phase + self.sample_period*2.0*np.pi*(self.fc+self.Kv*_in)
        
        if self.phase >= 2*np.pi:
            self.phase -= 2*np.pi

        if self._prev_phase >= self.phase:
            self._prev_phase -= 2*np.pi

        # state = 0:  clk phase between PI and 2*PI
        # state = 1:  clk phase between 0 and PI
        
        if self.phase >= 0.0 and self.phase < np.pi: # state = 1 
            if self._clk_state == 1: #stay in state 1
                self.out = 1.0
            else:  # transition from state=0 to state=1
                self.out = (self.phase+self._prev_phase)/(self.phase-self._prev_phase)
            self._clk_state = 1

        else: #state = 0
            if self._clk_state == 0: # stay in state 0
                self.out = -1.0
            else: # transition from state=1 to state=0 
                self.out = (2*np.pi-(self.phase+self._prev_phase))/(self.phase-self._prev_phase)
            self._clk_state = 0

        self._prev_phase = self.phase

        if (self.out < -1.0 or self.out > 1.0) and self._out_of_range_flag == 0:
            self._out_of_range_flag = 1
            print("Warning in Vco.inp:  interpolated output has value beyond -1 to 1 range")
            print("  in this case, out = %5.3f" %self.out);
            print("  probable cause:  input inappropriate");
            print("  in this case, in = %5.3f\n" %_in);

        return self.out 

    def inp_div(self,_in,divide_val):
        '''a divider
        @_in, float,voltage waveform input
        @divide_val, int
        '''
        if divide_val != self._prev_divide_val:
            self._divide_trans_count += 1

        self._prev_divide_val = divide_val



        if self._divide_trans_count>1 and self._trans_warning_flag ==0:
            self._trans_warning_flag = 1
            print("warning in Vco.inp:  divide value transitioned more than once")
            print("  during one cycle of Vco output")


        if self._divide_scale < 1.0:
            self._divide_scale = float(divide_val)    

        if self.sample_period*(self.fc+self.Kv*_in) > self._divide_scale/2.0:
            if self._divide_val_warning_flag == 0:
                self._divide_val_warning_flag = 1
                print("Warning in Vco.inp:  divide_val is too small for the given sample rate!")
                print("  in this case, divide_val = '%d', and should be >= '%d'" %(divide_val,int(4*sample_period*(self.fc+self.Kv*_in))))
                printf("  -> setting divide val to '%d' whenever it is too small" %int(4*self.fc+self.Kv*_in))

            divide_val = int(4*sample_period*(self.fc+self.Kv*_in))


        self.phase = self._prev_phase + self.sample_period*2.0*np.pi*(self.fc+self.Kv*_in)
        
        if self.phase >= 2*np.pi*self._divide_scale:
            self.phase -= 2*np.pi*self._divide_scale
            if self._prev_phase > self.phase:
                self._prev_phase -= 2*np.pi*self._divide_scale
            self._divide_scale = float(divide_val)
            self._divide_trans_count = 0


        # state = 0:  clk phase between PI and 2*PI
        # state = 1:  clk phase between 0 and PI
        
        if self.phase >= 0.0 and self.phase < np.pi*self._divide_scale: # state = 1 
            if self._clk_state == 1: #stay in state 1
                self.out = 1.0
            else:  # transition from state=0 to state=1
                self.out = (self.phase+self._prev_phase)/(self.phase-self._prev_phase)
            self._clk_state = 1

        else: #state = 0
            if self._clk_state == 0: # stay in state 0
                self.out = -1.0
            else: # transition from state=1 to state=0 
                self.out = (2*np.pi*self._divide_scale-(self.phase+self._prev_phase))/(self.phase-self._prev_phase)
            self._clk_state = 0

        self._prev_phase = self.phase

        if (self.out < -1.0 or self.out > 1.0) and self._out_of_range_flag == 0:
            self._out_of_range_flag = 1
            print("Warning in Vco.inp:  interpolated output has value beyond -1 to 1 range")
            print("  in this case, out = %5.3f" %self.out);
            print("  in this case, in = %5.3f, divide value = %d" %(_in,divide_val))
            print("  also, make sure divide value is not changing more than once")
            print("  per VCO cycle")


        return self.out 




