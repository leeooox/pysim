from __future__ import division
import numpy as np
from Rand import Rand
from Reg import Reg
from Filter import Filter


class cir_list:
    def __init__(self,mylist,start_entry=0):
        self._start_entry = start_entry
        self.idx = start_entry
        self.length= len(mylist)
        self.mylist=mylist
    def read(self):
        out = self.mylist[self.idx]

        self.idx += 1
        if self.idx >= self.length:
            self.idx = 0
            
        return out

    def reset(self):
        self.idx = self._start_entry
        

class SigGen:
    def __init__(self,type_,freq,Ts,other=None,start_entry=None):
        '''
        @type_, string, which could be "square", "sine", "prbs", "impulse"
        @freq, float, which is the data rate

        '''
        self.out = -1.0
        self.phase = 0.0
        self.square = 1.0


        self._rand1 = Rand("bernoulli")
        self._reg1 = Reg()
        #self.phase_filt = Filter


        self._clk_state = 0
        self._prev_phase = 0.0
        self._prev_square = 1.0
        self._data = 1.0
        self._prev_data = 1.0
        self._prev_in = 0.0
        self._first_entry_flag = 1
        self._end_data_flag = 0
        self._data_seq = cir_list([])

        self.set(type_,freq,Ts,other,start_entry)
        
    def reset(self):

        self._clk_state = 0
        self._prev_phase = -(self._sample_period*self._frequency)/2.0
        self.phase = self._prev_phase
        self.out = 0.0
        self._prev_square = 1.0
        self.square = 1.0
        self._data = 1.0
        self._prev_data = 1.0
        self._prev_in = 0.0
        self._first_entry_flag = 1
        self._end_data_flag = 0
        self._data_seq.reset()
        self._phase_filt.reset(0.0)





    def set(self,type_,freq,Ts,other=None,start_entry=0):
        self._sample_period = Ts
        self._frequency = freq
        self._phase_filt = Filter("a","1 - (1-a)*z^-1","a",0.5*freq*Ts)

        if start_entry and start_entry <0:
            err_msg  = "error in SigGen.set:  starting entry for List input must be >= 0\n"
            err_msg += "   (note that a value of 1 corresponds to the first entry)\n"
            err_msg += "   in this case, start_entry = %d\n" %start_entry
            raise Exception(err_msg)
            
        if self._sample_period < 1e-30:
            err_msg  = "error in SigGen.set:  Ts < 1e-30\n"
            err_msg += "   in this case, Ts = %5.3e\n" %Ts
            raise Exception(err_msg)

        if freq < 0.0:
            err_msg  = "error in SigGen.set:  freq <= 0.0\n"
            err_msg += "   in this case, freq = %5.3e\n" %freq
            raise Exception(err_msg)

        if type_ == "square":
            self._type_flag = 0
        elif type_ == "sine":
            self._type_flag = 1
        elif type_ == "prbs":
            self._type_flag = 2
        elif type_ == "impulse":
            self._type_flag = 3
        else:
            err_msg  = "error in SigGen.set:  type must be either\n"
            err_msg += "  'square', 'sine', 'prbs', or 'impulse'\n"
            err_msg += "  in this case, type = '%s'\n" %type_
            raise Exception(err_msg)

        if other:
            self._end_data_flag = 0
            self._prev_data =1.0
            self._data_seq = cir_list(other,start_entry)
            self._data = 1.0 if self._data_seq.read() >0.0 else -1.0

            
            if self._data != -1.0 and self._data != 1.0:
                print "error in SigGen.set:  data list has values that are not 1.0 or -1.0"
                print "  in this case, the data value is %5.3f" %self._data 
            
            if self._type_flag == 2:
                self._reg1.init(self._data)
                self._data = 1.0 if self._data_seq.read() >0.0 else -1.0
                if self._data != -1.0 and self._data != 1.0:
                    print "error in SigGen.set:  data list has values that are not 1.0 or -1.0"
                    print "  in this case, the data value is %5.3f" %self._data 

            self._prev_data = self._data

    def inp(self,in_):
        if self._first_entry_flag == 1:
            self._prev_in = 0.0
            self._phase_filt.reset(in_)
            self._prev_phase = -1.0 # start one cycle back
            self._first_entry_flag =0
        elif (in_ - self._prev_in) <-1.0 or (in_ - self._prev_in)>1.0:
            err_msg  = "error in SigGen.inp: input phase cannot change\n"
            err_msg += "     instantaneously by more than a cycle\n"
            err_msg += "  i.e.,  -1.0 <= delta in <= 1.0\n"
            err_msg += "  in this case, in = %5.4f, prev_in = %5.4f, delta in = %5.4f\n" %(in_,self._prev_in,in_-self._prev_in)
            raise Exception(err_msg)
        self._phase_filt.inp(in_)
        #print self.phase, self._prev_phase, self._sample_period,self._frequency, self._phase_filt.out,self._prev_in
        self.phase = self._prev_phase + self._sample_period*self._frequency - (self._phase_filt.out-self._prev_in)
        #print self.phase 
        if self.phase >=1.0:
            self.phase -= 1.0

        #state = 0:  clk phase between 0.5 and 1.0
        #state = 1:  clk phase between 0 and 0.5


        if self._prev_phase >= self.phase:
            self._prev_phase -= 1.0

        if self.phase >= 0.0 and self.phase < 0.5: #state=1
            if self._clk_state == 1: # stay in state 1
                self.square = 1.0
            else: #transition from state=0 to state=1
                self.square = (self.phase+self._prev_phase)/(self.phase-self._prev_phase)
            self._clk_state = 1
            impulse = .5*(self.square-self._prev_square)
        else: #state = 0 
            if self._clk_state == 0: # stay in state 0
                self.square = -1.0
            else: #transition from state=1 to state=0
                self.square = (1.0-self.phase -self._prev_phase)/(self.phase-self._prev_phase)
            self._clk_state = 0
            impulse = 0.0

        if self.square < -1.0 and self.square >1.0:

            err_msg  = "error in SigGen.inp:  interpolated output beyond -1 to 1 range\n"
            err_msg += "  in this case, square out = %5.3f\n" %self.square
            err_msg += "  probable cause:  input inappropriate\n"
            err_msg += "  in this case, in = %5.3f\n" %in_
            raise Exception(err_msg)

        if self._type_flag == 0: # square
            self.out = self.square
        elif self._type_flag == 1: # sine
            self.out = np.sin(2*np.pi*self.phase)
        elif self._type_flag == 2: # prbs
            self.out = self._reg1.out
        elif self._type_flag == 3: # impulse
            self.out = impulse*self._data
        else:
            err_msg  = "error in SigGen.inp:  type_flag not recognized\n"
            err_msg += "  in this case, type_flag = %d\n" %self._type_flag
            raise Exception(err_msg)

        self._reg1.inp(self._data,self.square) 

        if self.square == 1.0 and self._prev_square != 1.0: # impulse has finished transitioning
            if self._data_seq.length == 0:
                self._data = self._rand1.inp()
            elif self._end_data_flag == 0:
                self._data = self._data_seq.read()
            if self._data != -1.0 and self._data != 1.0:
                self._data = self._prev_data
                self._end_data_flag = 1
            else:
                self._data = 1.0 if self._data > 0.0 else -1.0
                self._prev_data = self._data

        self._prev_square = self.square
        self._prev_in = self._phase_filt.out
        self._prev_phase = self.phase

        return self.out

            
if __name__ == "__main__":
    a = [5,6,7]
    a_seq = cir_list(a,2)
    for i in range(10):
        print a_seq.read()
