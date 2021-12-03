#!/usr/bin/python3
# Bootup menu

from board import boardfunctions , network
import os
import sys
import time
import centaurv2
from display import epd2in9d , epaper
import psutil
sys.path.append("/home/pi/centaur/PIL")
from PIL import Image , ImageDraw , ImageFont
import configparser
import v2conf

#change dso do not accept figure moves outsite startpos
global smess
menuitem = 1
curmenu = None
selection = ""
#lkey = v2conf.lichesstoken
#lrating = v2conf.ratingrange
#cclock = v2conf.chessoclock
scpu = psutil.cpu_count()

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
#		os.execv(__file__, sys.argv)
		sys.executable, ['python2'] + sys.argv
		selection = "BACK"
		return
	if menuitem < 1:
		menuitem = 1
	if menuitem > len(curmenu):
		menuitem = len(curmenu)
	epaper.clearArea(0,0,16,295)
	draw = ImageDraw.Draw(epaper.epaperbuffer)
	draw.polygon([(2, (menuitem * 20) + 2), (2, (menuitem * 20) + 18),
				  (17, (menuitem * 20) + 10)], fill=0)
#	draw.line((17, 0, 17, 295), fill=0, width=1)

quickselect = 0

def fieldActivity(id):
	# This function receives field activity. +fieldid for lift -fieldid for place down
	global quickselect
	global curmenu
	global selection
	
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
	
#
#	if res[17] == 0 and res[18] == 0 and res[19] == 0 and res[20] == 0 and res[21] == 0 and res[22] == 0 and res[23] == 0 and res[24] == 0 and res[25]==0 and res[26]==0 and res[27]==0 and res[28]==0 and res[29]== 0 and res[30]== 0 and res[31]== 0 and res[32]== 0 and res[33]== 0 and res[34]== 0 and res[35]== 0 and res[36]== 0 and res[37]== 0 and res[38]== 0 and res[39]== 0 and res[40]== 0 and res[41]== 0 and res[42]== 0 and res[43]== 0 and res[44]== 0 and res[45]== 0 and res[46]== 0 and res[47]== 0:	
#	quickselect = 1
	row = 1
	for k, v in menu.items():
		epaper.writeText(row,"    " + str(v))
		row = row + 1
		epaper.clearArea(0,0,16,295)
		draw = ImageDraw.Draw(epaper.epaperbuffer)
		draw.polygon([(2, (menuitem * 20) + 2), (2, (menuitem * 20) + 18),
					  (17, (menuitem * 20) + 10)], fill=0)
		#draw.line((17,0,17,295), fill=0, width=1)
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
	if scpu == 4:
		menu = {
		'ENGINE': ' Play Engine',
		'MESS': ' Emulators',
		'Centaur': ' DGT Centaur',
		'Lichess': ' Lichess',
		'DGT': ' DGT Board',
		'BEAR': ' Bearlink',
		'SETUP': ' Setup',
		'Reboot': ' Reboot',
		'Shutdown': ' Shutdown'}
		
	else:
	
		menu = {
			'ENGINE': ' Play Engine',
			'Centaur': ' DGT Centaur',
			'Lichess': ' Lichess',
			'DGT': ' DGT Board',
			'BEAR': ' Bearlink',
			'SETUP': ' Setup',
			'Reboot': ' Reboot',
			'Shutdown': ' Shutdown'}
	print(menu)
	result = doMenu(menu)
	
	if result == "Centaur":
		epaper.clearScreen()
        
		boardfunctions.writeText(1, "load game...")
		boardfunctions.pauseEvents()
