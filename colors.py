# Example which shows using ANSI color codes to print color to the terminal
# window.

def color(this_color, string):
    return "\033[" + this_color + "m" + string + "\033[0m"

for i in range(30, 38):
    c = str(i)
    print('This is %s' % color(c, 'color ' + c))

    c = '1;' + str(i)
    print('This is %s' % color(c, 'color ' + c))
