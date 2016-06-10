import pyb

import micropython
micropython.alloc_emergency_exception_buf(100)

led1 = pyb.LED(4) # 4 = Blue
led2 = pyb.LED(3) # 3 = Yellow

pin = pyb.Pin('SW', pyb.Pin.IN, pull=pyb.Pin.PULL_UP)

def callback(line):
    led1.toggle()
    if pin.value(): # 1 = not pressed
        led2.off()
    else:
        led2.on()


ext = pyb.ExtInt(pin, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_UP, callback)

