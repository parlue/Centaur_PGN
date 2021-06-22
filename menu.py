# Bootup menu

import boardfunctions
import os
import sys
import time

# Power on sound
boardfunctions.beep(boardfunctions.SOUND_POWER_ON)
boardfunctions.clearSerial()
boardfunctions.initScreen()
time.sleep(2)
boardfunctions.ledsOff()

while True:
    menu = {
		'Centaur': 'DGT Centaur',
		'PGN2USB': 'Export PGN to USB'
		'PGN2Mail': 'Export PGN via Mail'
	    	'ANLG2Mail': 'Export analysed PGN via Mail'
        	'Lichess': 'Lichess',
		'LichessAPI': 'Import Key',
        	'DGTBoard': 'DGT Boardclone',
		'Update': 'Update dso stack',
		'Connecttest': 'Tethering test', 
        'Shutdown': 'Shutdown',
        'Reboot': 'Reboot'}
    boardfunctions.initialised = 0
    result = boardfunctions.doMenu(menu)
    if result == "Centaur":
        boardfunctions.clearScreen()
        os.chdir("/home/pi/centaur")
        os.system("/home/pi/centaur/centaur")
        sys.exit()
	if result == "PGN2USB":
        boardfunctions.clearScreen()
        os.chdir("/mnt/")
        os.system("./chessgame.py")
        sys.exit()
	if result == "PGN2mail":
        boardfunctions.clearScreen()
        os.chdir("/mnt/")
        os.system("./chessgamemail.py")
        sys.exit()
	if result == "ANLG2Mail":
        boardfunctions.clearScreen()
        os.chdir("/mnt/")
        os.system("./chessgamemail.py")
        sys.exit()
	if result == "DGT":
        boardfunctions.clearScreen()
        os.chdir("/home/pi/dgt/")
        os.system("./dgtbord.py")
        sys.exit()
	if result == "LichessAPI":
        boardfunctions.clearScreen()
        os.chdir("/mnt/")
        os.system("./config.py")
        sys.exit()
	if result == "Update":
        boardfunctions.clearScreen()
        os.chdir("/mnt/")
        os.system("./update.py")
        sys.exit()
		
    if result == "Shutdown":
        boardfunctions.clearScreen()
        boardfunctions.sleepScreen()
        boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
        os.system("/sbin/shutdown now")
        sys.exit()
    if result == "Reboot":
        boardfunctions.clearScreen()
        boardfunctions.sleepScreen()
        boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
        os.system("/sbin/shutdown -r now")
        sys.exit()
    if result == "BACK":
        boardfunctions.clearScreen()
        boardfunctions.sleepScreen()
        boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
        os.system("/sbin/shutdown now")
        sys.exit()

    if result == "Lichess":
        lichessmenu = {'Current': 'Current', 'New': 'New Game'}
        result = boardfunctions.doMenu(lichessmenu)
        print(result)
        # Current game will launch the screen for the current
        if (result != "BACK"):
            if (result == "Current"):
                boardfunctions.clearScreen()
                os.chdir("/home/pi/centaur/py")
                os.system("/bin/python3 /home/pi/centaur/py/lichess.py current")
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
