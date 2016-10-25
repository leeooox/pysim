class And2:
    def __init__(self):
        self.out = -1.0
        self._state = 0

    def inp(self,in0,in1):

        if self.out == -1:
            if in0 != -1.0 and in1 != -1.0:
                self._state = 1
                #in0 < in1,in0 transition occurs later than in1
                self.out = in0 if in0<in1 else in1
        elif self.out == 1.0:
            if in0 !=1.0 or in1 != 1.0:
                self._state = 0
                #-in0<-in1,in0 transition occurs later than in1
                self.out = in1 if (-in0<-in1) else in0
        else:
            if in0 == 1.0 and in1 == 1.0:
                self.out = 1.0
            elif in0 == -1.0 or in1 == -1.0:
                self.out = -1.0
            else:
                if self._state == 0:
                    if in0 != -1.0 and in1 != -1.0:
                        self._state = 1
                        #in0 < in1,in0 transition occurs later than in1
                        self.out = in0 if in0<in1 else in1
                else:
                    if in0 != 1.0 or in1 != 1.0:
                        self._state = 0
                        #-in0<-in1,in0 transition occurs later than in1
                        self.out = in1 if (-in0<-in1) else in0

        return self.out


class And:
    def __init__(self):
        self.out = -1.0
        self.and1 = And2()
        self.and2 = And2()
        self.and3 = And2()
        self.and4 = And2()

    def inp(self,in0,in1,in2=1.0,in3=1.0,in4=1.0):
        self.out = self.and4.inp(self.and3.inp(self.and2.inp(self.and1.inp(in0,in1),in2),in3),in4) 
        return self.out

