def tabulate(words, termwidth=79, pad=0):
    width = max([len(word) for word in words])
    nwords = len(words)
    ncols = max(1, (termwidth + 1) // (width + 1))
    nrows = (nwords + ncols - 1) // ncols
    for row in range(nrows):
        for i in range(row, nwords, nrows):
            print('%-*s' % (width, words[i]), end='\n' if i + nrows >= nwords else ' ')

words = ['.android_secure', 'Download', 'LOST.DIR', 'accel_test.py', 'b2g-updates', 'boot.py', 'data.bin', 'fs.py', 'irq_except.py', 'irq_var.py', 'main.py', 'mod3.py', 'mod4', 'pin_dump.py', 'pin_test.py', 'pwm.py', 'recovery.log', 'screenshots', 'sdread.py', 'size.py', 'updates']
tabulate(words)
