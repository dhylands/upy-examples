import pyb

# FTMx is clocked at F_BUS @ 48 MHz
# With a prescaler of 128, this drops to 375 kHz
# With a period of 37500, this wraps about 10 times/second

t0 = pyb.Timer(0, prescaler=128, period=37500)
ch0 = t0.channel(0, pyb.Timer.OC_TOGGLE, pin=pyb.Pin.board.D22, compare=10000)
fch1 = t0.channel(1, pyb.Timer.OC_TOGGLE, pin=pyb.Pin.board.D23, compare=20000)
