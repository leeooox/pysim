import numpy as np
from Poly import Poly


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

        #init poly
        arg_num = list(args)
        arg_den = list(args)
        arg_num.pop(1)
        arg_den.pop(0)

        num_poly = Poly(*arg_num)
        den_poly = Poly(*arg_den)

        #print num_poly.coeff
        #print num_poly.exp

        #print den_poly.coeff
        #print den_poly.exp
        
        num = args[0] if isinstance(args[0],str) else "set by List"
        den = args[1] if isinstance(args[1],str) else "set by List"


        self.set_base(num_poly,den_poly,num,den)


    
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
        pass


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


        for i in range(self.num_b_coeff):
            print("-- b_exp = %d ,b_coeff = %5.3f" %(self.b_exp[i],self.b_coeff[i]))


        for i in range(self.num_a_coeff):
            print("-- a_exp = %d ,a_coeff = %5.3f" %(self.a_exp[i],self.a_coeff[i]))



        exp0_index = np.where(self.a_exp==0)[0][0]
        a0_val = self.a_coeff[exp0_index]

        if np.abs(a0_val) < 1e-30:
            err_msg  = "error in 'set_dt_fil':  a0_val is close to zero\n"
            err_msg  = "  in this case, a0_val = %5.3e\n" %a0_val
            err_msg  = "  for num: %s\n" %num
            err_msg  = "      den: %s\n" %den
            raise Exception(err_msg)
            

        self.num_a_coeff -=1


        self.a_exp = np.delete(self.a_exp,exp0_index)
        self.a_coeff = np.delete(self.a_coeff,exp0_index)

        self.a_coeff /= -a0_val
        self.b_coeff /= a0_val


        print self.a_coeff
        print self.a_exp

        print self.b_coeff
        print self.b_exp
        num_y_samples_needed = np.max(self.a_exp)
        print "num_y_samples_needed =",num_y_samples_needed

        num_x_samples_needed = np.max(self.b_exp)
        print "num_x_samples_needed =", num_x_samples_needed


        if num_y_samples_needed != self._num_y_samples or \
                num_x_samples_needed != self._num_x_samples or \
                (self._num_x_samples == 0 and self._num_y_samples==0):

            new_filt_flag = 1
        else:
            new_filt_flag = 0


        print "new_filt_flag = ",new_filt_flag


        if new_filt_flag == 1:
            self._num_y_samples = np.max(self.a_exp)
            self._num_x_samples = np.max(self.b_exp)

            self._y_samples = np.zeros(self._num_y_samples)
            self._x_samples = np.zeros(self._num_x_samples)

        print "num_a_coeff = %d, num_b_coeff = %d, num_x_samples = %d, num_y_samples = %d" \
                %(self.num_a_coeff,self.num_b_coeff,self._num_x_samples,self._num_y_samples)
        for i in range(self.num_b_coeff):
            print("b_exp = %d ,b_coeff = %5.3f" %(self.b_exp[i],self.b_coeff[i]))

        for i in range(self.num_a_coeff):
            print("a_exp = %d ,a_coeff = %5.3f" %(self.a_exp[i],self.a_coeff[i]))
