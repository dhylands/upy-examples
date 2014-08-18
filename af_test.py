from pyb import Pin, I2C, SPI, UART, ADC, Servo, DAC
import pins

def pins_test():
    i2c = I2C(1, I2C.MASTER)
    spi = SPI(2, SPI.MASTER)
    uart = UART(3, 9600)
    servo = Servo(1)
    adc = ADC(Pin.board.X3)
    dac = DAC(1)
    pin = Pin('X4', mode=Pin.AF_PP, af=Pin.AF3_TIM9)
    pin = Pin('Y1', mode=Pin.AF_OD, af=3)
    pin = Pin('Y2', mode=Pin.OUT_PP)
    pin = Pin('Y3', mode=Pin.OUT_OD, pull=Pin.PULL_UP)
    pin.high()
    pin = Pin('Y4', mode=Pin.OUT_OD, pull=Pin.PULL_DOWN)
    pin.high()
    pin = Pin('X18', mode=Pin.IN, pull=Pin.PULL_NONE)
    pin = Pin('X19', mode=Pin.IN, pull=Pin.PULL_UP)
    pin = Pin('X20', mode=Pin.IN, pull=Pin.PULL_DOWN)
    print('===== output of pins() =====')
    pins.pins()
    print('===== output of af() =====')
    pins.af()

pins_test()

