from machine import Pin, PWM
from esp32 import PCNT
import time
from lcd import BL, LCD

print('encoder_lcd')
# This script sets up the ESP32 PCNT peripheral to do quadrature decoding
pin_a = Pin(16, Pin.IN, pull=Pin.PULL_UP)
pin_b = Pin(17, Pin.IN, pull=Pin.PULL_UP)
rotary = PCNT(0, min=-32000, max=32000)
rotary.init(channel=0, pin=pin_a, falling=PCNT.INCREMENT, rising=PCNT.DECREMENT, mode_pin=pin_b, mode_low=PCNT.REVERSE)
rotary.init(channel=1, pin=pin_b, falling=PCNT.DECREMENT, rising=PCNT.INCREMENT, mode_pin=pin_a, mode_low=PCNT.REVERSE)
rotary.start()

print('encoder_lcd: PWM')
pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(65535)#max 65535

print('encoder_lcd: LCD')
lcd = LCD()
lcd.fill(0)
lcd.show()

spin_idx = 0
spin_str = '\\|/-'

print('encoder_lcd: loop')
while True:
    lcd.fill(0)
    lcd.text(f'Counter: {rotary.value()} {spin_str[spin_idx]}', 60, 40, 0xF800)
    lcd.show()
    spin_idx = (spin_idx + 1) % 4
