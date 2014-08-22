import pyb

# TIM2 runs at 84 MHz
# at 100 Hz, count runs from 0 to 840,000
# In center aligned mode, you get 50Hz output.
t2 = pyb.Timer(2, pin=pyb.Pin.board.X2, mode=pyb.Timer.PWM, channel=2, freq=100, pulse=210000, counter_mode=pyb.Timer.COUNTER_MODE_CENTER_1)
t3 = pyb.Timer(2, pin=pyb.Pin.board.X3, mode=pyb.Timer.PWM, channel=3, freq=100, pulse=420000, counter_mode=pyb.Timer.COUNTER_MODE_CENTER_1)

