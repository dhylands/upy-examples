import pyb
import gc

us = pyb.Timer(2, prescaler=83, period=0x7fffffff).counter
clean = gc.collect
begin = pyb.disable_irq
end = pyb.enable_irq

def test(code='pass', N=None, opt=None, irqOff=True, debug=False):
    prefix = "@micropython.%s" % opt if opt else ""
    begins, ends = ("begin()", "end()") if irqOff else ("", "")
    wrap = "for i in range(%s): " % N if N else ""
    testbench = ("""if 1:
        %s
        def _test():
            %s%s; pass
       
        %s
        def _ref():
            %spass
       
        %s
        clean()
        t0 = us()
        _test()
        t1 = us()
        clean()
        t2 = us()
        _ref()
        t3 = us()
        clean()
        t4 = us()
        %s
        """ % (prefix, wrap, code, prefix, wrap, begins, ends))
    if debug:
        print(testbench)
        return
    exec(testbench)
    dt = (t1-t0) - (t3-t2)
    dtgc = (t2-t1) - (t4-t3)
    return dt/N if N else dt, dtgc

#test('1*1', 8192, debug=True)

I = 1
F = 1.
def tabulate(opt=None, irqOff=True, ):
    codes = "1*1", "I*I", "1.*1.", "F*F"
    print("Time (us) measured using", opt or 'bytecode',
          "without interrupts" if irqOff else "")
    print("%6s"% 'counts', end="")
    for code in codes:
        print(" %5s %3s"% (code, 'gbc'), end="")
    print()
    for i in range(14):
        print("%6d"% 2**i, end="")
        for code in codes:
            #if ((opt=='native' and
            #     ("." in code and 2**i >= 64 or
            #      "F" in code and 2**i >= 256)) or
            #    (opt=='viper' and
            #     ("1" in code and 2**i >= 1024 or
            #      "I" in code and 2**i >= 1024 or
            #      "." in code and 2**i >= 64 or
            #      "F" in code and 2**i >= 256))):
            #    # These cases bricked a pyboard
            #    print("   bricked", end="")
            #else:
            print(" %5d %3d"% test(code, 2**i, opt), end="")
        print()

print("Hold USR button until GREEN+YELLOW after reset to recover bricked pyboard")
for opt in (None, 'native', 'viper'):
    tabulate(opt, opt!='viper')

