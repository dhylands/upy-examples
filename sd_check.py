import pyb
import os
import sys

print("sys.path =", sys.path)
if os.getcwd() == '/sd':
    print("### SDCard detected ###")
    vars = ['0', '0']
    try:
        with open("/sd/sd_check.vars",  "r") as vars_file:
            vars = vars_file.read().split()
    except:
        pass
    hard_reset_count = int(vars[0])
    soft_reset_count = int(vars[1])
    print("### hard_reset_count = %d, soft_reset_count = %d ###" % (hard_reset_count, soft_reset_count))
    hard_reset = 0
    if soft_reset_count % 40 == 0:
        hard_reset = 1
    soft_reset_count += 1
    hard_reset_count += hard_reset
    with open("/sd/sd_check.vars",  "w") as vars_file:
        vars_file.write('%d %d ' % (hard_reset_count, soft_reset_count))
    pyb.sync()
    vcp = pyb.USB_VCP()
    if vcp.any():
        print("Key press detected on USB - stopping")
    else:
        uart = pyb.UART(6, 115200)
        if uart.any():
            print("Key press detected on USB - stopping")
        else:
            pyb.delay(100)
            if hard_reset:
                pyb.hard_reset()
            pyb.soft_reset()
else:
    print('##############################################################')
    print('##############################################################')
    print("###");
    print("### SD card NOT present");
    print("###");
    print('##############################################################')
    print('##############################################################')
    pyb.delay(3000)

