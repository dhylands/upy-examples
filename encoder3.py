import pyb
import stm

# This script sets up a timer to do quadrature decoding
#
# THis script assumes that you have a jumper from X1 to X3 and X2 to X4

out_idx = 0
out_seq = [0, 1, 3, 2]

pin_a2 = pyb.Pin('X3', pyb.Pin.OUT_PP)
pin_b2 = pyb.Pin('X4', pyb.Pin.OUT_PP)

def set_out():
    print("Writing X4 {:d} X3 {:d}".format((out_seq[out_idx] & 0x02) != 0, (out_seq[out_idx] & 0x01) != 0))
    pin_a2.value((out_seq[out_idx] & 0x01) != 0)
    pin_b2.value((out_seq[out_idx] & 0x02) != 0)

def incr():
    global out_idx
    out_idx = (out_idx + 1) % 4
    set_out()

def decr():
    global out_idx
    out_idx = (out_idx - 1) % 4
    set_out()

set_out()

pin_a = pyb.Pin('X1', pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)
pin_b = pyb.Pin('X2', pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)

enc_timer = pyb.Timer(2, prescaler=1, period=100000)
enc_channel = enc_timer.channel(1, pyb.Timer.ENC_AB)

for i in range(12):
    print("Counter =", enc_timer.counter());
    incr()
for i in range(24):
    print("Counter =", enc_timer.counter());
    decr()
for i in range(12):
    print("Counter =", enc_timer.counter());
    incr()
print("Counter =", enc_timer.counter());

