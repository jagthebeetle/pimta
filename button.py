import logging
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def on_press(fn, debounce=None):
    try:
        while True:
            input_state = GPIO.input(18)
            if input_state == False:
                fn()
                if debounce:
                    time.sleep(debounce)
    except KeyboardInterrupt:
        logging.info('Caught keyboard interrupt; shutting down.')
    finally:
        GPIO.cleanup()
