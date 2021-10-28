# Add lichess rating
#

from board import boardfunctions
import os
import time
import sys
#import re

boardfunctions.initScreen()
time.sleep(2)


range = boardfunctions.getText("Range XXXX-XXXX")

if range == "":
	sys.exit()

if len(range) > 6 and range.find("-")>=3:
	print(len(range))
	print(range.find("-"))
	
	range = range.strip()	
	range = "rating_range=\""+range+"\"" 
	conf = open('/home/pi/v2/ratingconf.py','w')
	conf.write(range)
else :
	range = "rating_range=None"
	conf = open('/home/pi/v2/ratingconf.py','w')
	conf.write(range)
	
conf.close()

