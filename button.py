import atexit
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

class Button(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def on_press(self, fn, debounce=250):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=fn, bouncetime=debounce)
