import pyb
import micropython

tick = 0

def light(led):
    def light_callback(tim):
        global tick
	if tick <= 3:
	    led.toggle()
	tick = (tick + 1) % 10
    return light_callback

micropython.alloc_emergency_exception_buf(100)

led = pyb.LED(4)
tim = pyb.Timer(1, freq=10)
tim.callback(light(led))

