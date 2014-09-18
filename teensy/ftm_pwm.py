import pyb

# FTMx is clocked at F_BUS @ 48 MHz
# With a prescaler of 128, this drops to 375 kHz
# With a period of 37500, this wraps about 10 times/second
# With center mode PWM, this corresponds to 5 Hz

t0 = pyb.Timer(0, prescaler=128, period=37500, counter_mode=pyb.Timer.COUNTER_MODE_CENTER)
ch0 = t0.channel(0, pin=pyb.Pin.board.D22, mode=pyb.Timer.PWM, pulse_width=((t0.period() + 1) // 4) - 1)
fch1 = t0.channel(1, pin=pyb.Pin.board.D23, mode=pyb.Timer.PWM, pulse_width=((t0.period() + 1) // 2) - 1)

