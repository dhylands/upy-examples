# A script from Peter Hinch.
# https://forum.micropython.org/viewtopic.php?p=62674#p62683
#
# This script returns the period between pulses and also the pulse duration (mark) and duty ratio (mark/period)

from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio
import time

@rp2.asm_pio(set_init=rp2.PIO.IN_LOW, autopush=True, push_thresh=32)
def period():
    wrap_target()
    set(x, 0)
    wait(0, pin, 0)  # Wait for pin to go low
    wait(1, pin, 0)  # Low to high transition
    label('low_high')
    jmp(x_dec, 'next') [1]  # unconditional
    label('next')
    jmp(pin, 'low_high')  # while pin is high
    label('low')  # pin is low
    jmp(x_dec, 'nxt')
    label('nxt')
    jmp(pin, 'done')  # pin has gone high: all done
    jmp('low')
    label('done')
    in_(x, 32)  # Auto push: SM stalls if FIFO full
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.IN_LOW, autopush=True, push_thresh=32)
def mark():
    wrap_target()
    set(x, 0)
    wait(0, pin, 0)  # Wait for pin to go low
    wait(1, pin, 0)  # Low to high transition
    label('low_high')
    jmp(x_dec, 'next') [1]  # unconditional
    label('next')
    jmp(pin, 'low_high')  # while pin is high
    in_(x, 32)  # Auto push: SM stalls if FIFO full
    wrap()

pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
sm0 = rp2.StateMachine(0, period, in_base=pin16, jmp_pin=pin16)
sm0.active(1)
sm1 = rp2.StateMachine(1, mark, in_base=pin16, jmp_pin=pin16)
sm1.active(1)

pwm = PWM(Pin(17))
pwm.freq(1000)
pwm.duty_u16(0xffff // 3)

# Clock is 125MHz. 3 cycles per iteration, so unit is 24.0ns
def scale(v):
    return (1 + (v ^ 0xffffffff)) * 24e-6  # Scale to ms

while True:
    period = scale(sm0.get())
    mark = scale(sm1.get())
    print(period, mark, mark/period)
    time.sleep(0.2)
