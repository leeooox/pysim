from __future__ import division
import sympy as sym
import numpy as np
from Const import NaN


class Poly:
    def __init__(self,*args,**kwargs):
        self.num_coeff = 0
        self.coeff = None #list of double
        self.exp = None #list of int

        self.max_ = NaN
        self.min_  = -NaN
        self.sample_period = NaN

        self.ivar = "!"

        self.set(*args,**kwargs)


    def set(self,*args,**kwargs):
        
        if len(args) > 1:
            expr = args[0]
            para_list = filter(lambda x:x,args[1].replace(" ","").strip().split(","))

            para_dict= {}
            i=2
            for para in para_list:
                para_dict[para] = args[i]
                if para == "Max":
                    self.max_ = args[i]
                elif para == "Min":
                    self.min_ = args[i]
                elif para == "Ts":
                    self.sample_period = args[i]

                i+=1

            self.ivar = self._get_ivar(expr,args[1])

            find_para_in_expr_flag = False
            for para in para_list:
                if expr.find(para) != -1:
                    find_para_in_expr_flag = True

            
            if self.ivar != "!":
                self.set_expr(expr,para_dict)
            elif not para_list:
                self.set_expr_no_vars(expr)
            elif not find_para_in_expr_flag:
                self.set_expr_no_vars(expr)
            else:
                self.set_expr(expr,para_dict)

        elif (len(args)==1 and isinstance(args[0],str)):
            expr = args[0]
            para_dict = {}
            self.ivar = self._get_ivar(expr)

            if self.ivar != "!":
                self.set_expr(expr,para_dict)
            else:
                self.set_expr_no_vars(expr)

        else:
            self.set_list(np.array(args[0]))



    def set_list(self,list_):
        self.ivar = "z"
        
        my_max = np.abs(np.max(list_))

        if my_max < 1e-20:
            err_msg = "Error in Poly.set (using List):  all elements within\n"
            err_msg += "  the input list appear to be zero!\n"
            raise Exception(err_msg)

        #remove the coeffecient which is 10E12 times smaller than max coeffecient
        my_max *= 1.0e-12

        coeff_in = np.array(list_,dtype=np.float)
        self.coeff = coeff_in[[np.abs(coeff_in)>my_max]]
        self.exp = -np.where(np.abs(coeff_in)>my_max)[0]
        self.num_coeff = len(self.coeff)

    def set_expr_no_vars(self,expr):
        pi = np.pi
        self.coeff = np.array([eval(expr)],dtype=np.float)
        self.exp = np.zeros(1)
        self.num_coeff = 1  

    def set_expr(self,expr,para_dict):
        #print "set by expr"

        expr_raw = expr.replace("^","**")

        s = sym.symbols(self.ivar)

        expr = sym.Poly(expr_raw)
        #print "para_dict",para_dict

        coeff_list = []
        exp_list = []
        for term in expr.as_expr().as_ordered_terms(order="rev-lex"):
            coeff,exp =  term.as_coeff_exponent(s)
            #print term,coeff,coeff.evalf(subs=para_dict),exp
            if exp in exp_list: # if the exp already existing
                idx = exp_list.index(exp)
                coeff_list[idx] += coeff.evalf(subs=para_dict)
            else:
                coeff_list.append(coeff.evalf(subs=para_dict))
                exp_list.append(exp)


        self.coeff = np.array(coeff_list,dtype=np.float)
        self.exp = np.array(exp_list,dtype=np.float) 
        self.num_coeff = len(self.coeff)

        #print self.coeff
        #print self.exp



    def _get_ivar(self,expr,para=""):
        para_list = filter(lambda x:x,para.replace(" ","").strip().split(","))
        para_single_letter = filter(lambda x:len(x)==1,para_list)

        expr = expr.replace(" ","").strip()

        ivar_can_list = []

        if expr.find("^") == -1:
            if len(para_single_letter)>0:
                # exp in [0,1]
                expr_temp = expr.replace("-","+").split("+")
                for expr_slice in expr_temp:
                    if expr_slice[-1].isalpha() and \
                            (expr_slice[-1] not in para_single_letter) and \
                            (expr_slice not in para_list):
                        ivar_can_list.append(expr_slice[-1])
            elif expr[-1].isalpha():
                ivar_can_list.append(expr[-1])


        else:
            for i in range(len(expr)):
                if expr[i] == "^" and expr[i-1].isalpha() and (expr[i-1] not in para_single_letter):
                       ivar_can_list.append(expr[i-1]) 



        if len(ivar_can_list) == 0:
            return "!"
        else:
            last_ivar = ivar_can_list[0]
            for ivar in ivar_can_list:
                if last_ivar!=ivar:
                    raise Exception("Wrong Poly expression")
                last_ivar = ivar
            return last_ivar



 
if __name__ == "__main__":
    Ts = 1e-9
    poly1 = Poly("fc + Kv*s","fc,Kv,Ts",10,2,Ts)

    print NaN

