import pyb
import micropython

# This script assumes that there is a jumper wire connecting X1 and X4

# For this example, we'll setup a timer in PWM mode to generate a servo pulse.
# Using a prescalar of 83 gives a timer-tick frequency of 1 MHz (84 MHz / 84).
# The period of 19999 gives a 20,000 usec or 20 msec period. The pulse width
# is then in microseconds.
servo_pin = pyb.Pin.board.X1
t5 = pyb.Timer(5, prescaler=83, period=19999);
servo = t5.channel(1, pyb.Timer.PWM, pin=servo_pin)
servo.pulse_width(1000)

debug_pin = pyb.Pin('X2', pyb.Pin.OUT_PP)

t2 = pyb.Timer(2, prescaler=83, period=0x0fffffff)
ic_pin = pyb.Pin.board.X4
ic = t2.channel(4, pyb.Timer.IC, pin=ic_pin, polarity=pyb.Timer.BOTH)

ic_start = 0
ic_width = 0

def ic_cb(tim):
    global ic_start
    global ic_width
    debug_pin.value(1)
    # Read the GPIO pin to figure out if this was a rising or falling edge
    if ic_pin.value():
        # Rising edge - start of the pulse
        ic_start = ic.capture()
    else:
        # Falling edge - end of the pulse
        ic_width = ic.capture() - ic_start & 0x0fffffff
    debug_pin.value(0)

micropython.alloc_emergency_exception_buf(100)
ic.callback(ic_cb)
pw = 1000
while True:
    servo.pulse_width(pw)
    pyb.delay(200)
    print("pulse_width = %d, ic_width = %d, ic_start = %d" % (pw, ic_width, ic_start))
    pw = ((pw - 900) % 1100) + 1000

