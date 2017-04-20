import pyb
import stm
    
@micropython.asm_thumb
def _write_packet(r0, r1, r2):      # uart(r0) buf(r1) len(r2)

    movw(r3, 0xffff)                # uart(r0) &= 0x7fffffff
    movt(r3, 0x7fff)                #
    and_(r0, r3)                    #

    # Disable the Receiver

    ldr(r3, [r0, stm.USART_CR1])    # uart->CR1 &= ~USART_CR1_RE
    mov(r4, 0x04)                   #
    bic(r3, r4)                     #
    str(r3, [r0, stm.USART_CR1])    #

    add(r2, r2, r1)                 # buf_end(r2) = &buf(r1)[len(r2)]
    sub(r2, 1)                      # buf_end--

# loop
    label(loop)
    cmp(r1, r2)
    bhi(endloop)                    # branch if buf > buf_end
    
    # Wait for the Transmit Data Register to be Empty

    mov(r4, 0x80)                   # while ((uart->SR & USART_SR_TXE) == 0) {
# wait_txe                          #   ;
    label(wait_txe)                 #
    ldr(r3, [r0, stm.USART_SR])     #
    tst(r3, r4)                     #
    beq(wait_txe)                   # }

    # Disable interrupts from the time that we write the last character
    # until the tx complete bit is set. This ensures that we re-enable
    # the Rx as soon as possible after the last character has left
    cmp(r1, r2)
    bne(write_dr)                   # if buf ==  buf_end
    cpsid(i)                        #   disable_irq
# write_dr
    label(write_dr)

    # Write one byte to the UART

    ldrb(r3, [r1, 0])               # uart->DR = *buf++
    add(r1, 1)                      #
    str(r3, [r0, stm.USART_DR])     #

    b(loop)
# endloop
    label(endloop)

    # Wait for Transmit Complete (i.e the last bit of transmitted data has left the shift register)

    mov(r4, 0x40)                   # while ((uart->SR & USART_SR_TC) == 0) {
# wait_tx_complete                  #   ;
    label(wait_tx_complete)         #
    ldr(r3, [r0, stm.USART_SR])     #
    tst(r3, r4)                     #
    beq(wait_txe)                   # }

    # Re-enable the receiver

    ldr(r3, [r0, stm.USART_CR1])    # uart->CR1 |= USART_CR1_RE
    mov(r4, 0x04)                   #
    orr(r3, r4)                     #
    str(r3, [r0, stm.USART_CR1])    #

    cpsie(i)                        # enable_irq

def inspect(f, nbytes=16):
    import stm
    import array
    import ubinascii
    @micropython.asm_thumb
    def dummy():
        pass
    if type(f) != type(dummy):
        raise ValueError('expecting an inline-assembler function')
    baddr = bytes(array.array('O', [f]))
    addr = baddr[0] | baddr[1] << 8 | baddr[2] << 16 | baddr[3] << 24
    print('function object at: 0x%08x' % addr)
    print('number of args: %u' % stm.mem32[addr + 4])
    code_addr = stm.mem32[addr + 8]
    print('machine code at: 0x%08x' % code_addr)
    print('----------')
    print('import binascii')
    print("with open('code.bin', 'wb') as f:")
    import ubinascii
    hex_str = ubinascii.hexlify(bytearray([stm.mem8[code_addr + i] for i in range(nbytes)]))
    print("    f.write(binascii.unhexlify(%s))" % hex_str)
    print('----------')

def test():
    inspect(_write_packet, 64)
    pyb.repl_uart(pyb.UART(4, 115200))
    uart = pyb.UART(6, 1000000)
    buf = bytearray(b'123456')
    _write_packet(stm.USART6 | 0x80000000, buf, len(buf))

test()
