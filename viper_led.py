import pyb
import stm

# The BLUE Led on the pyboard is on pin B4

LED_MASK = const(1 << 4)

# The BLUE Led on the pyboard is active high

@micropython.viper
def v_led_pulse():
  LED_BSRR = ptr16(stm.GPIOB + stm.GPIO_BSRR)
  LED_BSRR[0] = LED_MASK # high = on
  pyb.delay(100)
  LED_BSRR[1] = LED_MASK # low = off
  pyb.delay(100)

@micropython.viper
def v_blink():
  for i in range(10):
    v_led_pulse()
    v_led_pulse()
    pyb.delay(600)

v_blink()
