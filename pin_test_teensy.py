import pyb

def test_pin(pin_name):
    pin = pyb.Pin(pin_name, pyb.Pin.OUT_PP)
    pin.high()
    pyb.delay(250)
    pin.low()
    pyb.delay(250)

def MyMapper(pin_name):
   if pin_name == "bar":
       return pyb.Pin.cpu.C5    # LED

def test():
    test_pin('C5')

    MyMapperDict = {'Foo' : pyb.Pin.board.D13 }   # GREEN 
    pyb.Pin.dict(MyMapperDict)

    test_pin('Foo')

    pyb.Pin.mapper(MyMapper)

    test_pin('bar')
    test_pin('D13')

test()
