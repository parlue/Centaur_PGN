# Bootup menu

import boardfunctions
import os
import sys
import time
import centaurv2
import epd2in9d
sys.path.append("/home/pi/centaur/PIL")
from PIL import Image
# import lichessV4

# Power on sound
epd = epd2in9d.EPD()
boardfunctions.beep(boardfunctions.SOUND_POWER_ON)
boardfunctions.clearSerial()
boardfunctions.initScreen()
time.sleep(1)
boardfunctions.ledsOff()
os.chdir("/home/pi/v2/")

while True:
	menu = {
		'Centaur': 'DGT Centaur',
		'Lichess': 'Lichess',
		'DGT': 'DGT Board',
		'BT': 'BT paring',
		'wifi': 'Wifi Setup',
		'Connection': 'WiFi check',
		#'Configuration': 'Import conf',
		#'Update': 'Systemupdate',
		'Reboot': 'Reboot',
		'Shutdown': 'Shutdown'}
#	boardfunctions.ledsOff()	
	boardfunctions.initialised = 0
	result = boardfunctions.doMenu(menu)
	
	if result == "Centaur":
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, "load game...")
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centaur")
		#sys.exit()

	if result == "DGT":
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 dgte.py")
	
	if result == "BT":
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 bt.py &")
	if result == "wifi":
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 wifi.py")	

	if result == "Connection":
		centaurv2.connectiontest()
		#os.chdir("/home/pi/v2")
		#os.system("/usr/bin/python3.6 ./connectiontest.py")
	if result == "Shutdown":
		#boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
		#boardfunctions.shutdown()
		
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, "Please shutdown")
		boardfunctions.writeText(2, 'from the centaur')
		boardfunctions.writeText(3, 'aplication')
		boardfunctions.writeText(4, '...')
		boardfunctions.writeText(5, 'load centaur')
		time.sleep(2)
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centaur")
		#image = Image.open('/home/pi/centaur/fonts/logo.bmp')
		#epd.DisplayPartial(epd.getbuffer(image))
		#time.sleep(3)
		#boardfunctions.sleepScreen()
		#boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
		#os.system("/sbin/poweroff")
		#sys.exit()
	if result == "Reboot":
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, 'reboot now')
		time.sleep(2)
		boardfunctions.sleepScreen()
		boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
		os.system("/sbin/reboot")
		sys.exit()
	
	if result == "Lichess":
		lichessmenu = {'Current': 'Current', 'New': 'New Game'}
		result = boardfunctions.doMenu(lichessmenu)
		print(result)
		# Current game will launch the screen for the current
		if (result != "BACK"):
			if (result == "Current"):
				boardfunctions.clearScreen()
				os.chdir("/home/pi/v2")
				os.system("/usr/bin/python3.6 /home/pi/v2/lichessV4.py current")
				sys.exit()

			livemenu = {'Rated': 'Rated', 'Unrated': 'Unrated'}
			result = boardfunctions.doMenu(livemenu)
			if result == "Rated":
				rated=True
			else:	
				rated=False
			colormenu = {'white': 'White', 'random': 'Random', 'black': 'Black'}
			result = boardfunctions.doMenu(colormenu)
			color = result
			timemenu = {'10 , 5': '10+5 minutes' , '15 , 10': '15+10 minutes', '30': '30 minutes', '30 , 20': '30+20 minutes', '60 , 20': '60+20 minutes'}
			result = boardfunctions.doMenu(timemenu)
			if result =='10 , 5':
				gtime = '10'
				gincrement = '5'
			if result == '15 , 10':
				gtime = '15'
				gincrement = '10'
			if result == '30':
				gtime = '30'
				gincrement = '0'
			if result == '30 , 20':	
				gtime = '30'
				gincrement = '20'
			if result == "60 , 20":
				gtime = '60'
				gincrement = '20'
		
			os.chdir("/home/pi/v2")
			os.system(f"/usr/bin/python3.6 /home/pi/v2/lichessV4.py New {gtime} {gincrement} {rated} {color}")
			
			#sys.exit()