#		boardfunctions.clearScreen()
		time.sleep(4)
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centi.sh")
		
		#sys.exit()
	if result == "SETUP":
		time.sleep(1)
		setupmenu = {'CHESSCLOCK': ' Chessclock' , 'wifi': ' Wifi setup' , 'Connection': ' Wifi check' , 'lichessapi': ' Lichesskey', 'lichessrating': 'Lichessrating'}
		result = doMenu(setupmenu)
		if result == "lichessapi":
			epaper.clearScreen()
			boardfunctions.pauseEvents()
			os.chdir("/home/pi/v2/")
			os.system("/usr/bin/python3.6 lichessapi.py")
			boardfunctions.unPauseEvents()
		if result == "CHESSCLOCK":
			time.sleep(1)
			timemenu ={'none': ' No clock', '5 , 3': ' 5+3 minutes' , '10 , 5': ' 10+5 minutes' , '15 , 10': ' 15+10 minutes', '30': ' 30 minutes', '30 , 20': ' 30+20 minutes', '60': ' 60 minutes', '90': ' 90 minutes'}
			result = doMenu(timemenu)
			if result == 'none':
				w = "0"
				b = "0"
				i = "0"
			if result =='5 , 3':
				w = "5"
				b = "5"
				i = "3"
			if result =='10 , 5':
				w = "10"
				b = "10"
				i = "5"
			if result == '15 , 10':
				w = "15"
				b = "15"
				i = "10"
			if result == '30':
				w = "30"
				b = "30"
				i = "0"
			if result == '30 , 20':	
				w = "30"
				b = "30"
				i = "20"
			if result == "60":
				w = "60"
				b = "60"
				i = "0"
			if result == "90":
				w = "90"
				b = "90"
				i = "0"
			#w=str(w)
			#b=str(b)
			#i=str(i)
			conf = open('/home/pi/v2/chessclock.py','w')
			conf.write(f'chessoclock = [{w},{b},{i}]')
			conf.close()
			
			
		if result == "lichessrating":
			epaper.clearScreen()
			boardfunctions.pauseEvents()
			os.chdir("/home/pi/v2/")
			os.system("/usr/bin/python3.6 lichessrating.py")
			boardfunctions.unPauseEvents()
		if result == "wifi":
			time.sleep(1)
			wifimenu = {'wpa2': ' WPA2-PSK', 'wps': ' WPS Setup' }
			#' Recover wifi'}
			result = doMenu(wifimenu)
			if (result != "BACK"):
				if (result == 'wpa2'):
					boardfunctions.pauseEvents()
					os.chdir("/home/pi/v2/")
					os.system("/usr/bin/python3.6 wifi.py")
					boardfunctions.unPauseEvents()
				if (result == 'wps'):
					if network.check_network():
						selection = ""
						#from DGTCentaurMods.display import epd2in9d
						#epd = epd2in9d.EPD()
						#epd.init()
						# TODO: put here script to backup network.
						IP = network.check_network()
						epaper.clearScreen()
						epaper.writeText(0, ' Network is up.')
						epaper.writeText(1, ' Press OK to')
						epaper.writeText(2, ' disconnect')
						epaper.writeText(4, IP)
						timeout = time.time() + 15
						while selection == "" and time.time() < timeout:
							if selection == "BTNTICK":
								print("") # Placeholder
								# network.disconnect_all() not enable until Restore
								# function is finished
					else:
						wpsMenu = {'connect': 'Connect wifi'}
						result = doMenu(wpsMenu)
						if (result == 'connect'):
							epaper.clearScreen()
							epaper.writeText(0, 'Press WPS button')
							network.wps_connect()
							time.sleep(30)
				if (result == 'recover'):
					print() # placeholer
					# TODO: Build funtion in network.py to force restore wifi.
		if result == "Connection":
			centaurv2.connectiontest()
							
	
	if result == "DGT":
		epaper.clearScreen()
		boardfunctions.pauseEvents()
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 dgte.py")
		boardfunctions.unPauseEvents()
	if result == "BEAR":
		epaper.clearScreen()
		boardfunctions.pauseEvents()
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 bearlink.py")
		boardfunctions.unPauseEvents()

	if result == "Shutdown":
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, "Please shutdown")
		boardfunctions.writeText(2, 'from the centaur')
		boardfunctions.writeText(3, 'aplication')
		boardfunctions.writeText(4, '...')
		boardfunctions.writeText(5, 'load centaur')
		boardfunctions.pauseEvents()
		time.sleep(2)
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centi.sh")
		
	
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
	
	if result == "MESS":
		time.sleep(1)
		enginepath = str("/home/pi/v2/messengine/")
		enginemenu = {'Lang': ' R. Lang', 'Konig': ' J. Konig', 'Schroder': ' E. Schroeder', 'other': ' Ohter'}
		result = doMenu(enginemenu)
		time.sleep(1)
		if result == "Lang":
			engmenu ={'Amsterdam': ' Amsterdam', 'Dallas': ' Dallas', 'London': ' London', 'Roma': ' Roma'}
			result = doMenu(engmenu)
			time.sleep(1)
			if result == "Amsterdam":
				result="amsterd"
				time.sleep(1)
				enginefile = enginepath + "amsterd"
				ucifile = enginepath + "amsterd" + ".uci"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + "amsterd" + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			#
				
			if result == 'Dallas':
				time.sleep(1)
				result = "dallas16"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "dallas16"
				ucifile = enginepath + "dallas16" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == 'London':
				time.sleep(1)
				result = "lond32"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "lond32"
				ucifile = enginepath + "lond32" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == 'Roma':
				time.sleep(1)
				result = "roma32"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "roma32"
				ucifile = enginepath + "roma32" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
		
		if result == "Konig":
			time.sleep(1)
			engmenu={'Risc2500': ' Risc2500', 'Montreux': ' Montreux', 'Tascr30': ' Tascr30'}
			result = doMenu(engmenu)
			if result == 'Risc2500':
				time.sleep(1)
				result = 'risc2500'
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "risc2500"
				ucifile = enginepath + "risc2500" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == 'Montreux':
				time.sleep(1)
				result = "montreux"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "montreux"
				ucifile = enginepath + "montreux" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == 'Tascr30':
				time.sleep(1)
				result = "tascr30_king"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "tascr30_king"
				ucifile = enginepath + "tascr30_king" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
				
		if result == "Schroder":
			time.sleep(1)
			engmenu = {'MMIV': ' MMIV', 'MMV': ' MMV', 'Rebel': ' Rebel', 'Nshort': ' Nshort', 'Polgar': ' Polgar'}
			result = doMenu(engmenu)
			if result == "MMIV":
				time.sleep(1)
				result = "mm4"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "mm4"
				ucifile = enginepath + "mm4" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == "MMV":
				time.sleep(1)
				result = "mm5"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "mm5"
				ucifile = enginepath + "mm5" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == "Rebel":
				time.sleep(1)
				result = "rebel5"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "rebel5"
				ucifile = enginepath + "rebel5" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == "Nshort":
				time.sleep(1)
				result = "nshort"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "nshort"
				ucifile = enginepath + "nshort" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
			if result == "Polgar":
				time.sleep(1)
				result = "polgar"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "polgar"
				ucifile = enginepath + "polgar" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()
					time.sleep(2)
		if result == "other":
			time.sleep(1)
			engmenu = {'sensory': ' Sensory 9', 'prodigy': ' Prodigy', 'chess2001': ' CXG Chess','Supercon': ' Supercon'}
			result = doMenu(engmenu)
			if result == "Supercon":
				time.sleep(1)
				result = "supercon"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "supercon"
				ucifile = enginepath + "supercon" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()	
					time.sleep(2)
			if result == "sensory":
				time.sleep(1)
				result = "super9ccg"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "super9ccg"
				ucifile = enginepath + "super9ccg" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()	
					time.sleep(2)
			if result == "prodigy":
				time.sleep(1)
				result = "prodigy"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "prodigy"
				ucifile = enginepath + "prodigy" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()	
					time.sleep(2)
			if result == "chess2001":
				time.sleep(1)
				result = "ch2001"
				sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(sfmenu)
				time.sleep(1)
				enginefile = enginepath + "ch2001"
				ucifile = enginepath + "ch2001" + ".uci"
				if os.path.exists(ucifile):
					# Read the uci file and build a menu
					config = configparser.ConfigParser()
					config.read(ucifile)
					print(config.sections())
					smenu = {}
					for sect in config.sections():
						smenu[sect] = sect
					sec = doMenu(smenu)
					if sec != "BACK":
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
						boardfunctions.unPauseEvents()
						time.sleep(2)
				else:
					# With no uci file we just call the engine
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					print("/home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					os.system("/usr/bin/python3.6 /home/pi/v2/universalmessuci.py " + color + " \"" + result + "\"")
					boardfunctions.unPauseEvents()	
					time.sleep(2)
