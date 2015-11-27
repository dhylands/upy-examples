import pyb

class AtomicTest:

    def start(self):
        self.counter = 0
        self.irq_count = 0
        self.main_count = 0
        self.done = False
        tim = pyb.Timer(4)
        tim.init(freq=1000)
        tim.callback(self.callback)

    def report(self):
        print("main_count = %d irq_count = %d counter = %d sum = %d" % (self.main_count, self.irq_count, self.counter, self.main_count + self.irq_count))

    def callback(self, tim):
        self.counter += 1
        self.irq_count += 1
        if self.irq_count >= 10000:
            tim.callback(None)
            self.done = True

t = AtomicTest()

t.start()
while not t.done:
    t.main_count += 1
    t.counter += 1
t.report()

t.start()
while not t.done:
    t.main_count += 1
    irq_state = pyb.disable_irq()
    t.counter += 1
    pyb.enable_irq(irq_state)
t.report()
