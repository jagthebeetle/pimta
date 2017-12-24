# pimta

Requirements are listed in `requirements.txt`, but might only make sense on Raspbian Jessie.
Code developed with python 2.7.

4 daisy-chained MAX7219s drive a 32x8 LED grid, connected via the Pi's SPI pins. A switch
connected to GPIO 18 is listened to for button presses.
