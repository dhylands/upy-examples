# Example which shows RTC Alarm

import pyb
import stm
import time
import os

# Bit field constants (using names from CMSIS)
RTC_CR_ALRAE = 1 << 8
RTC_CR_ALRIE = 1 << 12
RTC_ISR_ALRAWF = 1 << 0
RTC_ISR_ALRAF = 1 << 8
RTC_ALRMAR_SU_Pos = 0
RTC_ALRMAR_ST_Pos = 4
RTC_ALRMAR_MNU_Pos = 8
RTC_ALRMAR_MNT_Pos = 12
RTC_ALRMAR_MSK3 = 1 << 23
RTC_ALRMAR_MSK4 = 1 << 31
PWR_CR_DBP = 1 << 8
RCC_APB1ENR_PWREN = 1 << 28

alarm_fired = False

def alarm_cb(line):
    global alarm_fired
    alarm_fired = True
    print('alarm fired')

def sw_cb(line):
    print('sw_cb')

def rtc_regs():
    for name in ['TR', 'DR', 'CR', 'ISR', 'WUTR', 'ALRMAR', 'WPR', 'SSR', 'TAFCR', 'ALRMASSR']:
        offset = eval('stm.RTC_' + name)
        val = stm.mem32[stm.RTC + offset] & 0xffffffff
        print('{:8s} = {:08x}'.format(name, val))

machine = os.uname().machine
print('machine =', machine)

if 'NUCLEO-F091RC' in machine:
    sw_name = 'USER_B1'
else:
    sw_name = 'SW'

if 'STM32L4' in machine:
    rtc_exti_alarm_line = 18
    # SW on the NUCLEO_L476RG
    sw_exti = pyb.ExtInt(sw_name, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, sw_cb)
else:
    rtc_exti_alarm_line = 17
    # SW on the Pyboard 1.1
    sw_exti = pyb.ExtInt(sw_name, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, sw_cb)

# The F0 and F4 have Backup Domain Protection and this needs to be disabled
# before writes to the RTC registers are enabled.
USE_DBP = 'STM32F0' in machine or 'STM32F4' in machine
if USE_DBP:
    # Ensure that the PWR clock is enabled (so we can tweak PWR_CR)
    apb1enr = stm.mem32[stm.RCC + stm.RCC_APB1ENR]
    apb1enr |= RCC_APB1ENR_PWREN
    stm.mem32[stm.RCC + stm.RCC_APB1ENR] = apb1enr

alarm_exti = pyb.ExtInt(rtc_exti_alarm_line, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, alarm_cb)
# alarm_exti.regs()

rtc = pyb.RTC()

def disable_alarm_a():
    rtc_cr = stm.mem32[stm.RTC + stm.RTC_CR]
    rtc_cr &= ~RTC_CR_ALRAE     # Clear ALRAE (Alarm A Enable)
    stm.mem32[stm.RTC + stm.RTC_CR] = rtc_cr

def enable_alarm_a():
    rtc_isr = stm.mem32[stm.RTC + stm.RTC_ISR]
    rtc_isr &= ~RTC_ISR_ALRAF   # Clear ALRAF
    stm.mem32[stm.RTC + stm.RTC_ISR] = rtc_isr
    rtc_cr = stm.mem32[stm.RTC + stm.RTC_CR]
    rtc_cr |= RTC_CR_ALRAE      # Set ALRAE (Alarm A Enable)
    rtc_cr |= RTC_CR_ALRIE      # Set ALRAIE (Alarm A Interrupt Enable)
    stm.mem32[stm.RTC + stm.RTC_CR] = rtc_cr

def wait_for_alarm_a_ready():
    while True:
        rtc_isr = stm.mem32[stm.RTC + stm.RTC_ISR]
        if (rtc_isr & RTC_ISR_ALRAWF) == 1:
            return

def disable_write_protection():
    if USE_DBP:
        pwr_cr = stm.mem32[stm.PWR + stm.PWR_CR]
        pwr_cr |= PWR_CR_DBP  # Enable access to RTC & Backup registers
        stm.mem32[stm.PWR + stm.PWR_CR] = pwr_cr
    stm.mem32[stm.RTC + stm.RTC_WPR] = 0xca
    stm.mem32[stm.RTC + stm.RTC_WPR] = 0x53

def enable_write_protection():
    stm.mem32[stm.RTC + stm.RTC_WPR] = 0xff
    if USE_DBP:
        pwr_cr = stm.mem32[stm.PWR + stm.PWR_CR]
        pwr_cr &= ~PWR_CR_DBP # Disable access to RTC & Backup registers
        stm.mem32[stm.PWR + stm.PWR_CR] = pwr_cr

def set_alarm_3_seconds_in_future():
    global alarm_fired
    rtc_time = list(rtc.datetime())

    # The order of the fields in the RTC time differs from the order that mktime wants
    # We call mktime since it will re-normalize the time if the seconds goes
    # above 59
    alarm_time = [rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[4], rtc_time[5], rtc_time[6], 0, 0]
    alarm_time[5] += 3  # Set the alarm 3 seconds in the future
    alarm_time = time.localtime(time.mktime(alarm_time)) # Normalize in case seconds wrap
    alarm_min = alarm_time[4]
    alarm_sec = alarm_time[5]
    print('Setting alarm for {:02}:{:02}:{:02}'.format(alarm_time[3], alarm_time[4], alarm_time[5]))

    disable_write_protection()
    disable_alarm_a()
    wait_for_alarm_a_ready()

    alrmar = 0
    alrmar |= RTC_ALRMAR_MSK4           # set MSK4 - date doesn't matter
    alrmar |= RTC_ALRMAR_MSK3           # set MSK3 - hours don't matter
    alrmar |= (alarm_min // 10) << RTC_ALRMAR_MNT_Pos # BCD tens of minutes
    alrmar |= (alarm_min % 10)  << RTC_ALRMAR_MNU_Pos # BCD units of minutes
    alrmar |= (alarm_sec // 10) << RTC_ALRMAR_ST_Pos  # BCD tens of seconds
    alrmar |= (alarm_sec % 10)  << RTC_ALRMAR_SU_Pos  # BCD units of seconds
    stm.mem32[stm.RTC + stm.RTC_ALRMAR] = alrmar
    stm.mem32[stm.RTC + stm.RTC_ALRMASSR] = 0   # No comparison on subseconds
    alrmar2 = stm.mem32[stm.RTC + stm.RTC_ALRMAR] & 0xffffffff
    if alrmar != alrmar2:
        print('#####')
        print('##### Setting ALRMAR failed alrmar = {:08x} alrmar2 = {:08x}'.format(alrmar, alrmar2))
        print('#####')

    alarm_fired = False
    enable_alarm_a()
    enable_write_protection()


rtc_time = rtc.datetime()
print('Current time is {:02}:{:02}:{:02}'.format(rtc_time[4], rtc_time[5], rtc_time[6]))

# rtc_regs()
set_alarm_3_seconds_in_future()
# rtc_regs()

for i in range(20):
    time.sleep_ms(500)
    rtc_time = rtc.datetime()
    print('Current time is {:02}:{:02}:{:02}'.format(rtc_time[4], rtc_time[5], rtc_time[6]))
    if alarm_fired and i < 14:
        set_alarm_3_seconds_in_future()


print('Done')
