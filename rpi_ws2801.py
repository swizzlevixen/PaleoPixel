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

from PIL import Image


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


def write_stream(pixels):
    spidev.write(pixels)
    return


def correct_pixel_brightness(pixel):
    corrected_pixel = bytearray(3)
    corrected_pixel[0] = int(pixel[0] / 1.1)
    corrected_pixel[1] = int(pixel[1] / 1.1)
    corrected_pixel[2] = int(pixel[2] / 1.3)

    return corrected_pixel


def pixelinvaders():
    print ("Start PixelInvaders listener " + args.UDP_IP + ":" + str(args.UDP_PORT))
    sock = socket.socket(socket.AF_INET,  # Internet
                      socket.SOCK_DGRAM)  # UDP
    sock.bind((args.UDP_IP, args.UDP_PORT))
    UDP_BUFFER_SIZE = 1024
    while True:
        data, addr = sock.recvfrom(UDP_BUFFER_SIZE)  # blocking call

        pixels_in_buffer = len(data) / PIXEL_SIZE

        pixels = bytearray(pixels_in_buffer * PIXEL_SIZE)

        for pixel_index in range(pixels_in_buffer):
            pixel_to_adjust = bytearray(data[(pixel_index * PIXEL_SIZE):((pixel_index * PIXEL_SIZE) + PIXEL_SIZE)])

            pixel_to_filter = correct_pixel_brightness(pixel_to_adjust)
            pixels[((pixel_index) * PIXEL_SIZE):] = filter_pixel(pixel_to_filter[:], 1)

        write_stream(pixels)
        spidev.flush()


def strip():
    img = Image.open(args.filename).convert("RGB")
    input_image = img.load()
    image_width = img.size[0]
    print "%dx%d pixels" % img.size
    # Create bytearray for the entire image
    # R, G, B byte per pixel, plus extra '0' byte at end for latch.
    print "Allocating..."
    column = [0 for x in range(image_width)]
    for x in range(image_width):
        column[x] = bytearray(args.array_height * PIXEL_SIZE + 1)

    print "Process Image..."
    for x in range(image_width):
        for y in range(args.array_height):
            value = input_image[x, y]
            y3 = y * 3
            column[x][y3] = value[0]
            column[x][y3 + 1] = value[1]
            column[x][y3 + 2] = value[2]

    print "Displaying..."
    while True:
        for x in range(image_width):
            write_stream(column[x])
            spidev.flush()
            time.sleep(0.001)
        time.sleep((args.refresh_rate / 1000.0))


def array():
    images = []
    if ('filelist.txt' in args.filename):
        with open(args.filename, 'r') as file:
            for filename in file:
                filename = filename.rstrip()
                if not filename:
                    continue
                print filename
                images.append(Image.open(filename).convert("RGB"))
    else:
        images.append(Image.open(args.filename).convert("RGB"))

    for img in images:
        input_image = img.load()
        print "%dx%d pixels" % img.size
        print "Reading in array map"
        pixel_map_csv = csv.reader(open("pixel_map.csv", "rb"))
        pixel_map = []
        for p in pixel_map_csv:
            pixel_map.append(p)
        if len(pixel_map) != args.array_width * args.array_height:
            print "Map size error"
        print "Remapping"
        value = bytearray(PIXEL_SIZE)

        # Create a byte array ordered according to the pixel map file
        pixel_output = bytearray(args.array_width * args.array_height * PIXEL_SIZE + 1)
        for array_index in range(len(pixel_map)):
            value = bytearray(input_image[int(pixel_map[array_index][0]), int(pixel_map[array_index][1])])

        pixel_output[(array_index * PIXEL_SIZE):] = filter_pixel(value[:], 1)
        print "Displaying..."
        write_stream(pixel_output)
        spidev.flush()
        time.sleep((args.refresh_rate) / 1000.0)


def pan():
    img = Image.open(args.filename).convert("RGB")
    input_image = img.load()
    image_width = img.size[0]
    print "%dx%d pixels" % img.size
    print "Reading in array map"
    pixel_map_csv = csv.reader(open("pixel_map.csv", "rb"))
    pixel_map = []
    for p in pixel_map_csv:
        pixel_map.append(p)
    if len(pixel_map) != args.array_width * args.array_height:
        print "Map size error"
    print "Remapping"

    # Create a byte array ordered according to the pixel map file
    pixel_output = bytearray(args.array_width * args.array_height * PIXEL_SIZE + 1)
    while True:
        for x_offset in range(image_width - args.array_width):
            for array_index in range(len(pixel_map)):
                value = bytearray(input_image[int(int(pixel_map[array_index][0]) + x_offset), int(pixel_map[array_index][1])])
                pixel_output[(array_index * PIXEL_SIZE):] = filter_pixel(value[:], 1)

        print "Displaying..."
        write_stream(pixel_output)
        spidev.flush()
        time.sleep((args.refresh_rate) / 1000.0)


