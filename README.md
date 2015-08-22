# RGBLedDaemon
A tiny simple daemon for controlling a single RGB Led for Raspberry Pi written in Python.

While this daemon requires being sudo to start it, it doesn't require being sudo to change color and blink state of the LED in the GPIO.


Usage
-----

For starting the daemon, type:

    sudo python rgbled.py start

You can change color by typing the color:

    python rgbled.py color blue

You can turn blinking on by typing:

    python rgbled.py blink on

For stopping the daemon, type:

    sudo python rgbled.py stop


Schematic
---------

This code uses GPIOs 5, 6 and 13, which are the pins 29, 31 and 33 in the Raspberry Pi 2 Board. Pin 6 is the GND on the same board, and I'm using it.


![RGB Led pinout](https://github.com/ericoporto/RGBLedDaemon/raw/master/images/rgbled_raspi_small.png "Raspberry Pi with RGB Led pinout")


![Real Board](https://github.com/ericoporto/RGBLedDaemon/raw/master/images/real_board.jpg "Raspberry Pi with RGB Led mounted")


My pin selection comes from the example right here: https://www.hackster.io/windowsiot/rgb-led-sample . Your RGB Led may be different.


Dependencies
------------

This code uses Sander's Python Daemon from here: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ .
