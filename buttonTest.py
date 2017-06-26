import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUTTON = 5

GPIO.setup(BUTTON, GPIO.IN, GPIO.PUD_UP)

def printFunction(channel):
    print("button pressed!")


while True:
    GPIO.wait_for_edge(BUTTON, GPIO.RISING)
    print("Button Pressed, taking picture")
    sleep(0.5)
    continue

GPIO.cleanup()
