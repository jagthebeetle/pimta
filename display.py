from luma.led_matrix import device
from luma.core.interface import serial
from luma.core import legacy
from luma.core.legacy import font

class Matrix(object):
    def __init__(self, n=4):
        self.iface = serial.spi(port=0, device=0, gpio=serial.noop())
        self.device = device.max7219(self.iface, cascaded=n,
                                     block_orientation=-90,
                                     rotate=0)
    def print_msg(self, msg, debug=0):
        if not debug:
            legacy.show_message(self.device, msg, fill='white',
                                font=font.proportional(font.CP437_FONT))
        else:
            print msg

if __name__ == '__main__':
    leds = Matrix()
    leds.print_msg('Hello World')
