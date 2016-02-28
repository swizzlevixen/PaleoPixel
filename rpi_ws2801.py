"""
rpi_ws2801

Adafruit NeoPixel library port to run WS2801 pixels from the Raspberry Pi SPI


Author: Mark Boszko (boszko@gmail.com)

Raspberry Pi SPI driver code for WS2801 pixels based on PixelPi by Scott Gibson
https://github.com/scottjgibson/PixelPi


Usage:

You will need to translate 3.3V SPI logic levels from the Raspberry Pi to 5V.
Several options are possible, and I have a suggested circuit on my blog post
that describes this project in more detail:

TODO: blog link

- Connect the RPi's MOSI output to the SDI (Serial Data Input) on the WS2801s
- Connect the RPi SCLK clock output to CKI (ClocK Input) on the WS2801
- The RPi's 5V pins will probably not be enough to power a string of
    any significant length. Use an external power supply of appropriate amperage
- Be sure to connect the RPi ground to the LED strip's ground


Version History:

0.5 - Begin development

"""

import argparse
import csv
import socket
import time


# 3 bytes per pixel
PIXEL_SIZE = 3

BLACK = bytearray(b'\x00\x00\x00')
BLUE = bytearray(b'\x00\x00\xff')
BROWN = bytearray(b'\xa5\x2a\x2a')
GRAY = bytearray(b'\x80\x80\x80')
GREY = bytearray(b'\x80\x80\x80')
GREEN = bytearray(b'\x00\x80\x00')
OLIVE = bytearray(b'\x80\x80\x00')
ORANGE = bytearray(b'\xff\xa5\x00')
RED = bytearray(b'\xff\x00\x00')
VIOLET = bytearray(b'\xee\x82\xee')
WHITE = bytearray(b'\xff\xff\xff')
YELLOW = bytearray(b'\xff\xff\x00')
RAINBOW = [RED, GREEN, BLUE, YELLOW, VIOLET, ORANGE, GRAY, OLIVE, BROWN]


def correct_pixel_brightness(pixel):
    corrected_pixel = bytearray(3)
    corrected_pixel[0] = int(pixel[0] / 1.1)
    corrected_pixel[1] = int(pixel[1] / 1.1)
    corrected_pixel[2] = int(pixel[2] / 1.3)

    return corrected_pixel


def all_off():
    pixel_output = bytearray(args.num_leds * PIXEL_SIZE + 3)
    print "Turning all LEDs Off"
    for led in range(args.num_leds):
        pixel_output[led * PIXEL_SIZE:] = filter_pixel(BLACK, 1)
    spidev.write(pixel_output)
    spidev.flush()


def all_on():
    pixel_output = bytearray(args.num_leds * PIXEL_SIZE + 3)
    print "Turning all LEDs On"
    for led in range(args.num_leds):
        pixel_output[led * PIXEL_SIZE:] = filter_pixel(WHITE, 1)
    spidev.write(pixel_output)
    spidev.flush()


def fade():
    pixel_output = bytearray(args.num_leds * PIXEL_SIZE + 3)
    current_color = bytearray(PIXEL_SIZE)
    print "Displaying..."

    while True:
        for color in RAINBOW:
            for brightness in [x * 0.01 for x in range(0, 100)]:
                current_color[:] = filter_pixel(color[:], brightness)
                for pixel_offset in [(x * 3) for x in range(args.num_leds)]:
                    pixel_output[pixel_offset:] = current_color[:]
                spidev.write(pixel_output)
                spidev.flush()
                time.sleep((args.refresh_rate) / 1000.0)
            for brightness in [x * 0.01 for x in range(100, 0, -1)]:
                current_color[:] = filter_pixel(color[:], brightness)
                for pixel_offset in [(x * 3) for x in range(args.num_leds)]:
                    pixel_output[pixel_offset:] = current_color[:]
                spidev.write(pixel_output)
                spidev.flush()
                time.sleep((args.refresh_rate) / 1000.0)


