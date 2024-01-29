import machine
import time

led = machine.Pin(21, machine.Pin.OUT)

LED_ON = 0
LED_OFF = 1

tick = 0
led_value = LED_OFF
led.value(led_value)
while True:
    if tick <= 3:
        led_value = 1 - led_value
        led.value(led_value)
    tick = (tick + 1) % 10
    time.sleep_ms(100)
