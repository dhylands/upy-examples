#
# Test for Control C
#

import pyb
import sys
import time

def loop(enabled, uart, readchar):
    print('\nStarting loop')
    try:
        for i in range(3000):
            if enabled:
                print('enabled', i, '\r', end='')
            else:
                print('disabled', i, '\r', end='')
            if uart and uart.any():
                if readchar:
                    ch = uart.readchar()
                else:
                    ch = uart.read(1)
                print('\nRead', ch, 'from UART')
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nCaught KeyboardInterrupt Interrupt")
        time.sleep(1)


def loop2(uart, readchar):
    sys.stdin.ioctl(sys.stdin.IOCTL_SET_INTERRUPT_CHAR, -1)
    print('Control-C should be disabled')
    loop(False, uart, readchar)

    sys.stdin.ioctl(sys.stdin.IOCTL_SET_INTERRUPT_CHAR, 3)
    print('Control-C should be enabled')
    loop(True, uart, readchar)

def test():
    uart = pyb.repl_uart()
    if uart is None:
        print('This test needs to run with a repl_uart')
        return

    # With UART using the irq, we shouldn't need to read the uart to detect
    # the Control-C
    uart.init(115200, read_buf_len=64)
    loop2(None, True)   # test readchar
    loop2(None, False)  # test read

    # Without using the IRQ, we need to actually perform a read on the uart
    # in order to trigger the Control-C
    uart.init(115200, read_buf_len=0)
    loop2(uart, True)   # test readchar
    loop2(uart, False)  # test read

test()
