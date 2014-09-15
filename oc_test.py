import pyb

# setup oc_clock to be a 1 kHz clock. Since it toggles we want it to toggle
# 2000 times per second to get a 1000 Hz clock.
t2 = pyb.Timer(2, freq=2000)
oc  = t2.channel(2, mode=pyb.Timer.OC, pin=pyb.Pin.board.X2, oc_mode=pyb.Timer.OC_MODE_TOGGLE)

# stup PWM to be 200 Hz with a 1 clock pulse_width
t5 = pyb.Timer(5, prescaler=41999, period=9)
pwm = t5.channel(3, mode=pyb.Timer.PWM, pin=pyb.Pin.board.X3, pulse_width=1)

