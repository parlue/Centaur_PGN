#!/usr/bin/python3.6 

import sys
import pathlib
import os
import boardfunctions
from pathlib import Path

# check if stick is available
usbstick = pathlib.Path("/dev/sda1")
updatefile = pathlib.Path("/media/update.tar")
boardfunctions.initScreen()
time.sleep(2)
boardfunctions.ledsOff()

def main():
	if usbstick.exists() :
		os.system('mount -t vfat /dev/sda1 /media')
		if updatefile.exists():
			boardfunctions.writeText(10, "Running systemupdate... plz wait")
			os.system('mkdir /media/tmp')
			os.system('tar xvf /media/update.tar /media/tmp/')
			os.system('/media/tmp/update.sh')
			os.system('rm -rf /media/tmp')
			os.system('rm /media/update.tar')
			os.system('umount /media')
			time.sleep(1)
			boardfunctions.writeText(10, "done")
			time.sleep(2)
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
