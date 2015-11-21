#
# Test file to send some commands to a bioloid servo
#

import pyb
import stm

# Bioloid command to set the led on on servo 1
#   Sending WRITE to ID 1 offset 0x19 len 1
#   W: 0000: ff ff 01 04 03 19 01 dd
#   R: 0000: ff ff 01 02 00 fc
#   Rcvd Status: None
#
# Bioloid command to set the led off on servo 1
#   Sending WRITE to ID 1 offset 0x19 len 1
#   W: 0000: ff ff 01 04 03 19 00 de
#   R: 0000: ff ff 01 02 00 fc
#   Rcvd Status: None
#
# The checksum for a packet is the sum of the characters in the packet
# (which starts after the second 0xff) and then bitwise inverted.

def checksum(packet):
    return ~sum(packet[2:len(packet)-1]) & 0xff

def fill_checksum(packet):
    packet[len(packet) - 1] = checksum(packet)

def dump(label, packet):
    print(label, ' '.join('{:02x}'.format(x) for x in packet))

def pkt_led_on(servo_id):
    packet = bytearray((0xff, 0xff, servo_id, 4, 3, 0x19, 1, 0))
    fill_checksum(packet)
    return packet

def pkt_led_off(servo_id):
    packet = bytearray((0xff, 0xff, servo_id, 4, 3, 0x19, 0, 0))
    fill_checksum(packet)
    return packet

def enable_rx():
    """Set the RE bit in the CR1 register."""
    cr1 = stm.mem16[stm.USART6 + stm.USART_CR1]
    cr1 |= 0x04
    stm.mem16[stm.USART6 + stm.USART_CR1] = cr1

def disable_rx():
    """Clear the RE bit in the CR1 register."""
    cr1 = stm.mem16[stm.USART6 + stm.USART_CR1]
    cr1 &= ~0x04
    stm.mem16[stm.USART6 + stm.USART_CR1] = cr1

def led_on():
    disable_rx()
    u6.write(pkt_led_on(12))
    enable_rx()

def led_off():
    disable_rx()
    u6.write(pkt_led_off(12))
    enable_rx()

def process_char():
    while True:
        char = u6.readchar()
        if char == -1:
            return
        print('Got {:02x}'.format(char))
    

u6 = pyb.UART(6, 1000000)

# Turn on HDSEL - which puts the UART in half-duplex mode. This connects
# Rx to Tx internally, and only enables the transmitter when there is data
# to send.
cr3 = stm.mem16[stm.USART6 + stm.USART_CR3]
cr3 |= 0x08
stm.mem16[stm.USART6 + stm.USART_CR3] = cr3


for i in range(4):
    print('on')
    led_on()
    process_char()
    print('off')
    led_off()
    process_char()