def chase():
    pixel_output = bytearray(args.num_leds * PIXEL_SIZE + 3)
    print "Displaying..."
    current_color = bytearray(PIXEL_SIZE)
    pixel_index = 0
    while True:
        for current_color[:] in RAINBOW:
            for pixel_index in range(args.num_leds):
                pixel_output[((pixel_index - 2) * PIXEL_SIZE):] = filter_pixel(current_color[:], 0.2)
                pixel_output[((pixel_index - 1) * PIXEL_SIZE):] = filter_pixel(current_color[:], 0.4)
                pixel_output[((pixel_index) * PIXEL_SIZE):] = filter_pixel(current_color[:], 1)
                pixel_output += '\x00' * ((args.num_leds - 1 - pixel_index) * PIXEL_SIZE)

                spidev.write(pixel_output)
                spidev.flush()
                time.sleep((args.refresh_rate) / 1000.0)
                pixel_output[((pixel_index - 2) * PIXEL_SIZE):] = filter_pixel(current_color[:], 0)


gamma = bytearray(256)


# Apply Gamma Correction and RGB / GRB reordering
# Optionally perform brightness adjustment
def filter_pixel(input_pixel, brightness):
    output_pixel = bytearray(PIXEL_SIZE)

    input_pixel[0] = int(brightness * input_pixel[0])
    input_pixel[1] = int(brightness * input_pixel[1])
    input_pixel[2] = int(brightness * input_pixel[2])

    output_pixel[0] = gamma[input_pixel[0]]
    output_pixel[1] = gamma[input_pixel[1]]
    output_pixel[2] = gamma[input_pixel[2]]
    return output_pixel


parser = argparse.ArgumentParser(add_help=True, version='1.0', prog='pixelpi.py')
subparsers = parser.add_subparsers(help='sub command help?')
common_parser = argparse.ArgumentParser(add_help=False)
common_parser.add_argument('--verbose', action='store_true', dest='verbose', default=True, help='enable verbose mode')
common_parser.add_argument('--spi_dev', action='store', dest='spi_dev_name', required=False, default='/dev/spidev0.0', help='Set the SPI device descriptor')
common_parser.add_argument('--refresh_rate', action='store', dest='refresh_rate', required=False, default=500, type=int, help='Set the refresh rate in ms (default 500ms)')
parser_fade = subparsers.add_parser('fade', parents=[common_parser], help='Fade Mode - Fade colors on all LEDs')
parser_fade.set_defaults(func=fade)
parser_fade.add_argument('--num_leds', action='store', dest='num_leds', required=True, default=50, type=int,  help='Set the  number of LEDs in the string')
parser_chase = subparsers.add_parser('chase', parents=[common_parser], help='Chase Mode - Chase display test mode')
parser_chase.set_defaults(func=chase)
parser_chase.add_argument('--num_leds', action='store', dest='num_leds', required=True, default=50, type=int,  help='Set the  number of LEDs in the string')
parser_all_on = subparsers.add_parser('all_on', parents=[common_parser], help='All On Mode - Turn all LEDs On')
parser_all_on.set_defaults(func=all_on)
parser_all_on.add_argument('--num_leds', action='store', dest='num_leds', required=True, default=50, type=int,  help='Set the  number of LEDs in the string')
parser_all_off = subparsers.add_parser('all_off', parents=[common_parser], help='All Off Mode - Turn all LEDs Off')
parser_all_off.set_defaults(func=all_off)
parser_all_off.add_argument('--num_leds', action='store', dest='num_leds', required=True, default=50, type=int,  help='Set the  number of LEDs in the string')

args = parser.parse_args()
spidev = file(args.spi_dev_name, "wb")
# Calculate gamma correction table. This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
for i in range(256):
    gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)

args.func()


#print "File Name             = %s" % args.filename
#print "Display Mode          = %s" % args.mode
#print "SPI Device Descriptor = %s" % args.spi_dev_name
#print "Refresh Rate          = %s" % args.refresh_rate
#print "Array Dimensions      = %dx%d" % (args.array_width, args.array_height)
