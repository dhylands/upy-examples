#!/usr/bin/python -u

"""Program for testing rfcomm on the host."""

from __future__ import print_function

import select
import serial
import sys
import tty
import termios
import traceback
import argparse
import time

def serial_mon(port, baud):
    """Reads and write to a serial port."""
    try:
        serial_port = serial.Serial(port=port,
                                    baudrate=baud,
                                    timeout=0.001,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    xonxoff=False,
                                    rtscts=False,
                                    dsrdtr=False)
    except serial.serialutil.SerialException:
        print("Unable to open port '%s'\r" % port)
        return

    serial_fd = serial_port.fileno()
    tty.setraw(serial_fd)
    new_settings = termios.tcgetattr(serial_fd)
    new_settings[6][termios.VTIME] = 0
    new_settings[6][termios.VMIN] = 1
    termios.tcsetattr(serial_fd, termios.TCSANOW, new_settings)

    epoll = select.epoll()
    epoll.register(serial_port.fileno(), select.POLLIN)
    epoll.register(sys.stdin.fileno(), select.POLLIN)

    while True:
        events = epoll.poll()
        for fileno, _ in events:
            if fileno == serial_port.fileno():
                try:
                    data = serial_port.read(256)
                except serial.serialutil.SerialException:
                    print('Serial device @%s disconnected.\r' % port)
                    print('\r')
                    serial_port.close()
                    return
                #for x in data:
                #    print("Serial.Read '%c' 0x%02x\r" % (x, ord(x)))
                sys.stdout.write(data)
                sys.stdout.flush()
            if fileno == sys.stdin.fileno():
                data = sys.stdin.read(1)
                #for x in data:
                #    print("stdin.Read '%c' 0x%02x\r" % (x, ord(x)))
                if data[0] == chr(3):
                    raise KeyboardInterrupt
                if data[0] == '\n':
                    serial_port.write('\r')
                else:
                    serial_port.write(data)
                time.sleep(0.002)


def main():
    """The main program."""
    global LOG_FILE

    default_baud = 9600
    parser = argparse.ArgumentParser(
        prog="bluetooth-host.py",
        usage="%(prog)s [options] [command]",
        description="Reads and writes to HC05",
        epilog="Press Control-C to quit"
    )
    parser.add_argument(
        "-b", "--baud",
        dest="baud",
        action="store",
        type=int,
        help="Set the baudrate used (default = %d)" % default_baud,
        default=default_baud
    )
    parser.add_argument(
        "-p", "--port",
        dest="port",
        help="Set the serial port to use (default /dev/rfcomm0",
        default="/dev/rfcomm0"
    )
    args = parser.parse_args(sys.argv[1:])

    stdin_fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(stdin_fd)
    try:
        # Make some changes to stdin. We want to turn off canonical
        # processing  (so that ^H gets sent to the device), turn off echo,
        # and make it unbuffered.
        tty.setraw(stdin_fd)
        new_settings = termios.tcgetattr(stdin_fd)
        new_settings[3] &= ~(termios.ICANON | termios.ECHO)
        new_settings[6][termios.VTIME] = 0
        new_settings[6][termios.VMIN] = 1
        termios.tcsetattr(stdin_fd, termios.TCSANOW, new_settings)

        serial_mon(port=args.port, baud=args.baud)
    except KeyboardInterrupt:
        print('\r')
        # Restore stdin back to its old settings
        termios.tcsetattr(stdin_fd, termios.TCSANOW, old_settings)
    except Exception:
        # Restore stdin back to its old settings
        termios.tcsetattr(stdin_fd, termios.TCSANOW, old_settings)
        traceback.print_exc()
    else:
        # Restore stdin back to its old settings
        termios.tcsetattr(stdin_fd, termios.TCSANOW, old_settings)

main()


