from machine import Pin
from neopixel import NeoPixel


class NeoImageLoader:
    pass


class NeoDevice:
    def __init__(self, pin, width, height, snake=True):
        self.pin_number = pin
        self.width = width
        self.height = height
        self.snake = snake

        self._pin = Pin(self.pin_number, Pin.OUT)
        self._device = NeoPixel(self._pin, self.total_pixels)

    @property
    def total_pixels(self):
        return self.width * self.height

    def translate(self, pixel_position):
        """
        Pixel top left to bottom right to
        snake position from bottom right to left
        :param pixel_position:
        :return:
        """
        # Work out the X/Y from the top left
        x = pixel_position % self.width
        y = pixel_position // self.width

        # X is our column
        column_offset = (self.width - 1 - x) * self.height
        if x % 2 == 0:  # Even column, runs downwards
            return column_offset + y
        else:
            return column_offset + (self.height - 1) - y

    def translate_xy(self, x, y):
        return self.translate(y * self.width + x)

    def write_pixel(self, pixel_number, colour):
        location = self.translate(pixel_number)
        print("Location: {}".format(location))
        print("Pixel number: {}".format(pixel_number))
        print("Colour: {}".format(colour))
        print("Device item: {}".format(self._device[self.translate(pixel_number)]))
        self._device[self.translate(pixel_number)] = colour

    def write_absolute_pixel(self, pixel_number, colour):
        self._device[pixel_number] = colour

    def write_xy_pixel(self, x, y, colour):
        self._device[self.translate_xy(x, y)] = colour

    def refresh(self):
        self._device.write()


class ViewPort:
    """
    The view port for a NeoCanvas. Present a window onto a device
    """
    def __init__(self, neo_device, neo_canvas):
        self._device = neo_device
        self._canvas = neo_canvas

    def display(self, x, y):
        """
        Write the canvas to the device from position x, y
        +--------------------------+
        |    x                     |
        |   y+-------------+       |
        |    |             |       |
        |    +-------------+h      |
        |                  w       |
        +--------------------------+
        :param x:
        :param y:
        :return:
        """
        dev_x = 0
        dev_y = 0
        for row in range(y, y + self._device.height):
            for col in range(x, x + self._device.width):
                pixel = self._canvas.get_pixel(col, row)
                self._device.write_xy_pixel(dev_x, dev_y, pixel)


class NeoCanvas:
    """
    A NeoPixel canvas
    This is a virtual canvas for driving data to a NeoPixel array
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [(0, 0, 0)] * self.total_pixels

    @property
    def total_pixels(self):
        return self.width * self.height

    def get_viewport(self, neo_device):
        """
        Return a viewport for a specific device
        :param neo_device:
        :return:
        """
        return ViewPort(neo_device, self)

    def get_pixel(self, x, y):
        return self.canvas[y * self.width + x]

    def set_pixel(self, x, y, colour):
        self.canvas[y * self.width + x] = colour
