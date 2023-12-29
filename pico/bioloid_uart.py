from machine import UART, Pin, mem32
import time

from micropython import const

UART = (UART(0, baudrate=1000000, tx=Pin(12), rx=Pin(13)), UART(1, baudrate=1000000, tx=Pin(8), rx=Pin(9)))

UART0_BASE = const(0x40034000)
UART1_BASE = const(0x40038000)

UART_BASE = (UART0_BASE, UART1_BASE)

UARTCR = const(0x30)
UARTCR_RXE = const(1 << 9)
UARTCR_TXE = const(1 << 8)

print(f'UARTCR_RXE = 0x{UARTCR_RXE:08x} UARTCD_TXE = 0x{UARTCR_TXE:08x}')

UARTFR = const(0x18)
UARTFR_TXFE = const(1 << 7)
UARTFR_BUSY = const(1 << 3)

UARTFR_DONE_MASK = const(UARTFR_TXFE | UARTFR_BUSY)
UARTFR_DONE = const(UARTFR_TXFE)

def setup(uart):
    base = UART_BASE[uart]
    uartcr_addr = base + UARTCR
    org_uartcr = mem32[uartcr_addr]
    # Enable RX and disable Tx
    new_uartcr = (org_uartcr | UARTCR_RXE) & ~UARTCR_TXE
    mem32[uartcr_addr] = new_uartcr
    print(f'Modified UART {uart} CR from 0x{org_uartcr:08x} to 0x{new_uartcr:08x}')
    while UART[uart].any():
        UART[uart].read(1)

def write(uart, data):
    # Disable Rx and enable Tx
    base = UART_BASE[uart]
    uartcr_addr = base + UARTCR
    org_uartcr = mem32[uartcr_addr]
    new_uartcr = (org_uartcr | UARTCR_TXE) & ~UARTCR_RXE
    mem32[uartcr_addr] = new_uartcr

    UART[uart].write(data)

    # Wait for the data to be sent
    uartfr_addr = base + UARTFR

    while mem32[uartfr_addr] & UARTFR_DONE_MASK != UARTFR_DONE:
        continue

    # Turn off the Tx and restore Rx
    mem32[uartcr_addr] = org_uartcr

def read(uart, n):
    return UART[uart].read(n)

setup(0)
setup(1)

counter = 0

while counter < 5:
    s0 = f'ping{counter:02d}'
    s1 = f'pong{counter:02d}'

    print('----------')

    print(f'UART0: Send "{s0}"')
    write(0, s0)
    r1 = read(1, 6)
    print(f'UART1: Rcvd "{r1}"')

    print('')

    print(f'UART 1: Send "{s1}"')
    write(1, s1)
    r0 = read(0, 6)
    print(f'UART 0: Rcvd "{r0}"')

    counter += 1
    time.sleep(1)
