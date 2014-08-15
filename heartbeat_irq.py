import pyb
import micropython

class Heartbeat(object):

    def __init__(self):
        self.tick = 0
        self.led = pyb.LED(4) # 4 = Blue
        tim = pyb.Timer(4)
        tim.init(freq=10)
        tim.callback(self.heartbeat_cb)

    def heartbeat_cb(self, tim):
        if self.tick <= 3:
            self.led.toggle()
        self.tick = (self.tick + 1) % 10

micropython.alloc_emergency_exception_buf(100)
Heartbeat()
