# Add lichess Key
#
import sys
sys.path.append('/home/pi/v2')
from board import boardfunctions
import os
import time

#import re

boardfunctions.initScreen()
time.sleep(3)


lichesskey = boardfunctions.getText("lichess key")

if lichesskey == "":
	sys.exit()
key = "lichesstoken = \"" + lichesskey +"\""

conf = open('/home/pi/v2/v2conf.py','w')
conf.write(key)
conf.close()

