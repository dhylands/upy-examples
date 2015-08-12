import pyb

class rotary():
    def __init__(self,Apin='X21',Bpin='X22'):
        self.B = pyb.Pin(Bpin)
        self.A = pyb.Pin(Apin)

        self.prevA = self.A.value()
        self.prevB = self.B.value()

        self.CWcount = 0
        self.CCWcount = 0

        self.position = 0

        self.Bint = pyb.ExtInt(self.B,pyb.ExtInt.IRQ_RISING_FALLING,pyb.Pin.PULL_UP,self.callback)
        self.Aint = pyb.ExtInt(self.A,pyb.ExtInt.IRQ_RISING_FALLING,pyb.Pin.PULL_UP,self.callback)


    def callback(self,line):
        #     self.Bint.disable()
        #     self.Aint.disable()

        A = self.A.value()
        B = self.B.value()

        #previous state 11
        if   self.prevA==1 and self.prevB==1:
            if A==1 and B==0:
                #print( "CCW 11 to 10")
                self.CCWcount += 1
                self.prevA = A
                self.prevB = B

            elif A==0 and B==0:
                #print ("CW 11 to 00")
                self.CWcount += 1
                self.prevA = A
                self.prevB = B

        #previous state 10
        elif self.prevA==1 and self.prevB==0:
            if A==1 and B==1:
                #print ("CW 10 to 11")
                self.CWcount += 1
                self.prevA = A
                self.prevB = B

            elif A==0 and B==0:
                #print ("CCW 10 to 00")
                self.CCWcount += 1
                self.prevA = A
                self.prevB = B

        #previous state 00
        elif self.prevA==0 and self.prevB==0:
            if A==1 and B==1:
                #print ("CCW 00 to 11")
                self.CCWcount += 1
                self.prevA = A
                self.prevB = B

            elif A==1 and B==0:
                #print ("CW 00 to 10")
                self.CWcount+=1
                self.prevA = A
                self.prevB = B

        #     self.Bint.enable()
        #     self.Aint.enable()

        if A==1 and B==1:
            if self.CWcount>=3 and self.CWcount>self.CCWcount:
                self.position+=1
                print (self.position)
            if self.CCWcount>=3 and self.CCWcount>self.CWcount:
                self.position-=1
                print(self.position)
            self.CCWcount = 0
            self.CWcount  = 0


