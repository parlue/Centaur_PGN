# Play pure ct800 without DGT Centaur Adaptive Play
#
import gamemanager
import sys
import os
# sys.path.append('/home/pi/v2/board')
from display import epaper
import time
import chess
import chess.engine
import sys
import pathlib
from random import randint
import configparser
curturn = 1
computeronturn = 0
kill = 0

# Expect the first argument to be 'white' 'black' or 'random' for what the player is playing
computerarg = sys.argv[1]
if computerarg == "white":
	computeronturn = 0
if computerarg == "black":
	computeronturn = 1
if computerarg == "random":
	computeronturn = randint(0,1)

# Arg2 is going to contain the name of our engine choice. We use this for database logging and to spawn the engine
enginename = sys.argv[2]

ucioptionsdesc = "Default"
ucioptions = {}
if len(sys.argv) > 3:
	# This also has an options string...but what is actually passed in 3 is the desc which is the section name
	ucioptionsdesc = sys.argv[3]
	# These options we should derive form the uci file
	ucifile = "/home/pi/v2/engines/" + enginename + ".uci"
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read(ucifile)
	print(config.items(ucioptionsdesc))
	for item in config.items(ucioptionsdesc):
		ucioptions[item[0]] = item[1]
	print(ucioptions)

if computeronturn == 0:
	gamemanager.setGameInfo(ucioptionsdesc, "", "", "Player", enginename)
else:
	gamemanager.setGameInfo(ucioptionsdesc, "", "", enginename, "Player")

def keyCallback(key):
	# This function will receive any keys presses on the keys
	# under the display. Possibles:
	# gamemanager.BTNBACK  gamemanager.BTNTICK  gamemanager.BTNUP
	# gamemanager.BTNDOWN  gamemanager.BTNHELP  gamemanager.BTNPLAY
	global kill
	print("Key event received: " + str(key))
	if key == gamemanager.BTNBACK:
		kill = 1
	if key == gamemanager.BTNHELP:
		hallo = 0
		
def eventCallback(event):
	global curturn
	global engine
	global eloarg
	global kill
	global mv
	
	#cmove = 0
	# This function receives event callbacks about the game in play
	if event == gamemanager.EVENT_NEW_GAME:
		epaper.writeText(0,"New Game")
		epaper.writeText(1,"               ")
		epaper.writeText(13,"Play "+ enginename)
		curturn = 1
		epaper.drawFen(gamemanager.cboard.fen())
		print('fertig')
		return
	if event == gamemanager.EVENT_WHITE_TURN:
		print("here we are")
		curturn = 1
		epaper.writeText(0,"White turn")
		if curturn == computeronturn:
			os.chdir("/home/pi/v2/engines/")
			engine = chess.engine.SimpleEngine.popen_uci("/home/pi/v2/engines/" + enginename)
			if ucioptions != {}:
				options = (ucioptions)
				engine.configure(options)
			limit = chess.engine.Limit(time=5)
			mv = engine.play(gamemanager.cboard, limit, info=chess.engine.INFO_ALL)
			mv = mv.move
			epaper.writeText(12, "Engine: " + str(mv))
			engine.quit()
			gamemanager.computerMove(str(mv))
		return
	if event == gamemanager.EVENT_BLACK_TURN:
		curturn = 0
		epaper.writeText(0,"Black turn")
		if curturn == computeronturn:
			os.chdir("/home/pi/v2/engines/")
			engine = chess.engine.SimpleEngine.popen_uci("/home/pi/v2/engines/" + enginename)
			if ucioptions != {}:
				options = (ucioptions)
				print("preload")
				engine.configure(options)
				print("options load")
			limit = chess.engine.Limit(time=5)
			mv = engine.play(gamemanager.cboard, limit, info=chess.engine.INFO_ALL)
			mv = mv.move
			epaper.writeText(12,"Engine: " + str(mv))
			engine.quit()
			gamemanager.computerMove(str(mv))
		return	
	if event == gamemanager.EVENT_RESIGN_GAME:
		gamemanager.resignGame(computeronturn + 1)
		return
	if type(event) == str:
		# Termination.CHECKMATE
		# Termination.STALEMATE
		# Termination.INSUFFICIENT_MATERIAL
		# Termination.SEVENTYFIVE_MOVES
		# Termination.FIVEFOLD_REPETITION
		# Termination.FIFTY_MOVES
		# Termination.THREEFOLD_REPETITION
		# Termination.VARIANT_WIN
		# Termination.VARIANT_LOSS
		# Termination.VARIANT_DRAW
		if event.startswith("Termination."):
			epaper.writeText(1,event[12:])
			time.sleep(10)
			kill = 1

def moveCallback(move):
	# This function receives valid moves made on the board
	# Note: the board state is in python-chess object gamemanager.cboard
	epaper.drawFen(gamemanager.cboard.fen())
	epaper.writeText(9, move)


# Activate the epaper
epaper.initEpaper()

# Set the initial state of curturn to indicate white's turn
curturn = 1
if computeronturn == 0:
	epaper.writeText(9,"You are WHITE")
else:
	epaper.writeText(9,"You are BLACK")

# Subscribe to the game manager to activate the previous functions
gamemanager.subscribeGame(eventCallback, moveCallback, keyCallback)
epaper.writeText(0,"Place pieces in")
epaper.writeText(1,"Starting Pos")


while kill == 0:
	time.sleep(0.1)
