#!/usr/bin/python3.6 

# This file is part of the Centaur V2 Mod open source software
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
# Add lichess Key
#
import sys
sys.path.append('/home/pi/v2')
from board import boardfunctions
import os
import time

#import re

boardfunctions.initScreen()
time.sleep(4)


lichesskey = boardfunctions.getText("lichess key")

if lichesskey == "":
	sys.exit()
key = "lichesstoken = \"" + lichesskey +"\""

conf = open('/home/pi/v2/v2conf.py','w')
conf.write(key)
conf.close()

