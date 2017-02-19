import RPi.GPIO as GPIO
import time 

# To use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# Setup GPIO output channel
GPIO.setup(7, GPIO.OUT)

# Blink GPIO17 ad infinitum
while True:
  GPIO.output(7, GPIO.HIGH) # Off
  time.sleep(1)
  GPIO.output(7, GPIO.LOW) # On
  time.sleep(1)

GPIO.cleanup()
