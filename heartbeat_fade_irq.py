import pyb

# LEDs 1 = Red
#      2 = Green
#      3 = Orange
#      4 = Blue     (can be faded)

class Heartbeat(object):

    def __init__(self):
        self.tick = 0
        self.led = pyb.LED(4)
        tim = pyb.Timer(4)
        tim.init(freq=100)
        tim.callback(self.heartbeat_cb)

    def heartbeat_cb(self, tim):
        if self.tick < 40:
            # self.tick % 20 gives a number 0 to 19
            # subtracting 9 makes it -9 to 10
            # abs maps it 9 to 0 to 10
            # subtracting from 10 maps it 1 to 10 to 0
            # multiplying by 25 scales it 25 to 250 to 0
            self.led.intensity((10 - (abs((self.tick % 20) - 9))) * 25)
        self.tick = (self.tick + 1) % 100

Heartbeat()
