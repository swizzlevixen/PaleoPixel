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

PaleoPixel.py is licensed for used under The MIT License (MIT). Please see LICENSE.txt for full text of the license.

Adafruit_LEDpixels.py is covered under their original license. Please see LICENSE.txt for full text of the license.

## Version History:

- **1.0.1** - 2016-02-29 - Changed license from CC-BY-4.0 to MIT, due to recommendation by Creative Commons not to apply their licenses to software. See [CC's FAQ](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software) for details.

- **1.0** - 2016-02-27 - Started development and complete rewrite, all in the same day!

