import pyb
import stm

# This script sets up a timer to do quadrature decoding
#
# It was tested using a switch similar to https://www.sparkfun.com/products/9117

pin_a = pyb.Pin('X1', pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)
pin_b = pyb.Pin('X2', pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)

enc_timer = pyb.Timer(2, prescaler=1, period=100000)
enc_channel = enc_timer.channel(1, pyb.Timer.ENC_B)

def dump_regs(timer_base):
    smcr = stm.mem16[timer_base + stm.TIM_SMCR]
    sms = smcr & 0x0007
    ece = (smcr & 0x4000) >> 14
    print('SMS = {:03b} ECE = {:1b}'.format(sms, ece))

dump_regs(stm.TIM2)

out_idx = 0
out_seq = [0, 1, 3, 2]

pin_a2 = pyb.Pin('X3', pyb.Pin.OUT_PP)
pin_b2 = pyb.Pin('X4', pyb.Pin.OUT_PP)

def set_out():
    print("Writing {:d}{:d}".format((out_seq[out_idx] & 0x01) != 0, (out_seq[out_idx] & 0x02) != 0))
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

if False:
    set_out()
    while True:
        for i in range(10):
            print("Counter =", enc_timer.counter(), " channel =", enc_channel.capture());
            incr()
        for i in range(10):
            print("Counter =", enc_timer.counter(), " channel =", enc_channel.capture());
            decr()
        break
else:
    while True:
        print("Counter =", enc_timer.counter());
        pyb.delay(200)

