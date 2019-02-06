#!/usr/bin/env python
#
# Doorbell-application to send notifications to user/groupchat with Telegram bot
# Notification contains a webcam image from an axis camera.
# To be run on raspberry pi or something with GPIO.
#
# Hacked together by fenrus.
# Feel free to use in any way you like.
#

from time import sleep
import telegram
from telegram.error import NetworkError, Unauthorized
import os
import urllib
import RPi.GPIO as GPIO
import datetime
import logging

# if needed, enable logging for telegram stuff by uncommenting below:
# logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configures the GPIO stuffs properly. Short GPIO-->GND for action.
# with below setting, no +3.3v or resistor is needed.
# i use GPIO 7.
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)


### Configuration variables

# Check the telegram api for info about chat_id.
# Number is something like "12312312"
recipient = 'CHANGEME'

# axis webcam settings, i use a 225 FD camera.
# default creds are root/admin.
cameraip = '10.1.1.2'
cameracreds = 'root:admin'

# path to save images.
imagepath = '/home/pi/doorbell/'

# the secret telegram bot key
# Secret is something like "123123123:BBFEDDLPqUgdp7fMZm8I4s32oB1uxy1YWXY"
bot = telegram.Bot('CHANGEME')


print 'Starting the doorbell script\r'

while True:

   if (GPIO.input(7) == False):
      t = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
      thr = datetime.datetime.now().strftime('%d/%m at %H:%M')
      print t, "Button pushed!\r"

      filename = 'capture_' + t + '.jpg'

      f = open(filename, 'wb')
      # URL to fetch .jpg still from axis camera Might differ from your camera.
      f.write(urllib.urlopen("http://"+ cameracreds +"@"+ cameraip + "/axis-cgi/jpg/image.cgi?resolution=640x480&dummy="+ t).read())
      f.close()
      print datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), 'image saved'
      bot.send_message(chat_id=recipient, text='Doorbell rang ' + thr)
      bot.send_photo(chat_id=recipient, photo=open(filename, 'rb'))
      print datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), 'image sent'

      # also, if you want to - you can also play a doorbell sound on your RPI.
      # os.system('mpg321 /home/pi/doorbell-1.mp3')
   sleep(0.2);