def all_off():
    pixel_output = bytearray(args.num_leds * PIXEL_SIZE + 3)
    print "Turning all LEDs Off"
    for led in range(args.num_leds):
        pixel_output[led * PIXEL_SIZE:] = filter_pixel(BLACK, 1)
    write_stream(pixel_output)
    spidev.flush()


def all_on():
    pixel_output = bytearray(args.num_leds * PIXEL_SIZE + 3)
    print "Turning all LEDs On"
    for led in range(args.num_leds):
        pixel_output[led * PIXEL_SIZE:] = filter_pixel(WHITE, 1)
    write_stream(pixel_output)
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
                write_stream(pixel_output)
                spidev.flush()
                time.sleep((args.refresh_rate) / 1000.0)
            for brightness in [x * 0.01 for x in range(100, 0, -1)]:
                current_color[:] = filter_pixel(color[:], brightness)
                for pixel_offset in [(x * 3) for x in range(args.num_leds)]:
                    pixel_output[pixel_offset:] = current_color[:]
                write_stream(pixel_output)
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

                write_stream(pixel_output)
                spidev.flush()
                time.sleep((args.refresh_rate) / 1000.0)
                pixel_output[((pixel_index - 2) * PIXEL_SIZE):] = filter_pixel(current_color[:], 0)


gamma = bytearray(256)


# Open SPI device, load image in RGB format and get dimensions:
def load_image():
    print "Loading..."


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
parser_strip = subparsers.add_parser('strip', parents=[common_parser], help='Stip Mode - Display an image using POV and a LED strip')
parser_strip.set_defaults(func=strip)
parser_strip.add_argument('--filename', action='store', dest='filename', required=False, help='Specify the image file eg: hello.png')
parser_strip.add_argument('--array_height', action='store', dest='array_height', required=True, type=int, default='7', help='Set the Y dimension of your pixel array (height)')
parser_array = subparsers.add_parser('array', parents=[common_parser], help='Array Mode - Display an image on a pixel array')
parser_array.set_defaults(func=array)
parser_array.add_argument('--filename', action='store', dest='filename', required=False, help='Specify the image file eg: hello.png')
parser_array.add_argument('--array_width', action='store', dest='array_width', required=True, type=int, default='7', help='Set the X dimension of your pixel array (width)')
parser_array.add_argument('--array_height', action='store', dest='array_height', required=True, type=int, default='7', help='Set the Y dimension of your pixel array (height)')
parser_pixelinvaders = subparsers.add_parser('pixelinvaders', parents=[common_parser], help='Pixelinvaders Mode - setup pixelpi as a Pixelinvaders slave')
parser_pixelinvaders.set_defaults(func=pixelinvaders)
parser_pixelinvaders.add_argument('--udp-ip', action='store', dest='UDP_IP', required=True, help='Used for PixelInvaders mode, listening address')
parser_pixelinvaders.add_argument('--udp-port', action='store', dest='UDP_PORT', required=True, default=6803, type=int, help='Used for PixelInvaders mode, listening port')
parser_fade = subparsers.add_parser('fade', parents=[common_parser], help='Fade Mode - Fade colors on all LEDs')
parser_fade.set_defaults(func=fade)
parser_fade.add_argument('--num_leds', action='store', dest='num_leds', required=True, default=50, type=int,  help='Set the  number of LEDs in the string')
parser_chase = subparsers.add_parser('chase', parents=[common_parser], help='Chase Mode - Chase display test mode')
parser_chase.set_defaults(func=chase)
parser_chase.add_argument('--num_leds', action='store', dest='num_leds', required=True, default=50, type=int,  help='Set the  number of LEDs in the string')
parser_pan = subparsers.add_parser('pan', parents=[common_parser], help='Pan Mode - Pan an image across an array')
parser_pan.set_defaults(func=pan)
parser_pan.add_argument('--filename', action='store', dest='filename', required=False, help='Specify the image file eg: hello.png')
parser_pan.add_argument('--array_width', action='store', dest='array_width', required=True, type=int, default='7', help='Set the X dimension of your pixel array (width)')
parser_pan.add_argument('--array_height', action='store', dest='array_height', required=True, type=int, default='7', help='Set the Y dimension of your pixel array (height)')
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
