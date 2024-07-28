"""
Implements Text based LCD output.
"""

from lcd import LCD
from log import log

class LCD_Text(LCD):

    def __init__(self) -> None:
        super().__init__()
        self.fill(0)
        self.row_height = 9
        self.col_width = 8
        self.num_rows = self.height // self.row_height
        self.num_cols = self.width // self.col_width
        self.row = 0
        self.col = 0
        self.bg_color = 0
        self.fg_color = self.white
        self.scroll_height = (self.num_rows - 1) * self.row_height

    def print(self, *args, end='\n'):
        """Convenience function so you don't need to remember to put the \n
           at the end of the line.
        """
        s = ' '.join(str(arg) for arg in args) + end
        self.write(s)

    def write(self, s: str) -> Union[int|None]:
        # s = data.decode('ascii')
        if len(s) < 1:
            return None
        count = 0
        for ch in s:
            self.write_char(ch)
            count += 1
        self.show()
        return count

    def write_char(self, ch: str) -> None:
        log('ch =', ch)
        if isinstance(ch, int):
            ch = chr(ch)
        if ch == '\n':
            self.col = 0
            self.row += 1
        elif self.col >= self.num_cols:
            self.col = 0
            self.row += 1
        if self.row >= self.num_rows:
            self.scroll_row()
            self.row -= 1
        if ch >= ' ':
            x, y = self.calc_text_posn(self.row, self.col)
            self.text(ch, x, y, self.fg_color)
            self.col += 1

    def calc_text_posn(self, row: int, col: int) -> Tuple[int, int]:
        return (col * self.col_width, row * self.row_height)

    def scroll_row(self) -> None:
        self.scroll(0, -self.row_height)
        self.rect(0, self.scroll_height, self.width, self.row_height, self.bg_color, True)

def main():
    lcd = LCD_Text()
    lcd.write('This is a test\n')
    lcd.write('to see what ')
    lcd.write('happens\n')
    for i in range(15):
        lcd.print(i)

if __name__ == '__main__':
    main()
