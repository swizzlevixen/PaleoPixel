# PaleoPixel

Adafruit NeoPixel library port to control the older WS2801 pixels from Raspberry Pi hardware SPI. Includes Adafruit “strandtest”-style functions and performs a self-test if run as main.


## Provenance

Author: Mark Boszko

Raspberry Pi SPI driver code for WS2801 pixels based on Adafruit_LEDpixels.py  
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

Python port of NeoPixel library based on the rpi_ws281x library port, by Tony DiCola and Jeremy Garff  
https://github.com/jgarff/rpi_ws281x


## Usage

I'm specifically using this with two of the [12mm Diffused Thin Digital RGB LED Pixels (Strand of 25) - WS2801](https://www.adafruit.com/products/322) from Adafruit, but it should work with any [WS2801](http://www.adafruit.com/datasheets/WS2801.pdf)-controlled LED strands.

You'll need to translate 3.3V SPI logic levels from the Raspberry Pi to 5V. Several options are possible, as laid out in [Adafruit's tutorial](https://learn.adafruit.com/neopixels-on-raspberry-pi/wiring). I also have a suggested circuit on my blog post that describes this project in more detail:

http://stationinthemetro.com/2016/02/27/tiki-nook-build-part-2-raspberry-pi-led-control

- Connect the RPi's MOSI output to the SDI (Serial Data Input) on the WS2801s
- Connect the RPi SCLK clock output to CKI (ClocK Input) on the WS2801
- The RPi's 5V pins will probably not be enough to power a string of any significant length. Use an external power supply of appropriate amperage
- Be sure to connect the RPi ground to the LED strip's ground

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">PaleoPixel</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/bobtiki/PaleoPixel" property="cc:attributionName" rel="cc:attributionURL">Mark Boszko</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code" rel="dct:source">https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code</a>.

## Version History:

- **1.0** - 2016-02-27 - Started development and complete rewrite, all in the same day!

