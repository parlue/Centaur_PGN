# Add lichess rating
#

import boardfunctions
import os
import time
import sys
#import re

boardfunctions.initScreen()
time.sleep(2)


lichesskey = boardfunctions.getTextnumbers("ratingrange")

if lichesskey == "":
	sys.exit()
key = "rating_rage =" + ratingrange 

conf = open('/home/pi/v2/rating.conf.py",'w')
conf.write(key)
conf.close()

