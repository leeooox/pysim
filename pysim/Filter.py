from __future__ import division
import numpy as np
from Poly import Poly
from Const import NaN



class Filter:
    def __init__(self,*args,**kwargs):

        self.num_a_coeff = 0
        self.num_b_coeff = 0
        self.out = 0.0

        #internal var
        self._num_x_samples = 0
        self._num_y_samples = 0

        self._x_samples_pointer = 0 
        self._y_samples_pointer = 0

        self._max_out = 0
        self._min_out = 0

        self.set(*args,**kwargs)

    def set(self,*args,**kwargs):
        #init poly
        arg_num = list(args)
        arg_den = list(args)
        arg_num.pop(1)
        arg_den.pop(0)

        num_poly = Poly(*arg_num)
        den_poly = Poly(*arg_den)

        
        num = args[0] if isinstance(args[0],str) else "set by List"
        den = args[1] if isinstance(args[1],str) else "set by List"

        #print num_poly.ivar
        #print den_poly.ivar


        self.set_base(num_poly,den_poly,num,den)


    def inp(self,in_):
        cur_index = 0
        self.out = 0.0
        for i in range(self.num_b_coeff):
            if self.b_exp[i]==0:
                self.out += self.b_coeff[i]*in_
            else:
                cur_index = self._x_samples_pointer + self.b_exp[i] - 1
                if (cur_index >= self._num_x_samples):
                    cur_index -= self._num_x_samples
                self.out += self.b_coeff[i]*self._x_samples[cur_index]


        for i in range(self.num_a_coeff): # a0 coeffient already removed
            cur_index = self._y_samples_pointer + self.a_exp[i] - 1
            if (cur_index >= self._num_y_samples):
                cur_index -= self._num_y_samples
            self.out += self.a_coeff[i]*self._y_samples[cur_index]

        #update sample memory
        if self._num_x_samples>0:
            self._x_samples_pointer -=1
            if self._x_samples_pointer < 0:
                self._x_samples_pointer = self._num_x_samples-1
            self._x_samples[self._x_samples_pointer] = in_

        if self._num_y_samples>0:
            self._y_samples_pointer -=1
            if self._y_samples_pointer < 0:
                self._y_samples_pointer = self._num_y_samples-1
            self._y_samples[self._y_samples_pointer] = self.out 

        if self.out > self._max_out:
            self.reset(self._max_out)
        if self.out < self._min_out:
            self.reset(self._min_out)
        
        return self.out


    def reset(self,value):
        self.out = value
        #figure out DC gain
        den = 1.0
        for i in range(self.num_a_coeff):
            den -= self.a_coeff[i]
        num = 0.0
        for i in range(self.num_b_coeff):
            num += self.b_coeff[i]

        #reset state information and output
        if np.abs(num) >1e-24:
            inv_gain = den/num
            self._x_samples[:] = inv_gain*self.out
        else:
            self._x_samples[1:] = self._x_samples[0]


        self._y_samples[:] = self.out



    
    def set_base(self,num_poly,den_poly,num,den):
        self._x_samples_pointer = 0 
        self._y_samples_pointer = 0

        self._max_out = den_poly.max_
        self._min_out = den_poly.min_

        if num_poly.ivar == "!" and den_poly.ivar == "!":
            num_poly.ivar = "z"
            den_poly.ivar = "z"


        if num_poly.ivar != den_poly.ivar:
            if num_poly.ivar != "!" and den_poly.ivar != "!":
                err_msg  = "error in Filter construct:  independent variables for\n"
                err_msg += "numerator and denominator polynomials are different\n"
                err_msg += "   in this case, ivar for num = %c, for den = %c\n" %(num_poly.ivar,den_poly.ivar)
                err_msg += "   for num: %s\n" %num
                err_msg += "       den: %s\n" %den
                raise Exception(err_msg)

        if num_poly.ivar == "z" or den_poly.ivar == "z":
            self.ivar = "z"
            self.set_dt_filt(num_poly,den_poly,num,den)
        elif num_poly.ivar == "s" or den_poly.ivar == "s":
            self.ivar = "s"
            self.set_ct_filt(num_poly,den_poly,num,den)
        else:
            err_msg  = "error:  filter must have 'z' or 's' for ivar\n"
            err_msg += "  in this case, ivar = %s\n" %num_poly.ivar
            err_msg += "   for num: %s\n" %num
            err_msg += "       den: %s\n" %den
            raise Exception(err_msg)

    def set_ct_filt(self,num_poly,den_poly,num,den):
        number_num_coeff = num_poly.num_coeff
        number_den_coeff = den_poly.num_coeff
        #print number_num_coeff,number_den_coeff

        num_coeff = num_poly.coeff
        den_coeff = den_poly.coeff

        if np.min(np.abs(np.modf(num_poly.exp)[0])) > 0.01:
            err_msg  = "error in 'set_ct_filt':  num_poly->exp has noninteger\n"
            err_msg += "values\n"
            err_msg += "in this case, num_poly.exp = %s" %num_poly.exp
            err_msg += "  for num: %s\n" %num
            err_msg += "      den: %s\n" %den
            raise Exception(err_msg)

        num_exp = np.floor(num_poly.exp).astype(int)


        if np.min(np.abs(np.modf(den_poly.exp)[0])) > 0.01:
            err_msg  = "error in 'set_ct_filt':  den_poly->exp has noninteger\n"
            err_msg += "values\n"
            err_msg += "in this case, den_poly.exp = %s" %den_poly.exp
            err_msg += "  for num: %s\n" %num
            err_msg += "      den: %s\n" %den
            raise Exception(err_msg)
        den_exp = np.floor(den_poly.exp).astype(int)



        #print num_coeff,den_coeff,num_exp,den_exp


        _min = np.min([np.min(num_exp),np.min(den_exp)])
        #print _min

        if _min<0:
            num_exp -=_min
            den_exp -=_min

        #print num_exp,den_exp


        _max = np.max([np.max(num_exp),np.max(den_exp)])
        #print _max

        temp_coeff = np.zeros(_max+1) # as start index is 0

        if self.num_b_coeff != _max+1 or self.num_a_coeff != _max:
            self.num_b_coeff = _max+1
            self.num_a_coeff = _max+1

            self._num_y_samples = _max
            self._num_x_samples = _max

            self._y_samples = np.zeros(self._num_y_samples)
            self._x_samples = np.zeros(self._num_x_samples)


        else:
            self.num_a_coeff = _max+1



        self.b_coeff = np.zeros(self.num_b_coeff)
        self.b_exp = np.arange(self.num_b_coeff)
        self.a_coeff = np.zeros(self.num_a_coeff)
        self.a_exp = np.arange(self.num_a_coeff)


        sample_period = num_poly.sample_period


        #print self.b_coeff,self.b_exp,self.a_coeff,self.a_exp,sample_period


        if sample_period == NaN:
            err_msg  = "error in 'set_ct_fil':  sample_period has not been set\n"
            err_msg += "  in variable list, you must specify 'Ts'\n"
            err_msg += "  for num: %s\n" %num
            err_msg += "      den: %s\n" %den
            raise Exception(err_msg)
        elif sample_period < 1e-30:
            err_msg  = "error in 'set_ct_fil':  sample_period can't be < 1e-30\n\n"
            err_msg += "  in this case, sample_period = %5.3e\n" %sample_period
            err_msg += "  for num: %s\n" %num
            err_msg += "      den: %s\n" %den
            raise Exception(err_msg)


        #numerator conversion


        for i in range(number_num_coeff):
            temp_coeff[:]=0.0
            scale = num_coeff[i]
            if num_exp[i] > 0:
                scale *= np.power(2.0/sample_period,num_exp[i])

                temp_coeff[0] = 1.0
                temp_coeff[1] = -1.0
                for j in range(1,num_exp[i]): #perform mult. of (1 - z^-1)
                    for k in range(_max,0,-1):
                        temp_coeff[k] -= temp_coeff[k-1]
            
                if (num_exp[i] < _max): # perform first multiplication of (1 + z^-1)
                    for k in range(_max,0,-1):
                        temp_coeff[k] += temp_coeff[k-1]

            elif num_exp[i]<_max:
                temp_coeff[0] = 1.0
                temp_coeff[1] = 1.0
            for j in range(num_exp[i]+1,_max):# perform mult. of (1 + z^-1)
                for k in range(_max,0,-1):
                    temp_coeff[k] += temp_coeff[k-1]
                
            for j in range(_max+1):
                self.b_coeff[j] += temp_coeff[j]*scale
 
        #denominator conversion
        for i in range(number_den_coeff):
            temp_coeff[:]=0.0
            scale = den_coeff[i]
            if den_exp[i] > 0:
                scale *= np.power(2.0/sample_period,den_exp[i])

                temp_coeff[0] = 1.0
                temp_coeff[1] = -1.0
                for j in range(1,den_exp[i]): #perform mult. of (1 - z^-1)
                    for k in range(_max,0,-1):
                        temp_coeff[k] -= temp_coeff[k-1]
            
                if (den_exp[i] < _max): # perform first multiplication of (1 + z^-1)
                    for k in range(_max,0,-1):
                        temp_coeff[k] += temp_coeff[k-1]

            elif den_exp[i]<_max:
                temp_coeff[0] = 1.0
                temp_coeff[1] = 1.0
            for j in range(den_exp[i]+1,_max):# perform mult. of (1 + z^-1)
                for k in range(_max,0,-1):
                    temp_coeff[k] += temp_coeff[k-1]
                
            for j in range(_max+1):
                self.a_coeff[j] += temp_coeff[j]*scale


        #for i in range(_max+1):
        #    print ("orig num[%d] = %5.9e" %(i,self.b_coeff[i]))


        #for i in range(_max+1):
        #    print ("orig den[%d] = %5.9e" %(i,self.a_coeff[i]))

        #for i in range(self.num_b_coeff-1,-1,-1):
        #    self.b_coeff[i] = self.b_coeff[i]/self.a_coeff[0]
        self.b_coeff /= self.a_coeff[0]


        self.num_a_coeff -= 1
        a0_val = self.a_coeff[0]

        for i in range(self.num_a_coeff):
            self.a_exp[i] = self.a_exp[i+1]
            self.a_coeff[i] = -self.a_coeff[i+1]/a0_val


        #for i in range(self.num_b_coeff):
        #    print("num[%d] = %5.3f" %(self.b_exp[i],self.b_coeff[i])) 
        #for i in range(self.num_a_coeff):
        #    print("den[%d] = %5.3f" %(self.a_exp[i],self.a_coeff[i]))   


    def set_dt_filt(self,num_poly,den_poly,num,den):
        self.num_b_coeff = num_poly.num_coeff
        self.num_a_coeff = den_poly.num_coeff
        
        self.b_coeff = num_poly.coeff
        
        self.a_coeff = den_poly.coeff
        

        
        if np.min(np.abs(np.modf(num_poly.exp)[0])) > 0.01:
            err_msg  = "error in 'set_dt_filt':  num_poly->exp has noninteger\n"
            err_msg += "values\n"
            err_msg += "in this case, num_poly.exp = %s" %num_poly.exp
            err_msg += "  for num: %s\n" %num
            err_msg += "      den: %s\n" %den
            raise Exception(err_msg)

        self.b_exp = (-np.floor(num_poly.exp)).astype(int)


        if np.min(np.abs(np.modf(den_poly.exp)[0])) > 0.01:
            err_msg  = "error in 'set_dt_filt':  den_poly->exp has noninteger\n"
            err_msg += "values\n"
            err_msg += "in this case, den_poly.exp = %s" %den_poly.exp
            err_msg += "  for num: %s\n" %num
            err_msg += "      den: %s\n" %den
            raise Exception(err_msg)
        self.a_exp = (-np.floor(den_poly.exp)).astype(int)


        #print self.b_exp,self.a_exp

        _min = np.min(self.a_exp)

        self.a_exp -= _min
        self.b_exp -= _min

        _min = np.min(self.b_exp)
        self.b_exp -= _min


        #for i in range(self.num_b_coeff):
        #    print("-- b_exp = %d ,b_coeff = %5.3f" %(self.b_exp[i],self.b_coeff[i]))


        #for i in range(self.num_a_coeff):
        #    print("-- a_exp = %d ,a_coeff = %5.3f" %(self.a_exp[i],self.a_coeff[i]))



        exp0_index = np.where(self.a_exp==0)[0][0]
        a0_val = self.a_coeff[exp0_index]

        if np.abs(a0_val) < 1e-30:
            err_msg  = "error in 'set_dt_fil':  a0_val is close to zero\n"
            err_msg  = "  in this case, a0_val = %5.3e\n" %a0_val
            err_msg  = "  for num: %s\n" %num
            err_msg  = "      den: %s\n" %den
            raise Exception(err_msg)
            

        self.num_a_coeff -=1

        if exp0_index < self.num_a_coeff:
            self.a_exp = np.delete(self.a_exp,exp0_index)
            self.a_coeff = np.delete(self.a_coeff,exp0_index)

        self.a_coeff /= -a0_val
        self.b_coeff /= a0_val


        #print self.a_coeff
        #print self.a_exp

        #print self.b_coeff
        #print self.b_exp
        num_y_samples_needed = np.max(self.a_exp)
        #print "num_y_samples_needed =",num_y_samples_needed

        num_x_samples_needed = np.max(self.b_exp)
        #print "num_x_samples_needed =", num_x_samples_needed


        if num_y_samples_needed != self._num_y_samples or \
                num_x_samples_needed != self._num_x_samples or \
                (self._num_x_samples == 0 and self._num_y_samples==0):

            new_filt_flag = 1
        else:
            new_filt_flag = 0


        #print "new_filt_flag = ",new_filt_flag


        if new_filt_flag == 1:
            self._num_y_samples = np.max(self.a_exp)
            self._num_x_samples = np.max(self.b_exp)

            self._y_samples = np.zeros(self._num_y_samples)
            self._x_samples = np.zeros(self._num_x_samples)

        #print "num_a_coeff = %d, num_b_coeff = %d, num_x_samples = %d, num_y_samples = %d" \
        #        %(self.num_a_coeff,self.num_b_coeff,self._num_x_samples,self._num_y_samples)
        #for i in range(self.num_b_coeff):
        #    print("b_exp = %d ,b_coeff = %5.3f" %(self.b_exp[i],self.b_coeff[i]))

        #for i in range(self.num_a_coeff):
        #    print("a_exp = %d ,a_coeff = %5.3f" %(self.a_exp[i],self.a_coeff[i]))
