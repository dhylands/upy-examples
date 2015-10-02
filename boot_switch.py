import pyb

sw = pyb.Switch()
# 1 - Red
# 2 - Green
# 3 - Yellow
# 4 - Blue
pyb.LED(2).off() # Turn Greem LED off since normal boot turns it on
led = pyb.LED(1)
leds = (pyb.LED(4), pyb.LED(3), pyb.LED(2))

try:
    import boot_mode
    persisted_mode = boot_mode.mode
    mode = boot_mode.mode
except:
    persisted_mode = -1
    mode = 0

def mode_led(mode):
    for led in leds:
        led.off()
    if mode >= 0:
        leds[mode].on()

for i in range(10):
    led.on()
    pyb.delay(100)
    led.off()
    pyb.delay(100)
    if sw():
        while True:
            mode_led(mode)
            pyb.delay(500)
            if not sw():
                mode_led(-1)
                break
            mode = (mode + 1) % 3
        break

for i in range(3):
    mode_led(mode)
    pyb.delay(100)
    mode_led(-1)
    pyb.delay(100)

usb_mode = ('CDC+MSC', 'CDC+HID', 'CDC')[mode]
if mode != persisted_mode:
    with open('/flash/boot_mode.py', 'w') as f:
        f.write('mode = %d\n' % mode)
        f.write("usb_mode = '%s'\n" % usb_mode)
    pyb.sync()

pyb.usb_mode(usb_mode)
# Note: prints which occur before the call pyb.usb_mode() will not show on the
#       USB serial port.
print('usb_mode = %s' % usb_mode)

# Cleanup the namespace (since anything from boot.py shows up in the REPL)
del led, leds, mode, usb_mode, persisted_mode, i, sw, mode_led, boot_mode
