from machine import Pin,SPI,PWM
import framebuf
import time

BL = 7
DC = 8
CS = 10
SCK = 12
MOSI = 11
RST = 9

class LCD(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135

        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,50_000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)

        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(1000)
        self.set_backlight(1.0)

    def set_backlight(self, level: float) -> None:
        if level > 1.0:
            level = 1.0
        elif level < 0.0:
            level = 0.0
        self.pwm.duty_u16(int(level * 65535))

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)
    @micropython.viper
    def swap(self):
        buf=ptr8(self.buffer)
        for x in range(0,240*135*2,2):
            tt=buf[x]
            buf[x]=buf[x+1]
            buf[x+1]=tt
    @micropython.viper
    def ins(self,ins_data,ins_len:int,start:int):
        ins_buf=ptr8(ins_data)
        buf=ptr8(self.buffer)
        for x in range(ins_len):
            buf[start+x]=ins_buf[x]
    @micropython.viper
    def mirror(self):
        buf=ptr8(self.buffer)
        for y in range(0,135):
            for x in range(0,120):
                temp_x=(240-x)*2
                temp_y=y*480
                t1=buf[x*2+temp_y]
                t2=buf[x*2+temp_y+1]
                buf[x*2+temp_y]=buf[temp_x+temp_y]
                buf[x*2+temp_y+1]=buf[temp_x+temp_y+1]
                buf[temp_x+temp_y]=t1
                buf[temp_x+temp_y+1]=t2


    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.swap()
        self.spi.write(self.buffer)
        self.swap()
        self.cs(1)

if __name__ == '__main__':
    import gc
    gc.enable()
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(65535)#max 65535

    LCD = LCD()
    #color BRG
    LCD.fill(0)
    LCD.show()
    LCD.text("ESP32-S3-GEEK",60,40,0XF800)
    LCD.text("read bmp file ...",60,80,0X001F)
    LCD.show()

    while(1):
        time.sleep(1)

    LCD.fill(0xFFFF)
