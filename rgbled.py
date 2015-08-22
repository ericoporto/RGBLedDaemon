#!/usr/bin/env python
# TESTED WITH RASPBERRY PI 2 ONLY
import RPi.GPIO as GPIO
import sys, time
from daemon import Daemon
 
class RGBLedDaemon(Daemon):
  def __init__(self, *args, **kwargs):
    self.cf = '/tmp/rgbled-daemon.color'
    self.bf = '/tmp/rgbled-daemon.blink'
        
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    rpin = 5
    gpin = 6
    bpin = 13

    #PWM frequency in Hz
    freq = 100

    #Color blue
    GPIO.setup(rpin,GPIO.OUT)
    #Color green
    GPIO.setup(gpin,GPIO.OUT)
    # color red
    GPIO.setup(bpin,GPIO.OUT)
    #normal
    self.color = [255, 0, 0]
    self.rled = GPIO.PWM(rpin,freq)
    self.gled = GPIO.PWM(gpin,freq)
    self.bled = GPIO.PWM(bpin,freq)

    Daemon.__init__(self, *args, **kwargs)

  def run(self):
    with open(self.cf, 'w') as f:
      f.write("128\n128\n128\n")  

    with open(self.bf, 'w') as f:
      f.write("0")    

    self.rled.start(50)
    self.gled.start(50)
    self.bled.start(50)

    while True:
      self.color = [int(line) for line in open(self.cf, 'r')]
      self.blink = [int(line) for line in open(self.bf, 'r')]

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
    self.rled.ChangeDutyCycle(0)
    self.gled.ChangeDutyCycle(0)
    self.bled.ChangeDutyCycle(50)
    time.sleep(1)
    self.rled.stop()
    self.gled.stop()
    self.bled.stop()
    GPIO.cleanup()

    Daemon.stop(self, *args, **kwargs)

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
    else:
      print "Unknown command"
      sys.exit(2)
      sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)
