#import some stuff
import picamera
from time import sleep
from PIL import Image
import pygame
import random
import os.path
import cups
import datetime
import RPi.GPIO as GPIO
import pytumblr
import threading


#Set some global variables
PICFOLDERNAME='PhotoboothPics/'
PIXWIDTH=1024
PIXHEIGHT=768
BIGFONTSIZE=200
LILFONTSIZE=80
PRINTERSHEETSREMAININGCOUNT=input("How many sheets of paper are left in the printer?")
YELLOWBUTTON = 5
GREENBUTTON = 16
LIGHT = 21
EXITAPP = False
GETREADYDELAY=3
DELAYFORPRINT=30
COUNTTIMEDELAY=1 
DELAYBETWEENSHOTS=3 
YESPRINT=1
YESPOST=1

#Method to display text
def displayText(text='asdf', fontsize=1, Yoffset=10, resetScreen=1):
    font = pygame.font.Font('freesansbold.ttf', fontsize)
    if resetScreen:
        screen.fill(black)
    width, height = font.size(text)
    xoffset = (w-width) // 2
    #yoffset = (h-height) // 2
    coords = xoffset, Yoffset
    font_surf = font.render(text, True, textcol)
        
    screen.blit(font_surf, coords)
    pygame.display.update()


# INIT DISPLAY
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
black = pygame.Color(0, 0, 0)
textcol = pygame.Color(255, 255, 255)
w, h = screen.get_size()
screen.fill(black)

# INIT CAMERA
camera = picamera.PiCamera()
camera.vflip = False
camera.hflip = False
camera.preview_fullscreen = False
camera.preview_window = ((w-PIXWIDTH)//2,300,PIXWIDTH,PIXHEIGHT)
camera.resolution = (PIXWIDTH, PIXHEIGHT)
camera.awb_mode = 'shade'
camera.contrast = -10



camera.start_preview()

sleep(1000)