import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

def heartbeat_cb(tim):
    global tick
    if tick <= 3:
        led.toggle()
    tick = (tick + 1) % 10

tick = 0
led = pyb.LED(4) # 4 = Blue
tim = pyb.Timer(4)
tim.init(freq=10)
tim.callback(heartbeat_cb)
