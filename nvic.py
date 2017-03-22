import machine

SCS = 0xE000E000
SCB = SCS + 0x0D00
NVIC = SCS + 0x0100
VTOR = SCB + 0x08

SCB_SHP = SCB + 0x18
NVIC_PRIO = NVIC + 0x300

def dump_nvic():
    print('NVIC_PRIO = {:08x} @ {:08x}'.format(machine.mem32[NVIC_PRIO], NVIC_PRIO))
    print('VTOR      = {:08x} @ {:08x}'.format(machine.mem32[VTOR], VTOR))

    print('System IRQs')
    for i in range(12):
        irq = -(16 - (i + 4))
        prio = machine.mem8[SCB_SHP + i] >> 4
        if prio > 0:
            print('{:3d}:{:d}'.format(irq, prio))

    print('Regular IRQs')
    for irq in range(80):
        prio = machine.mem8[NVIC_PRIO + irq] >> 4
        if prio > 0:
            print('{:3d}:{:d}'.format(irq, prio))

def nvic_set_prio(irq, prio):
    if irq < 0:
        idx = (irq & 0x0f) - 4
        machine.mem8[SCB_SHP + idx] = prio << 4
    else:
        machine.mem8[NVIC_PRIO + irq] = prio << 4


dump_nvic()
