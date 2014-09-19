import pyb

# TIM2 runs at 84 MHz
# at 20000 Hz, count runs from 0 to 4199
# In center mode, the frequency will be halved, so we'll get a 10 kHz output
t2 = pyb.Timer(2, freq=20000, mode=pyb.Timer.CtENTER)
ch2 = t2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.X2, pulse_width=(t2.period() + 1) // 4)
ch3 = t2.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3, pulse_width=(t2.period() + 1) // 2)

