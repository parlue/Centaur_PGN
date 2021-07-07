# Bootup menu

import boardfunctions
import os
import sys
import time

# Power on sound
boardfunctions.beep(boardfunctions.SOUND_POWER_ON)
boardfunctions.clearSerial()
boardfunctions.initScreen()
#time.sleep(1)
boardfunctions.ledsOff()
boardfunctions.writeText(14, "Status: offline")

while True:
	menu = {
		'Centaur': 'DGT Centaur',
		'shell': 'Go bash',
		'PGN2USB': 'Export PGN',
		'Lichess': 'Lichess',
		'Configuration': 'Import conf',
		'Update': 'Systemupdate',
		'Connection': 'Tethering', 
		'Shutdown': 'Shutdown',
		'Reboot': 'Reboot'}
	boardfunctions.initialised = 0
	result = boardfunctions.doMenu(menu)
	boardfunctions.writeText(14, "Status: offline")
	if result == "Centaur":
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, "load game...")
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centaur")
		#sys.exit()
	if result == "PGN2USB":
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 ./chessgame.py")
		sys.exit()
	if result == "configuration":
		os.chdir("/home/pi/v2/")
		os.system("/usr/bin/python3.6 ./getconfig.py")
		sys.exit()
	if result == "shell":
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, "load shell")
		os.system("/bin/bash")
		sys.extit()
	#if result == "PGN2mail":
		#	os.chdir("/home/pi/v2")
		#	os.system("./pgn2mail.py")
		#	sys.exit()
	#if result == "ANLG2Mail":
		#os.chdir("/mnt/")
		#os.system("./chessgamemail.py")
		#sys.exit()
	#if result == "DGT":
		#os.chdir("/home/pi/v2/")
		#os.system("./dgtbord.py")
		#sys.exit()
	#if result == "FICS_User":
		#os.chdir("/mnt/")
		#os.system("./config.py")
		#sys.exit()
	#if result == "ICC_User":
		#os.chdir("/mnt/")
		#os.system("./config.py")
		#sys.exit()
	if result == "Update":
		os.chdir("/home/pi/v2")
		os.system("/usr/bin/python3.6 ./update.py")
		sys.exit()
	if result == "Connection":
		os.chdir("/home/pi/v2")
		os.system("/usr/bin/python3.6 ./connectiontest.py")
	if result == "Shutdown":
		boardfunctions.clearScreen()
		boardfunctions.sleepScreen()
		boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
		os.system("/sbin/poweroff")
		sys.exit()
	if result == "Reboot":
		boardfunctions.clearScreen()
		boardfunctions.sleepScreen()
		boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
		os.system("/sbin/reboot")
		sys.exit()
	if result == "BACK":
		boardfunctions.clearScreen()
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
				os.system("/usr/local/bin/python3.6 /home/pi/v2/lichess.py current")
				sys.exit()

				livemenu = {'Rated': 'Rated', 'Unrated': 'Unrated'}
				result = boardfunctions.doMenu(livemenu)
				print(result)

				colormenu = {'Random': 'Random', 'Black': 'Black', 'White': 'White'}
				result = boardfunctions.doMenu(colormenu)
				print(result)

				timemenu = {'15': '15 Minutes', '30': '30 Minutes', '60': '60 Minutes'}
				result = boardfunctions.doMenu(timemenu)
				print(result)