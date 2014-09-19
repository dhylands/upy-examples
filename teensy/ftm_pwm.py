import pyb

# FTMx is clocked at F_BUS @ 48 MHz
# With a prescaler of 128, this drops to 375 kHz
# With a period of 37500, this wraps about 10 times/second
# With center mode PWM, this corresponds to 5 Hz

t0 = pyb.Timer(0, prescaler=128, period=37500, mode=pyb.Timer.CENTER)
ch0 = t0.channel(0, pyb.Timer.PWM, pin=pyb.Pin.board.D22, pulse_width=(t0.period() + 1) // 4)
ch1 = t0.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.D23, pulse_width=(t0.period() + 1) // 2)

