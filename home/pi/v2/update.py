#!/usr/bin/python3.6 

import sys
import pathlib
import os
import boardfunctions
from pathlib import Path

# check if stick is available
usbstick = pathlib.Path("/dev/sda1")
updatefile = pathlib.Path("/media/update.tar")
boardfunctions.clearSerial()
boardfunctions.initScreen()
boardfunctions.writeText(1, "check stick")

def main():
	if usbstick.exists() :
		os.system('mount -t vfat /dev/sda1 /media')
		boardfunctions.writeText(2, "stick found")
		boardfunctions.writeText(3, "check update")
		if updatefile.exists():
			boardfunctions.writeText(4, "update found")
			boardfunctions.writeText(5, "process update")
			os.system('mkdir /media/tmp')
			os.system('tar xvf /media/update.tar /media/tmp/')
			os.system('/media/tmp/update.sh')
			os.system('rm -rf /media/tmp')
			os.system('rm /media/update.tar')
			os.system('umount /media')
			boardfunctions.writeText(6, "done")
			boardfunctions.writeText(7, "reboot now")
			time.sleep(1)
			boardfunctions.clearScreen()
			boardfunctions.sleepScreen()
			boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
			os.system("/sbin/reboot")
			sys.exit()
		
		else :
			boardfunctions.writeText(4, "update missed")
			time.sleep(2)
		
	else :
		boardfunctions.writeText(2, "no stick found")
		time.sleep(2)

if __name__ == "__main__":
	main()
