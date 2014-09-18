import pyb

# FTMx is clocked at F_BUS @ 48 MHz
# With a prescaler of 128, this drops to 375 kHz
# With a period of 37500, this wraps about 10 times/second

t0 = pyb.Timer(0, prescaler=128, period=37500)
ch0 = t0.channel(0, pin=pyb.Pin.board.D22, mode=pyb.Timer.OC, compare=10000, oc_mode=pyb.Timer.OC_MODE_TOGGLE)
ch1 = t0.channel(1, pin=pyb.Pin.board.D23, mode=pyb.Timer.OC, compare=20000, oc_mode=pyb.Timer.OC_MODE_TOGGLE)
