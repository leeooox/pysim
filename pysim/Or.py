from And import And2


class Or:
    def __init__(self):
        self.out = -1.0
        self.and1 = And2()
        self.and2 = And2()
        self.and3 = And2()
        self.and4 = And2()

    def inp(self,in0,in1,in2=-1.0,in3=-1.0,in4=-1.0):
        self.out = -self.and4.inp(self.and3.inp(self.and2.inp(self.and1.inp(-in0,-in1),-in2),-in3),-in4) 
        return self.out

