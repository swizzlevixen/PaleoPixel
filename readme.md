# PaleoPixel

Adafruit NeoPixel library port to control the older WS2801 pixels from Raspberry Pi hardware SPI. Includes Adafruit “strandtest”-style functions and performs a self-test if run as main.


## Provenance

Author: Mark Boszko

Raspberry Pi SPI driver code for WS2801 pixels based on Adafruit_LEDpixels.py  
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

Python port of NeoPixel library based on the rpi_ws281x library port, by Tony DiCola and Jeremy Garff  
https://github.com/jgarff/rpi_ws281x


## Usage

You'll need to translate 3.3V SPI logic levels from the Raspberry Pi to 5V. Several options are possible, and I have a suggested circuit on my blog post that describes this project in more detail:

http://stationinthemetro.com/2016/02/27/tiki-nook-build-part-2-raspberry-pi-led-control

- Connect the RPi's MOSI output to the SDI (Serial Data Input) on the WS2801s
- Connect the RPi SCLK clock output to CKI (ClocK Input) on the WS2801
- The RPi's 5V pins will probably not be enough to power a string of any significant length. Use an external power supply of appropriate amperage
- Be sure to connect the RPi ground to the LED strip's ground


## Version History:

- **1.0** - 2016-02-27 - Started development and complete rewrite, all in the same day!