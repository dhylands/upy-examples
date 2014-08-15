import pyb

def test_pin(pin_name):
    pin = pyb.Pin(pin_name, pyb.Pin.OUT_PP)
    pin.high()
    pyb.delay(250)
    pin.low()
    pyb.delay(250)

def MyMapper(pin_name):
   if pin_name == "bar":
       return pyb.Pin.cpu.A15   # YELLOW

def test():
    test_pin('A13')    # RED

    MyMapperDict = {'Foo' : pyb.Pin.cpu.A14 }   # GREEN 
    pyb.Pin.dict(MyMapperDict)

    test_pin('Foo')

    pyb.Pin.mapper(MyMapper)

    test_pin('bar')
    test_pin('LED_BLUE')

test()
