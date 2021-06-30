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
		os.system('mkdir /media/tmp')
		os.system('tar xvf /media/update.tar /media/tmp/')
		os.system('/media/tmp/update.sh')
		os.system('rm -rf /media/tmp')
		os.system('umount /media')
		
	else :
		boardfunctions.writeText(10, "no update available")
		time.sleep(2)
		
else :
	boardfunctions.writeText(10, "No USB-Stick available")
	time.sleep(2)

if __name__ == "__main__":
	main()
