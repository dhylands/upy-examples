import pyb

# At 20 kHz, the duty cycle should 50 usec
t2 = pyb.Timer(2, freq=20000, mode=pyb.Timer.PWM)
ch1 = t2.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.X1, pulse_width_percent=5)
ch2 = t2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.X2, pulse_width_percent=35)
ch3 = t2.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3, pulse_width_percent=50)
ch4 = t2.channel(4, pyb.Timer.PWM, pin=pyb.Pin.board.X4, pulse_width_percent=95)

