#
#   Open Loop Brushless Motor Test
#
#   Seeed Xiao RP2040
#
#   Based off the Arduino code from this video:
#   https://www.youtube.com/watch?v=zSdetJsSeNw
#


import machine
from machine import Pin, ADC, PWM
import time
import math


pot = ADC(Pin(26))  # A0

enable_pin = Pin(1, Pin.OUT)  # D7
phase_a_pin = Pin(2, Pin.OUT)  # D8
phase_b_pin = Pin(3, Pin.OUT)  # D9
phase_c_pin = Pin(4, Pin.OUT)  # D10

phase_a_pwm = PWM(phase_a_pin, freq=31250, duty_u16=32768)
phase_b_pwm = PWM(phase_b_pin, freq=31250, duty_u16=32768)
phase_c_pwm = PWM(phase_c_pin, freq=31250, duty_u16=32768)

pot_angle = 0

enable_pin.value(1)

sin_a = 0
sin_b = 120
sin_c = 240

poles = 16

pi = math.pi


def moving():
    global sin_a, sin_b, sin_c
    global sin_a_pwm, sin_b_pwm, sin_c_pwm
    global phase_a_pwm, phase_b_pwm, phase_c_pwm

    sin_b = sin_a + 120
    sin_c = sin_b + 120

    sin_a = sin_a % 360
    sin_b = sin_b % 360
    sin_c = sin_c % 360

    sin_a_pwm = int(math.sin(sin_a * pi / 180.0) * 32767.5 + 32767.5)
    sin_b_pwm = int(math.sin(sin_b * pi / 180.0) * 32767.5 + 32767.5)
    sin_c_pwm = int(math.sin(sin_c * pi / 180.0) * 32767.5 + 32767.5)

    torque_constant = 0.7

    phase_a_pwm.duty_u16(int(sin_a_pwm * torque_constant))
    phase_b_pwm.duty_u16(int(sin_b_pwm * torque_constant))
    phase_c_pwm.duty_u16(int(sin_c_pwm * torque_constant))


while True:
    moving()
    adc = 0
    for i in range(10):
        adc += pot.read_u16()
        time.sleep_us(100)
    adc = adc / 10

    pot_angle = int(adc * (360 * poles) / 65536)
    sin_a = pot_angle


