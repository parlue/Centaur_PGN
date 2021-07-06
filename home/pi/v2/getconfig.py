#!/usr/bin/python3.6 

import sys
import pathlib
import os
import boardfunctions
from pathlib import Path

# check if stick is available
usbstick = pathlib.Path("/dev/sda1")
updatefile = pathlib.Path("/media/v2conf.py")
#boardfunctions.clearScreen()
time.sleep(1)
boardfunctions.ledsOff()
boardfunctions.writeText(1, "check Stick")

def main():
	if usbstick.exists() :
		os.system('mount -t vfat /dev/sda1 /media')
		boardfunctions.writeText(2, "stick found")
		boardfunctions.writeText(3, "check update")
		if updatefile.exists():
			boardfunctions.writeText(4, "config found")
			os.system('mount -o remount,rw /')
			boardfunctions.writeText(5, "import config")
			os.system('cp /media/v2conf.py /home/pi/v2/')
			os.system('sync')
			os.system('mount -o remount,r /')
			boardfunctions.writeText(6, "done")
			time.sleep(1)
			os.system('unount /media')
			boardfunctions.writeText(7, "reboot now")
			boardfunctions.clearScreen()
			boardfunctions.sleepScreen()
			boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
			os.system("/sbin/reboot")
			sys.exit()
		
		else :
			boardfunctions.writeText(4, "no config")
			time.sleep(2)
		
	else :
		boardfunctions.writeText(2, "No stick")
		time.sleep(2)

if __name__ == "__main__":
	main()
