# main.py -- put your code here!

import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

red = pyb.LED(1)
green = pyb.LED(2)
yellow = pyb.LED(3)
blue = pyb.LED(4)

leds = [red, green, yellow, blue]

for led in leds:
    led.on()
    pyb.delay(250)
    led.off()

A = 0
B = 0

def exti_callback(line):
    global A
    global B
    if line == 9:
        A = A + 1
    if line == 8:
        B = B + 1

extint1 = pyb.ExtInt(pyb.Pin.cpu.B9, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, exti_callback)
extint2 = pyb.ExtInt(pyb.Pin.cpu.B8, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, exti_callback)
#extint3 = pyb.ExtInt(pyb.Pin.cpu.C7, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, exti_callback)
#extint4 = pyb.ExtInt(pyb.Pin.cpu.C6, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, exti_callback)

t2 = pyb.Timer(2, freq=2000)
oc1  = t2.channel(1, pyb.Timer.OC_TOGGLE, pin=pyb.Pin.board.X1)
oc2  = t2.channel(2, pyb.Timer.OC_TOGGLE, pin=pyb.Pin.board.X2)

oc1.compare(0)
oc2.compare(t2.period()//2)

while True:
    pyb.delay(500)
    print('A = ', A, ' B = ', B)

