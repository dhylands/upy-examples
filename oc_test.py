import pyb
import micropython

debug_pin = pyb.Pin('X1', pyb.Pin.OUT_PP)

# setup oc_clock to be a 1 kHz clock
oc  = pyb.Timer(2, pin=pyb.Pin.board.X2, mode=pyb.Timer.OC,  channel=2, oc_mode=pyb.Timer.OC_MODE_TOGGLE, freq=2000)
pwm = pyb.Timer(5, pin=pyb.Pin.board.X3, mode=pyb.Timer.PWM, channel=3, prescaler=41999, period=9, pulse=1)

