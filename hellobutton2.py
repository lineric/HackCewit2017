# -*- coding: utf-8 -*-
# Start with the usual...  
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BOARD)  
  
# PUD_UP because GND 
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Another Example
while True:
  try:
    GPIO.wait_for_edge(7, GPIO.FALLING) # Waiting
    print "Hello World!"
  except KeyboardInterrupt:  
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
GPIO.cleanup() # clean up GPIO on normal exit 
