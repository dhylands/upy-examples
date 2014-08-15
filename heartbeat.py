import pyb

tick = 0
led = pyb.LED(4)    # 4 = Blue
while True:
    if tick <= 3:
        led.toggle()
    tick = (tick + 1) % 10
    pyb.delay(100)
