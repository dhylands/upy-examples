# Example which shows RTC Alarm

import pyb
import stm
import time

alarm_fired = False

def alarm_cb(line):
    global alarm_fired
    alarm_fired = True
    print('alarm fired')

def sw_cb(line):
    print('sw_cb')

alarm_exti = pyb.ExtInt(17, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, alarm_cb)

rtc = pyb.RTC()

RTC_ALRMASSR = 0x44                 # This constant is missing from stm

def disable_alarm_a():
    rtc_cr = stm.mem32[stm.RTC + stm.RTC_CR]
    rtc_cr &= ~(1 << 8)    # Set ALRAE (Alarm A Enable)
    stm.mem32[stm.RTC + stm.RTC_CR] = rtc_cr

def enable_alarm_a():
    rtc_cr = stm.mem32[stm.RTC + stm.RTC_CR]
    rtc_cr |= (1 << 8)    # Set ALRAE (Alarm A Enable)
    rtc_cr |= (1 << 12)   # Set ALRAIE (Alarm A Interrupt Enable)
    stm.mem32[stm.RTC + stm.RTC_CR] = rtc_cr

def wait_for_alarm_a_ready():
    while True:
        rtc_isr = stm.mem32[stm.RTC + stm.RTC_ISR]
        if (rtc_isr & (1 << 0)) == 1:
            return

def disable_write_protection():
    stm.mem32[stm.RTC + stm.RTC_WPR] = 0xca
    stm.mem32[stm.RTC + stm.RTC_WPR] = 0x53

def enable_write_protection():
    stm.mem32[stm.RTC + stm.RTC_WPR] = 0xff

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
    alrmar |= (1 << 31)                 # set MSK4 - date doesn't matter
    alrmar |= (1 << 23)                 # set MSK3 - hours don't matter
    alrmar |= (alarm_min // 10) << 12   # BCD tens of minutes
    alrmar |= (alarm_min % 10) << 8     # BCD units of minutes
    alrmar |= (alarm_sec // 10) << 4    # BCD tens of seconds
    alrmar |= (alarm_sec % 10) << 0     # BCD units of seconds
    stm.mem32[stm.RTC + stm.RTC_ALRMAR] = alrmar
    stm.mem32[stm.RTC + RTC_ALRMASSR] = 0   # No comparison on subseconds

    alarm_fired = False
    enable_alarm_a()
    enable_write_protection()


rtc_time = rtc.datetime()
print('Current time is {:02}:{:02}:{:02}'.format(rtc_time[4], rtc_time[5], rtc_time[6]))

set_alarm_3_seconds_in_future()

for i in range(14):
    pyb.delay(500)
    rtc_time = rtc.datetime()
    print('Current time is {:02}:{:02}:{:02}'.format(rtc_time[4], rtc_time[5], rtc_time[6]))
    if alarm_fired:
        set_alarm_3_seconds_in_future()

print('Done')
