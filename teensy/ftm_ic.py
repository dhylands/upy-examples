import pyb
import micropython


# D22 - FTM0 Channel 0
# D23 - FTM0 Channel 1
#
# This script assumes that there is a jumper wire connecting D21 and D22

# For this example, we'll setup a timer in PWM mode to generate a servo pulse.
# FTMx is clocked at 48 MHz. With a prescalar of 16, this drops to 3 MHz.
# 20 msec period is 60000 clock ticks. 1000 usec is a count of 3000, and
# 2000 usec s a count of 6000.

servo_pin = pyb.Pin.board.D22
t0 = pyb.Timer(0, prescaler=16, period=59999);
servo = t0.channel(0, pin=servo_pin, mode=pyb.Timer.PWM)
servo.pulse_width(1000 * 3)

debug_pin = pyb.Pin('D21', pyb.Pin.OUT_PP)

ic_pin = pyb.Pin.board.D23
ic = t0.channel(1, pin=ic_pin, mode=pyb.Timer.IC, ic_polarity=pyb.Timer.IC_POLARITY_BOTH)

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
        ic_width = ((ic.compare() - ic_start) & 0x0fffffff) // 3
    debug_pin.value(0)

micropython.alloc_emergency_exception_buf(100)
ic.callback(ic_cb)
pw = 1000
while True:
    servo.pulse_width(pw * 3)
    pyb.delay(200)
    print("pulste_width = %d, ic_width = %d, ic_start = %d" % (pw, ic_width, ic_start))
    pw = ((pw - 900) % 1100) + 1000

