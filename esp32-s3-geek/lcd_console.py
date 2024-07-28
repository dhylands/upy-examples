"""
Add dupterm support for directing stdout to the ESP32-S3-Geek LCD.
"""

import io
from typing import Union
import uos

from lcd_text import LCD_Text

class LcdConsole(io.IOBase):
    """Add dupterm support for the LCD."""

    def __init__(self) -> None:
        self.lcd = LCD_Text()

    def readinto(self, _buf, *_args) -> Union[None, int]:
        """Reads data into a buffer.
           Since we're only supporting output, we just return None.
        """
        return None

    def write(self, buf):
        """Writes `buf` to the LCD."""
        return self.lcd.write(buf)

lcd = LcdConsole()
uos.dupterm(lcd)
