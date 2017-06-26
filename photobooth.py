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

##########################
#THIS BLOCK SETS SHORTER LATE TIMES FOR DEBUGGING
#REMOVE FOR PRODUCTION!
#GETREADYDELAY=2
#DELAYFORPRINT=1
#COUNTTIMEDELAY=1 
#DELAYBETWEENSHOTS=1
#YESPRINT=0
#YESPOST=0
###########################

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

# INIT GPIO: BUTTON & LIGHT
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(YELLOWBUTTON, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(GREENBUTTON, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(LIGHT, GPIO.OUT)

#Method to flash the LED
def flashLed(e):
    while not EXITAPP:
        event_is_set = e.wait(2)
        if event_is_set:
            GPIO.output(LIGHT, True)
            sleep(0.5)
            GPIO.output(LIGHT, False)
            sleep(0.5)

# Authenticate with Tumblr via OAuth
client = pytumblr.TumblrRestClient(
  'gEimxWUm9Iexb18iieab5lRSp4Te0pu3r3SmPRmmHHzbqCZjuK',
  '4MOvfTSuZTJyUw0iA0e8nm2XkJQlEAiieY2RqU1eVMwsG8CkJC',
  'KlawXSusUrgdSaNJznJU1Ng2ho2PMFAsMdEhURpIoBy4YzrPGL',
  'Md7oV1P0YhAKSZSEcRF9ZWh3VkNRIJwfxJMJWxRpsv825JOX5M'
)
client.info()

# Setup a Tread that can handle blinking the light if needed
e = threading.Event()
t = threading.Thread(name='non-block', target=flashLed, args=(e, ))
t.start()

try:
    #BEGIN OUTER LOOP
    while True:

        if (PRINTERSHEETSREMAININGCOUNT < 2):
            e.set()

        displayText('Welcome to the Club Blue Victory Photobooth!', LILFONTSIZE)
        displayText('We\'ll take three pictures', LILFONTSIZE, 200, 0)
        displayText('press both buttons on top of this screen', LILFONTSIZE, 400, 0)
        displayText('(yellow then green) to get started', LILFONTSIZE, 600, 0)

        GPIO.wait_for_edge(YELLOWBUTTON, GPIO.RISING)
        GPIO.wait_for_edge(GREENBUTTON, GPIO.RISING)
        #Set some variables that we'll need in the inner loop
        i = datetime.datetime.now()
        HOUR = i.hour
        MINUTE = i.minute

        FILE_NAME_PREFIX = PICFOLDERNAME + "Photobooth_" + str(HOUR) + "_" + str(MINUTE) + "_"
    
        n=0

        #BEGIN INNER LOOP
        while n < 3:
            # Start up the display
            name=FILE_NAME_PREFIX+str(n)+".jpeg"
            n+=1
            camera.start_preview()
        
            #show an encouraging message
            if n==1:
                displayText('Here we go - get ready!', LILFONTSIZE)
            elif n==2:
                displayText('Two more to go!', LILFONTSIZE)
            else:
                displayText('Let\'s make this last one look great!', LILFONTSIZE)
        

            sleep(GETREADYDELAY)

            #OVERLAY Countdown
            displayText('3',BIGFONTSIZE)
            sleep(COUNTTIMEDELAY)

            displayText('2',BIGFONTSIZE)
            sleep(COUNTTIMEDELAY)

            displayText('1',BIGFONTSIZE)
            sleep(COUNTTIMEDELAY)

            #take the picture
            camera.capture(name, format='jpeg', resize=(PIXWIDTH,PIXHEIGHT))
            screen.fill(black)
            pygame.display.update()    
            camera.stop_preview()

            #READ IMAGE AND PUT ON SCREEN 
            img = pygame.image.load(name)
            displayText('Lookin\' Good!', LILFONTSIZE)
            screen.blit(img, ((w-PIXWIDTH)//2, 300))
            pygame.display.update()

            # WAIT A BIT
            sleep(DELAYBETWEENSHOTS)
            screen.fill(black)
            pygame.display.update()
        #END OF INNER LOOP

        displayText('Thanks for using the photobooth!', LILFONTSIZE)
        displayText('Your print should be ready soon.', LILFONTSIZE, 100, 0)
        displayText('We hope you enjoy the rest of the night!', LILFONTSIZE, 300, 0)

        #Now that we've captured the three images:
        #create a Python image library object from the image captured
        script_dir = os.path.dirname(os.path.abspath(__file__))
        im0 = Image.open(os.path.join(script_dir, FILE_NAME_PREFIX + '0.jpeg'))
        im1 = Image.open(os.path.join(script_dir, FILE_NAME_PREFIX + '1.jpeg'))
        im2 = Image.open(os.path.join(script_dir, FILE_NAME_PREFIX + '2.jpeg'))

        #Load the default template mine is a 1200 x 1800 pixel image otherwise you will have to change sizes below.
        bgimage = Image.open(os.path.join(script_dir, 'template.jpg'))
        # Thumbnail the images to make small images to paste onto the template
        im0.thumbnail((560,420))
        im1.thumbnail((560,420))
        im2.thumbnail((560,420))
        # Paste the images in order, 2 copies of the same image in my case, 2 columns (2 strips of images per 6x4)
        bgimage.paste(im0,(10,24))
        bgimage.paste(im1,(10,468))
        bgimage.paste(im2,(10,912))

        bgimage.paste(im0,(630,24))
        bgimage.paste(im1,(630,468))
        bgimage.paste(im2,(630,912))
        #Save the final image
        bgimage.save(os.path.join(script_dir,"Final_"+"test"+".jpg"))    

        #now print
        if YESPRINT:
            conn=cups.Connection()
            printers = conn.getPrinters()
            printer_name = printers.keys()[0]
            conn.printFile(printer_name,os.path.join(script_dir,"Final_"+"test"+".jpg"),"photobooth",{})
            PRINTERSHEETSREMAININGCOUNT = PRINTERSHEETSREMAININGCOUNT - 1


        #also post to Tumblr
        if YESPOST:
            client.create_photo('KristaAndChris', state="published", format="markdown", data=[os.path.join(script_dir, FILE_NAME_PREFIX + '0.jpeg'),os.path.join(script_dir, FILE_NAME_PREFIX + '1.jpeg'),os.path.join(script_dir, FILE_NAME_PREFIX + '2.jpeg')])

        sleep(DELAYFORPRINT)

        if (PRINTERSHEETSREMAININGCOUNT < 1):
            displayText('The printer is out of paper!',LILFONTSIZE)
            displayText('Please refill the printer before continuing', LILFONTSIZE, 200, 0)
            displayText('Ask Chris Jones for help', LILFONTSIZE, 400, 0)
            GPIO.wait_for_edge(GREENBUTTON, GPIO.RISING)

        
        e.clear()
    #END OF OUTER LOOP
except KeyboardInterrupt:
    print('i see that you hit ctrl + c. I''m working on shutting down gracefully!')
    EXITAPP = True
    # CLOSE CLEANLY AND EXIT
    sleep(2)
    pygame.quit()
    GPIO.cleanup()
    raise

