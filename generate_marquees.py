#!/usr/bin/env python3
import os
import click
import struct
from PIL import Image
"""
Generate marquees from the assets folder
"""


@click.command()
def main():
    """
    Clear the marquees folder
    Iterate over assets/marquees
    Load into Pillow
    Grab the RGB of each pixel
    Create a list of tuples for RGB values
    :return:
    """
    asset_path = "assets/marquees"
    dst_path = "root/marquees"
    for image in os.listdir(asset_path):
        if image.endswith(".png"):
            filename, ext = os.path.splitext(image)
            im = Image.open(os.path.join(asset_path, image))
            with open(os.path.join(dst_path, filename), "wb") as output:
                for y in range(0, im.height):
                    for x in range(0, im.width):
                        pixel = im.getpixel((x, y))
                        output.write(
                            struct.pack('BBB', pixel[0], pixel[1], pixel[2])
                        )
    raise click.exceptions.Exit(0)


if __name__ == "__main__":
    main()