# // here check	
	if result == "ENGINE":
		time.sleep(1)
		enginemenu = {'stockfish': 'Stockfish'}
		# Pick up the engines from the engines folder and build the menu
		enginepath = str("/home/pi/v2/engines/")
		enginefiles = os.listdir(enginepath)
		for f in enginefiles:
			fn = str(f)
			if '.uci' not in fn:
				if '.bin' not in fn:
				# If this file is not .uci then assume it is an engine
					enginemenu[fn] = fn
		result = doMenu(enginemenu)
		print(result)
		if result == "stockfish":
			time.sleep(1)
			sfmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
			color = doMenu(sfmenu)
			print(color)
			# Current game will launch the screen for the current
			if (color != "BACK"):
				time.sleep(1)
				ratingmenu = {'2850': ' Pure', '1350': '  1350 ELO', '1500': ' 1500 ELO', '1700': ' 1700 ELO', '1800': ' 1800 ELO', '2000': ' 2000 ELO', '2200': ' 2200 ELO', '2400': ' 2400 ELO', '2600': ' 2600 ELO'}
				elo = doMenu(ratingmenu)
				if elo != "BACK":
					epaper.clearScreen()
					epaper.writeText(0, "Loading...")
					boardfunctions.pauseEvents()
					os.system("/usr/bin/python3.6 /home/pi/v2/stockfish.py " + color + " " + elo)
					boardfunctions.unPauseEvents()
		else:
			if result != "BACK":
				# There are two options here. Either a file exists in the engines folder as enginename.uci which will give us menu options, or one doesn't and we run it as default
				enginefile = enginepath + result
				ucifile = enginepath + result + ".uci"
				cmenu = {'white': ' White', 'black': ' Black', 'random': ' Random'}
				color = doMenu(cmenu)
				# Current game will launch the screen for the current
				if (color != "BACK"):
					if os.path.exists(ucifile):
						# Read the uci file and build a menu
						config = configparser.ConfigParser()
						config.read(ucifile)
						print(config.sections())
						smenu = {}
						for sect in config.sections():
							smenu[sect] = sect
						sec = doMenu(smenu)
						if sec != "BACK":
							epaper.clearScreen()
							epaper.writeText(0, "Loading...")
							boardfunctions.pauseEvents()
							print("/home/pi/v2/universaluci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
							os.system("/usr/bin/python3.6 /home/pi/v2/universaluci.py " + color + " \"" + result + "\"" + " \"" + sec+ "\"")
							boardfunctions.unPauseEvents()
					else:
						# With no uci file we just call the engine
						epaper.clearScreen()
						epaper.writeText(0, "Loading...")
						boardfunctions.pauseEvents()
						print("/home/pi/v2/universaluci.py " + color + " \"" + result + "\"")
						os.system("/usr/bin/python3.6 /home/pi/v2/universaluci.py " + color + " \"" + result + "\"")
						boardfunctions.unPauseEvents()
			#
	
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
				#boardfunctions.clearSerial()
				#time.sleep(2)
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
			#boardfunctions.clearSerial()
			#time.sleep(2)
			
			#sys.exit()