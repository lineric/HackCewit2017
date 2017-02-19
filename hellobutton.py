# Start with the usual...  
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BOARD)  
  
# PUD_UP because GND
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

# One Example 
def my_callback(channel):  
  print "Hello World!"

GPIO.add_event_detect(7, GPIO.FALLING, callback=my_callback)

while True: # Loop forever
  True
  
GPIO.cleanup() # clean up GPIO on normal exit 
