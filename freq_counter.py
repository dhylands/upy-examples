# Example which demonstrates using a timer to count external events.
#
# If the external events (i.e. edges) occur at a regular intervals then you
# can use this as a frequency counter.
#
# This example uses the TIM2_CH1_ETR signal as the clock source for timer 2.
# The ETR pin shares with channel 1, which is CPU pin A0 or board pin X1.
#
# This code also sets up channel 4 on Timer 5 (pin X4) as a signal source
# and expects a jumper wire from pin X4 to X1.

# Note that timers 2 & 5 are 32-bit timers. All of the other timers
# are only 16-bit.

import pyb
import stm

# Since we're toggling, the real freq will be half of the freq parameter.
T5 = pyb.Timer(5, freq=20000)
T5_CH4 = T5.channel(4, pyb.Timer.OC_TOGGLE, pin=pyb.Pin.board.X4)

# MicroPython doesn't directly support this particular timer mode, so we
# set the timer up as a regular timer and then adjust the clock source
# for the timer. The clock source is configured using the SMCR register.
pyb.Pin('X1', pyb.Pin.AF_PP, af=pyb.Pin.AF1_TIM2)
T2 = pyb.Timer(2, prescaler=0, period=0x3fffffff)

# SMCR
#   - ETP (bit 15) = 0 - selects rising edge on ETR input
#   - ECE (bit 14) = 1 - sets external clock mode 2
smcr = stm.mem32[stm.TIM2 + stm.TIM_SMCR]
smcr &= ~(1 << 15)  # clear ETP bit
smcr |= (1 << 14)  # set ECE bit
stm.mem32[stm.TIM2 + stm.TIM_SMCR] = smcr

while True:
  start_count = T2.counter()
  start_micros = pyb.micros()
  pyb.delay(100)
  end_count = T2.counter()
  delta_micros = pyb.elapsed_micros(start_micros)
  if end_count < start_count:
    end_count += 0x40000000
  delta_count = end_count - start_count
  print('Freq = {}'.format(int(delta_count / delta_micros * 1e6 + 0.5)))
  pyb.delay(900)