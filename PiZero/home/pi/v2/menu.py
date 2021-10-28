#!/usr/bin/python3
# Bootup menu

from board import boardfunctions , network
import os
import sys
import time
import centaurv2
from display import epd2in9d , epaper

sys.path.append("/home/pi/centaur/PIL")
from PIL import Image , ImageDraw , ImageFont
# import lichessV4

menuitem = 1
curmenu = None
selection = ""

def keyPressed(id):
	# This function receives key presses
	global menuitem
	global curmenu
	global selection
#	boardfunctions.beep(boardfunctions.SOUND_GENERAL)
	if id == boardfunctions.BTNDOWN:
		menuitem = menuitem + 1
	if id == boardfunctions.BTNUP:
		menuitem = menuitem - 1
	if id == boardfunctions.BTNTICK:
		if not curmenu:
			selection = "BTNTICK"
			print(selection)
			#event_key.set()
			return
		c = 1
		r = ""
		for k, v in curmenu.items():
			if (c == menuitem):
				selection = k
				menuitem = 1
				return
			c = c + 1
	if id == boardfunctions.BTNBACK:
		selection = "BACK"
		return
	if menuitem < 1:
		menuitem = 1
	if menuitem > len(curmenu):
		menuitem = len(curmenu)
	epaper.clearArea(0,0,17,295)
	draw = ImageDraw.Draw(epaper.epaperbuffer)
	draw.polygon([(2, (menuitem * 20) + 2), (2, (menuitem * 20) + 18),
				  (17, (menuitem * 20) + 10)], fill=0)
	draw.line((17, 0, 17, 295), fill=0, width=1)

quickselect = 0

def fieldActivity(id):
	# This function receives field activity. +fieldid for lift -fieldid for place down
	global quickselect
	global curmenu
	global selection
	if quickselect == 1 and (id < -23 and id > -32):
		boardfunctions.beep(boardfunctions.SOUND_GENERAL)
		menuitem = (id * -1) - 23
		c = 1
		r = ""
		for k, v in curmenu.items():
			if (c == menuitem):
				selection = k
				menuitem = 1
				return
			c = c + 1

# Power on sound
def doMenu(menu):
	# Draws a menu and waits for the response in the global variable 'selection'
	global menuitem
	global curmenu
	global selection
	global quickselect
	selection = ""
	curmenu = menu
	# Display the given menu
	epaper.clearScreen()
	menuitem = 1
	quickselect = 0
	boardfunctions.pauseEvents()
	res = boardfunctions.getBoardState()
	boardfunctions.unPauseEvents()
	if res[32] == 0 and res[33] == 0 and res[34] == 0 and res[35] == 0 and res[36]==0 and res[37] == 0 and res[38] == 0 and res[39] == 0:
		# If the 4th rank is empty then enable quick select mode. Then we can choose a menu option by placing and releasing a piece
		quickselect = 1
	row = 1
	for k, v in menu.items():
		epaper.writeText(row,"    " + str(v))
		row = row + 1
		epaper.clearArea(0,0,17,295)
		draw = ImageDraw.Draw(epaper.epaperbuffer)
		draw.polygon([(2, (menuitem * 20) + 2), (2, (menuitem * 20) + 18),
					  (17, (menuitem * 20) + 10)], fill=0)
		draw.line((17,0,17,295), fill=0, width=1)
	while selection == "":
		time.sleep(0.1)
	return selection

# Turn Leds off, beep, clear DGT Centaur Serial
# Initialise the epaper display - after which functions in epaper.py are available but you can also draw to the
# image epaper.epaperbuffer to change the screen.
boardfunctions.ledsOff()
boardfunctions.beep(boardfunctions.SOUND_POWER_ON)
boardfunctions.clearSerial()
epaper.initEpaper()
# Subscribe to board events. First parameter is the function for key presses. The second is the function for
# field activity
boardfunctions.subscribeEvents(keyPressed, fieldActivity)


while True:
	menu = {
		'Centaur': ' DGT Centaur',
		'Lichess': ' Lichess',
		'DGT': ' DGT Board',
		'Picochess': ' Picochess',
		'Connection': ' WiFi check',
		'lichessapi': ' Lichesskey',
		'lichessrating': ' Lichessrating',
		#'Update': 'Systemupdate',
		'Reboot': ' Reboot',
		'Shutdown': ' Shutdown'}
	result = doMenu(menu)
	
	if result == "Centaur":
		epaper.clearScreen()
        
		boardfunctions.writeText(1, "load game...")
		boardfunctions.pauseEvents()
		boardfunctions.clearScreen()
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centaur")
		#sys.exit()

	if result == "lichessapi":
		epaper.clearScreen()
		boardfunctions.pauseEvents()
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 lichessapi.py")
		boardfunctions.unPauseEvents()
		
	if result == "lichessrating":
		epaper.clearScreen()
		boardfunctions.pauseEvents()
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 lichessrating.py")
		boardfunctions.unPauseEvents()
		
		
	if result == "DGT":
		epaper.clearScreen()
		boardfunctions.pauseEvents()
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 dgte.py")
		boardfunctions.unPauseEvents()
	
	

	if result == "Connection":
		centaurv2.connectiontest()
		
	if result == "Shutdown":
		
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, "Please shutdown")
		boardfunctions.writeText(2, 'from the centaur')
		boardfunctions.writeText(3, 'aplication')
		boardfunctions.writeText(4, '...')
		boardfunctions.writeText(5, 'load centaur')
		time.sleep(2)
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centaur")
		
	
	if result == "Reboot":
		boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
		epaper.epd.init()
		epaper.epd.HalfClear()
		time.sleep(6)
		epaper.stopEpaper()
		time.sleep(2)
		boardfunctions.pauseEvents()
		os.system("/sbin/shutdown -r now &")
		sys.exit()
	
	
	if result == "Lichess":
		lichessmenu = {'Current': ' Current', 'New': ' New Game'}
		result = doMenu(lichessmenu)
		print(result)
		# Current game will launch the screen for the current
		if (result != "BACK"):
			if (result == "Current"):
				#boardfunctions.clearScreen()
				boardfunctions.pauseEvents()
				boardfunctions.clearScreen()
				os.chdir("/home/pi/v2")
				os.system("/usr/bin/python3.6 /home/pi/v2/lichessV4.py current")
				sys.exit()

			livemenu = {'Rated': ' Rated', 'Unrated': ' Unrated'}
			result = doMenu(livemenu)
			if result == "Rated":
				rated=True
			else:	
				rated=False
			colormenu = {'white': ' White', 'random': ' Random', 'black': ' Black'}
			result = doMenu(colormenu)
			color = result
			timemenu = {'10 , 5': ' 10+5 minutes' , '15 , 10': ' 15+10 minutes', '30': ' 30 minutes', '30 , 20': ' 30+20 minutes', '60 , 20': ' 60+20 minutes'}
			result = doMenu(timemenu)
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
			boardfunctions.pauseEvents()
			boardfunctions.clearScreen()
			os.chdir("/home/pi/v2")
			os.system(f"/usr/bin/python3.6 /home/pi/v2/lichessV4.py New {gtime} {gincrement} {rated} {color}")
			
			#sys.exit()