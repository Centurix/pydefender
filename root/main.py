from struct import unpack
from canvas import NeoDevice
from sdcard import sdcard
"""
Write basic compression algo for image storage

RLE for images

Has to be memory efficient.
"""


def write_marquee(marquee):
    device = NeoDevice(2, 40, 8)

    with open("marquees/{}".format(marquee), "rb") as image:
        pixel_value = image.read(3)
        pixel_count = 0
        while pixel_value != b"":
            device.write_pixel(pixel_count, unpack("BBB", pixel_value))
            pixel_count += 1
            pixel_value = image.read(3)
        device.refresh()


if __name__ == "__main__":
    pass
