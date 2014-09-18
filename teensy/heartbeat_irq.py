import pyb
import micropython

class Heartbeat(object):

    def __init__(self):
        self.tick = 0
        self.led = pyb.LED(1)
        tim = pyb.Timer(0)
        tim.init(prescaler=128, period=37500) # 10 Hz
        tim.callback(self.heartbeat_cb)

    def heartbeat_cb(self, tim):
        if self.tick <= 3:
            self.led.toggle()
        self.tick = (self.tick + 1) % 10

micropython.alloc_emergency_exception_buf(100)
Heartbeat()
