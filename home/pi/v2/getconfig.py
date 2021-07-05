#!/usr/bin/python3.6 

import sys
import pathlib
import os
import boardfunctions
from pathlib import Path

# check if stick is available
usbstick = pathlib.Path("/dev/sda1")
updatefile = pathlib.Path("/media/v2conf.py")
boardfunctions.initScreen()
time.sleep(2)
boardfunctions.ledsOff()

def main():
	if usbstick.exists() :
		os.system('mount -t vfat /dev/sda1 /media')
		if updatefile.exists():
			boardfunctions.writeText(10, "looking for config... plz wait")
			os.system('mount -o remount,rw /')
			os.system('cp /media/v2conf.py /home/pi/v2/')
			os.system('sync')
			os.system('mount -o remount,r /')
			time.sleep(1)
			boardfunctions.writeText(10, "done")
			time.sleep(2)
			os.system('unount /media')
			boardfunctions.clearScreen()
			boardfunctions.sleepScreen()
			boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
			os.system("/sbin/shutdown -r now")
			sys.exit()
		
		else :
			boardfunctions.writeText(10, "no update available")
			time.sleep(2)
		
	else :
		boardfunctions.writeText(10, "No USB-Stick available")
		time.sleep(2)

if __name__ == "__main__":
	main()
