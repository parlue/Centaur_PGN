# Bootup menu

import boardfunctions
import os
import sys
import time
import centaurv2
# import lichessV4

# Power on sound
boardfunctions.beep(boardfunctions.SOUND_POWER_ON)
boardfunctions.clearSerial()
boardfunctions.initScreen()
#time.sleep(1)
boardfunctions.ledsOff()
os.chdir("/home/pi/v2/")

while True:
	menu = {
		'Centaur': 'DGT Centaur',
		'Lichess': 'Lichess',
		'DGT': 'DGT Board',
		'shell': 'Go bash',
		'Configuration': 'Import conf',
		'Update': 'Systemupdate',
		'Shutdown': 'Shutdown',
		'Reboot': 'Reboot'}
	boardfunctions.initialised = 0
	result = boardfunctions.doMenu(menu)
	
	if result == "Centaur":
		boardfunctions.clearScreen()
		boardfunctions.writeText(1, "load game...")
		os.chdir("/home/pi/centaur")
		os.system("/home/pi/centaur/centaur")
		#sys.exit()
	if result == "PGN2USB":
		centaurv2.chessgame()
		sys.exit()
	if result == "Configuration":
		centaurv2.getconfig()
#		os.chdir("/home/pi/v2/")
#		os.system("/usr/bin/python3.6 ./getconfig.py")
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
		centaurv2.update()
#		os.chdir("/home/pi/v2")
#		os.system("/usr#/bin/python3.6 ./update.py")
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
				os.system("/usr/bin/python3.6 /home/pi/v2/lichessV4.py current")
				#lichessV4(current)
				sys.exit()

			livemenu = {'Rated': 'Rated', 'Unrated': 'Unrated'}
			result = boardfunctions.doMenu(livemenu)
			print(result)
			if result == "Rated":
				rated=True
			else:	
				rated=False
			

			colormenu = {'White': 'White', 'Random': 'Random', 'Black': 'Black'}
			result = boardfunctions.doMenu(colormenu)
			print(result)
			color = result

			timemenu = {'10 , 5': '10+5 Minutes' , '15 , 10': '15+10 Minutes', '30': '30 Minutes', '30 , 20': '30+20 Minutes'}
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
		
			print(gtime + ',' + gincrement)
			os.chdir("/home/pi/v2")
			os.system("/usr/bin/python3.6 /home/pi/v2/lichessV4.py New gtime gincrement rated color")
			#lichessV4(New, gtime, gincrement, rated, color)
			sys.exit()