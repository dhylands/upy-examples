import pyb

# board.D23 is cpu.C2 and has FTM0_CH1 on af 4

#pin = pyb.Pin.board.D23

pin = pyb.Pin.board.LED

# FTMx is clocked at F_BUS @ 48 MHz
# With a prescaler of 128, this drops to 375 kHz
# With a period of 37500, this wraps about 10 times/second

ftm = pyb.Timer(0, prescaler=128, period=37500)

blink_counter = 0
prev_counter = ftm.counter()
while True:
    curr_counter = ftm.counter()
    if curr_counter < prev_counter:
        # wrap
        blink_counter = (blink_counter + 1) % 10
        if blink_counter == 1 or blink_counter == 3:
            pin.high()
        elif blink_counter == 2 or blink_counter == 4:
            pin.low()
    prev_counter = curr_counter

