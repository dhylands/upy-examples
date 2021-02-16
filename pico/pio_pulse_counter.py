# Example using PIO to count pulses on an input pin.
#
# The following assumes Pin 17 is jumper to Pin 16
#
#   pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
#   pin17 = Pin(17, Pin.OUT)
#   pin17.low()
#
#   pc = PulseCounter(0, pin16)
#
#   print("pulse count =", pc.get_pulse_count())
#
#   pin17.high()
#   pin17.low()
#
#   print("pulse count =", pc.get_pulse_count())
#
#   pin17.high()
#   pin17.low()
#
#   print("pulse count =", pc.get_pulse_count())

import rp2

@rp2.asm_pio()
def pulse_counter():
    label("loop")
    # We wait for a rising edge
    wait(0, pin, 0)
    wait(1, pin, 0)
    jmp(x_dec, "loop")  # If x is zero, then we'll wrap back to beginning


class PulseCounter:
    # pin should be a machine.Pin instance
    def __init__(self, sm_id, pin):
        self.sm = rp2.StateMachine(0, pulse_counter, in_base=pin)
        # Initialize x to zero
        self.sm.put(0)
        self.sm.exec("pull()")
        self.sm.exec("mov(x, osr)")
        # Start the StateMachine's running.
        self.sm.active(1)

    def get_pulse_count(self):
        self.sm.exec("mov(isr, x)")
        self.sm.exec("push()")
        # Since the PIO can only decrement, convert it back into +ve
        return -self.sm.get() & 0x7fffffff
