import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LIGHT = 21

GPIO.setup(LIGHT, GPIO.OUT)

while True:
    GPIO.output(LIGHT, True)
    sleep(0.5)
    GPIO.output(LIGHT, False)
    sleep(0.5)

GPIO.cleanup()
