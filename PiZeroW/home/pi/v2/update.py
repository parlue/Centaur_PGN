#!/usr/bin/python3.6 

# This file is part of the Centaur V" Mod open source software
# ( https://github.com/dsommerfeld/DGTCentaur-2.0-by-dso )
#
# DGTCentaur Mods is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# DGTCentaur Mods is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see
#
# https://github.com/dsommerfeld/DGTCentaur-2.0-by-dso/blob/master/LICENSE.md
#
# This and any other notices must remain intact and unaltered in any
# distribution, modification, variant, or derivative of this software.
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
