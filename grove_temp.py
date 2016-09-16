# Pyboard code for reading a grove temp sensor connected to X1

import pyb
import math

B = 4275

temp_adc = pyb.ADC('X1')

def read_temp():
    temp_raw = temp_adc.read()
    R = (4095 / temp_raw) - 1.0
    
    temp = 1.0 / (math.log(R) / B + 1/298.15) - 273.15
    return temp

while True:
    t = read_temp()
    print('temp =', t)
    pyb.delay(1000)
