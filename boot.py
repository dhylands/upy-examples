# boot.py -- run on boot-up
#
# This is some common initialization that I like to keep around.

import pyb
import micropython
import sys
#pyb.main('main.py') # main script to run after this one
pyb.usb_mode('CDC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse

def bl():
    pyb.bootloader()

def pins():
    for pin_name in dir(pyb.Pin.board):
        pin = pyb.Pin(pin_name)
        print('{:10s} {:s}'.format(pin_name, str(pin)))

def af():
    for pin_name in dir(pyb.Pin.board):
        pin = pyb.Pin(pin_name)
        print('{:10s} {:s}'.format(pin_name, str(pin.af_list())))

def init():
    if True:
        uart = pyb.UART(6,115200)
        pyb.repl_uart(uart)
        print("REPL is also on UART 6 (Y1=Tx Y2=Rx)")
    if True:
        bufsize = 100
        print("Setting alloc_emergency_exception_buf to",  bufsize)
        micropython.alloc_emergency_exception_buf(bufsize)

init()
