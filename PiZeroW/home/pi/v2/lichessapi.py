# Add lichess Key
#

from board import boardfunctions
import os
import time
import sys
#import re

boardfunctions.initScreen()
time.sleep(2)


lichesskey = boardfunctions.getText("lichess key")

if lichesskey == "":
	sys.exit()
key = "lichesstoken = \"" + lichesskey +"\""

conf = open('/home/pi/v2/v2conf.py','w')
conf.write(key)
conf.close()

