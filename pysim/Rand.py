import numpy.random as rd

class Rand:
    def __init__(self,type_,p=0.5):
        self.out = 0.0
        self.set(type_,p)
        rd.seed(0)

    def set(self,type_,p):
        if type_ == "gauss":
            self._type_flag = 0
        elif type_ == "uniform":
            self._type_flag = 1
        elif type_ == "bernoulli":
            self._type_flag = 2
        else:
            err_msg  = "error in Rand constructor:  type must be 'gauss',\n"
            err_msg += "               'uniform', or 'bernoulli'\n"
            err_msg += "  in this case, type = '%s'\n" %type_
            raise Exception(err_msg) 

        self._p_bern = p

          

    def inp(self):
        if self._type_flag == 0:
            self.out = rd.randn() 
        elif self._type_flag == 1:
            self.out = rd.rand()
        elif self._type_flag == 2:
            self.out = rd.binomial(1,self._p_bern)*2-1
        else:
            err_msg  = "error in Rand out function:  must have 0 <= type_flag <= 2"
            err_msg += "   in this case, type_flag = %d"
            raise Exception(err_msg)

            
        return self.out

    def set_seed(self,in_):
        rd.seed(in_)

    def reset(self):
        rd.seed(0)


if __name__ == "__main__":
    rand1  = Rand(2)

    for i in range(20):
        print rand1.inp()

