# RGBLedDaemon
A tiny daemon for controlling a single RGB Led for Raspberry Pi written in Python.

While this daemon requires being sudo to start it, it doesn't require being sudo
 to change color and blink state of the LED in the GPIO.


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

This code uses GPIOs 5, 6 and 13, which are the pins 29, 31 and 33 in the Raspberry
Pi 2 Board. Pin 6 is the GND on the same board, and I'm using it.


![RGB Led pinout](https://github.com/ericoporto/RGBLedDaemon/raw/master/images/rgbled_raspi_small.png "Raspberry Pi with RGB Led pinout")


![Real Board](https://github.com/ericoporto/RGBLedDaemon/raw/master/images/real_board.jpg "Raspberry Pi with RGB Led mounted")


My pin selection comes from the example right here: https://www.hackster.io/windowsiot/rgb-led-sample .
Your RGB Led may be different.


Warnings
--------

Right now every time you call the script is called using `color` or `blink`, it
uses writing on `/tmp/` to communicate with the daemon.
So I recommend mounting `/tmp/` on RAM. To do this, is simple, first, edit the
raspberry pi fstab. If you are away, just connect in it using ssh.

To edit the fstab use `sudo nano fstab` . Once you are connected, add the following
line:

    tmpfs    /tmp    tmpfs    defaults,noatime,nosuid,size=100m    0 0

Than, just reboot with `sudo reboot`.

If you want to check if you have already done it before, just use `mount` or `df -h`.

I would like to point the following article as source: http://www.zdnet.com/article/raspberry-pi-extending-the-life-of-the-sd-card/ and also thank to dAnjou.

To avoid this, I'm planning to change this communication, but don't know how to
right now.



Dependencies
------------

This code uses Sander's Python Daemon from here: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ .
