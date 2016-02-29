#!/usr/bin/env python
"""
Adafruit NeoPixel library port to control the older WS2801 pixels from 
  Raspberry Pi hardware SPI. Includes Adafruit “strandtest”-style functions
  and performs a self-test if run as main.


Author: Mark Boszko (boszko+paleopixel@gmail.com)

Raspberry Pi SPI driver code for WS2801 pixels based on Adafruit_LEDpixels.py
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

Python port of NeoPixel library based on the rpi_ws281x library port,
  by Tony DiCola and Jeremy Garff
https://github.com/jgarff/rpi_ws281x


Usage:

You'll need to translate 3.3V SPI logic levels from the Raspberry Pi to 5V.
Several options are possible, and I have a suggested circuit on my blog post
that describes this project in more detail:

http://stationinthemetro.com/2016/02/27/tiki-nook-build-part-2-raspberry-pi-led-control

- Connect the RPi's MOSI output to the SDI (Serial Data Input) on the WS2801s
- Connect the RPi SCLK clock output to CKI (ClocK Input) on the WS2801
- The RPi's 5V pins will probably not be enough to power a string of
    any significant length. Use an external power supply of appropriate amperage
- Be sure to connect the RPi ground to the LED strip's ground


License:

Licensed under The MIT License (MIT). Please see LICENSE.txt for full text
of the license.


Version History:

- 1.0.1 - 2016-02-29 - Changed license from CC-BY-4.0 to MIT, due to 
                       recommendation by Creative Commons not to apply their 
                       licenses to software. See CC's FAQ for details:
                       https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software
- 1.0   - 2016-02-27 - Started development and complete rewrite, all in the 
                       same day!

"""


import RPi.GPIO as GPIO, time, os


# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.

#####
# 
# PaleoPixel - NeoPixel library port for WS2801 control over RPi hardware SPI
# 
#####

def Color(red, green, blue):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return ((red & 0xFF) << 16) | ((green & 0xFF) << 8) | (blue & 0xFF)

class PaleoPixel(object):
    def __init__(self, num):
        """Class to represent a WS2801 LED display.
        
        num - number of pixels in the display.
        """
        # Create an array for the LED data
        self._led_data = [0] * num

    def __del__(self):
        # Clean up memory used by the library when not needed anymore.
        if self._led_data is not None:
            self._led_data = None

    def begin(self):
        """Initialize _led_data to zeroes.
        Not necessary, since we do this in __init__, but handy.
        """
        for i in range(len(self._led_data)):
            self._led_data[i] = 0
        self.show()
        
    def show(self):
        """Update the display with the data from the LED buffer."""
        spidev = file("/dev/spidev0.0", "w")
        for i in range(len(self._led_data)):
            spidev.write(chr((self._led_data[i]>>16) & 0xFF))
            spidev.write(chr((self._led_data[i]>>8) & 0xFF))
            spidev.write(chr(self._led_data[i] & 0xFF))
        spidev.close()
        time.sleep(0.002)

    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        if (n >= len(self._led_data)):
            return
        self._led_data[n] = color

    def setPixelColorRGB(self, n, red, green, blue):
        """Set LED at position n to the provided red, green, and blue color.
        Each color component should be a value from 0 to 255 (where 0 is the
        lowest intensity and 255 is the highest intensity).
        """
        self.setPixelColor(n, Color(red, green, blue))

    def getPixels(self):
        """Return an object which allows access to the LED display data as if 
        it were a sequence of 24-bit RGB values.
        """
        return self._led_data

    def numPixels(self):
        """Return the number of pixels in the display."""
        return len(self._led_data)

    def getPixelColor(self, n):
        """Get the 24-bit RGB color value for the LED at position n."""
        return self._led_data[n]


        
#####
# 
# Test functions which animate LEDs in various ways.
# 
#####
         
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater marquee style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater marquee style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
     
     
       
#####      
#      
# Let's test it out!
#
#####

# Main program logic follows:
if __name__ == '__main__':
    # Create PaleoPixel object with appropriate number of LEDs.
    strip = PaleoPixel(LED_COUNT)
    # Reset the library (does not actually need to be called before
    # other functions, but we're testing here).
    strip.begin()

    print('Press Ctrl-C to quit.')
    while True:
        # Color wipe animations.
        colorWipe(strip, Color(255, 0, 0))  # Red wipe
        colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        colorWipe(strip, Color(0, 0, 255))  # Green wipe
        # Theater chase animations.
        theaterChase(strip, Color(127, 127, 127))  # White theater chase
        theaterChase(strip, Color(127,   0,   0))  # Red theater chase
        theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
        # Rainbow animations.
        rainbow(strip)
        rainbowCycle(strip)
        theaterChaseRainbow(strip)