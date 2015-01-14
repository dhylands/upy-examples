import pyb
import stm

# For this example, we assume that there is a wire connected from X1 to Y1
#
# Y1 corresponds to Timer 8 channel 1, which we'll use as output
# X1 corresponds to Timer 2 channel 1, which we'll use an the input gate
#
# We'll confgure X1 as a GPIO and initially drive it high (which corresponds
# to not counting). Then we'll toggle that pin when the user presses a key.

y1 = pyb.Pin('Y1', pyb.Pin.OUT_PP)
y1.high()

# tim2's source_freq is 84 MHz, so we'll set the prescalar to divide by
# 8399, which will drop the counter freq to 10 kHz, and we'll set the 
# period to be 50,000 clock ticks, so that it rolls over once every 5 seconds
#
# Note that the prescalar for tim2 is 16-bit but the period is 32-bit.

tim2 = pyb.Timer(2, prescaler=8399, period=49999)

# We're following the example on page 603 of the RM0090 document (STM32F405
# datasheet) (I copied the pertinent section below for reference):
#
#   Slave mode: Gated mode
#
#   The counter can be enabled depending on the level of a selected input.
#   In the following example, the upcounter counts only when TI1 input is low:
#
#       - Configure the channel 1 to detect low levels on TI1. Configure the
#         input filter duration (in this example, we don't need any filter, so
#         we keep IC1F=0000). The capture prescaler is not used for triggering,
#         so you don't need to configure it. The CC1S bits select the input
#         capture source only, CC1S=01 in TIMx_CCMR1 register. Write CC1P=1
#         and CC1NP=0 in TIMx_CCER register to validate the polarity (and
#         detect low level only).
#
#       - Configure the timer in gated mode by writing SMS=101 in TIMx_SMCR
#         register. Select TI1 as the input source by writing TS=101 in
#         TIMx_SMCR register.
#
#       - Enable the counter by writing CEN=1 in the TIMx_CR1 register (in
#         gated mode, the counter doesn't start if CEN=0, whatever is the
#         trigger input level). 
#
#   The counter starts counting on the internal clock as long as TI1 is low
#   and stops as soon as TI1 becomes high. The TIF flag in the TIMx_SR register
#   is set both when the counter starts or stops.
#
# If we set the channel up for input capture, then it will set CC1S to 01
# Setting the polarity to FALLING will set CC1P=1 and CC1NP=0

ch1 = tim2.channel(1, pyb.Timer.IC, pin=pyb.Pin.board.X1, polarity=pyb.Timer.FALLING)

# We'll need to set the SMS=101 and TS=101 in the SMCR register ourselves,
# since none of the exposed APIs maniipulate that register.
#
# SMS is bits 2:0 and TS is bits 6:4

smcr = stm.mem16[stm.TIM2 + stm.TIM_SMCR]
smcr &= 0b1111111110001000
smcr |= 0b0000000001010101
stm.mem16[stm.TIM2 + stm.TIM_SMCR] = smcr

usb_vcp = pyb.USB_VCP()

while True:
    if usb_vcp.any():
        ch = usb_vcp.read()
        if y1.value():
            print("Counter enabled")
            y1.low()
        else:
            y1.high()
            print("Counter disabled")
    pyb.delay(100)
    cnt = tim2.counter()
    print('cnt = %d' % cnt)

