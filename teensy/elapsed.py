import pyb
led = pyb.LED(1)

def blink_millis():
    start = pyb.millis()
    led.on()
    while pyb.elapsed_millis(start) < 100:
        pass
    led.off()
    while pyb.elapsed_millis(start) < 200:
        pass
    led.on()
    while pyb.elapsed_millis(start) < 300:
        pass
    led.off()
    while pyb.elapsed_millis(start) < 1000:
        pass

def blink_micros():
    start = pyb.micros()
    led.on()
    while pyb.elapsed_micros(start) < 100000:
        pass
    led.off()
    while pyb.elapsed_micros(start) < 200000:
        pass
    led.on()
    while pyb.elapsed_micros(start) < 300000:
        pass
    led.off()
    while pyb.elapsed_micros(start) < 1000000:
        pass

for i in range(5):
    blink_millis()
    blink_micros()

