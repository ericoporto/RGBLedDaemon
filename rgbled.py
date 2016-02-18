#!/usr/bin/env python
# TESTED WITH RASPBERRY PI 2 ONLY
import RPi.GPIO as GPIO
import sys, time
from daemon import Daemon
import os.path

class RGBLedDaemon(Daemon):
  def __init__(self, *args, **kwargs):
    self.cf = '/tmp/rgbled-daemon.color'
    self.bf = '/tmp/rgbled-daemon.blink'

    self.rpin = 5
    self.gpin = 6
    self.bpin = 13

    #PWM frequency in Hz
    self.freq = 100

    self.color = [255, 0, 0]

    self.rled = []
    self.gled = []
    self.bled = []

    Daemon.__init__(self, *args, **kwargs)

  def run(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(self.rpin,GPIO.OUT)
    GPIO.setup(self.gpin,GPIO.OUT)
    GPIO.setup(self.bpin,GPIO.OUT)
    self.rled = GPIO.PWM(self.rpin,self.freq)
    self.gled = GPIO.PWM(self.gpin,self.freq)
    self.bled = GPIO.PWM(self.bpin,self.freq)

    self.rled.start(50)
    self.gled.start(50)
    self.bled.start(50)

    while True:
      if(os.path.isfile(self.cf) ):
        self.color = [int(line) for line in open(self.cf, 'r')]
      else:
        self.color = [128,128,128]

      if(os.path.isfile(self.bf) ):
        self.blink = [int(line) for line in open(self.bf, 'r')]
      else:
        self.blink = [0]

      self.rled.ChangeDutyCycle(100*self.color[0]/255)
      self.gled.ChangeDutyCycle(100*self.color[1]/255)
      self.bled.ChangeDutyCycle(100*self.color[2]/255)
      time.sleep(0.75)

      if(self.blink[0] == 1):
        self.rled.ChangeDutyCycle(0)
        self.gled.ChangeDutyCycle(0)
        self.bled.ChangeDutyCycle(0)

      time.sleep(0.75)



  def stop(self, *args, **kwargs):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(self.rpin,GPIO.OUT)
    GPIO.setup(self.gpin,GPIO.OUT)
    GPIO.setup(self.bpin,GPIO.OUT)
    self.rled = GPIO.PWM(self.rpin,self.freq)
    self.gled = GPIO.PWM(self.gpin,self.freq)
    self.bled = GPIO.PWM(self.bpin,self.freq)

    self.rled.ChangeDutyCycle(0)
    self.gled.ChangeDutyCycle(0)
    self.bled.ChangeDutyCycle(50)
    time.sleep(1)
    self.rled.stop()
    self.gled.stop()
    self.bled.stop()
    GPIO.cleanup()

    if os.path.exists(self.cf):
      os.remove(self.cf)

    if os.path.exists(self.bf):
      os.remove(self.bf)

    Daemon.stop(self, *args, **kwargs)

  def setcolor(self, r, g, b):
    newcolor=r+"\n"+g+"\n"+b
    colors= {'color': newcolor}
    with open(self.cf, 'w') as f:
      f.write(colors['color'])

  def changecolor(self, newcolor):
    colors = {'red':"255\n0\n0",
      'green': "0\n255\n0",
      'blue': "0\n0\n255",
      'white': "255\n255\n255",
      'yellow': "241\n196\n15",
      'orange': "230\n126\n34",
      'cyan': "52\n152\n219",
      'purple': "155\n89\n182",
      'turquoise': "26\n188\n156",
      'gray': "128\n128\n128",
      'black': "0\n0\n0" }

    if(newcolor in colors):
      with open(self.cf, 'w') as f:
        f.write(colors[newcolor])

  def changeblink(self, newvalue):
    values = {'on':"1",
      'off': "0"}

    if(newvalue in values):
      with open(self.bf, 'w') as f:
        f.write(values[newvalue])


if __name__ == "__main__":
  daemon = RGBLedDaemon('/tmp/rgbled-daemon.pid')
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    else:
      print "Unknown command"
      sys.exit(2)
      sys.exit(0)
  elif len(sys.argv) == 3:
    if 'color' == sys.argv[1]:
      daemon.changecolor(sys.argv[2])
    elif 'blink' == sys.argv[1]:
      daemon.changeblink(sys.argv[2])
  elif len(sys.argv) == 5:
    if 'set' == sys.argv[1]:
      daemon.setcolor(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
      print "Unknown command"
      sys.exit(2)
      sys.exit(0)
  else:
    print "usage: %s start|stop|restart|color [color]|blink [on|off]" % sys.argv[0]
    sys.exit(2)
