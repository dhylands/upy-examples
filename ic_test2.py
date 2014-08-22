import pyb
import micropython

# This script assumes that there is a jumper wire connecting X1 and X4

# For this example, we'll use the pyb.Servo class to generate pulses.
servo = pyb.Servo(1)

debug_pin = pyb.Pin('X2', pyb.Pin.OUT_PP)

# We want the counter to increase once per microsecond. We set the prescalar
# up to divide by 84, which gives us a 1 MHz timer counter. This is a 32-bit
# timer, so we can set the period to be a large power of 2 (makes doing the
# pulse width calculation
# simpler)

ic_pin = pyb.Pin.board.X4
ic = pyb.Timer(2, pin=ic_pin, mode=pyb.Timer.IC, channel=4,
               prescaler=83, period=0x0fffffff,
               ic_polarity=pyb.Timer.IC_POLARITY_BOTH)

ic_start = 0
ic_width = 0

def ic_cb(tim):
    global ic_start
    global ic_width
    debug_pin.value(1)
    # Read the GPIO pin to figure out if this was a rising or falling edge
    if ic_pin.value():
        # Rising edge - start of the pulse
        ic_start = ic.pulse()
    else:
        # Falling edge - end of the pulse
        ic_width = ic.pulse() - ic_start & 0x0fffffff
    debug_pin.value(0)

micropython.alloc_emergency_exception_buf(100)
ic.callback(ic_cb)
pw = 1000
while True:
    servo.pulse_width(pw)
    pyb.delay(200)
    print("pulse_width = %d, ic_width = %d, %d" % (pw, ic_width, ic_start))
    pw = ((pw - 900) % 1100) + 1000

