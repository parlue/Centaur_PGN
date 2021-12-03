# Play a uci engine
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
import v2conf
import chessclock
import threading
from random import randint
import configparser
#chessoclock = v2.conf.chessoclock
#if len(chessoclock)==0:
chessoclock=chessclock.chessoclock
whiteclock = chessoclock[0]
blackclock = chessoclock[1]
incr = chessoclock[2]
curturn = 1
computeronturn = 0
kill = 0
engineload=0
sgame = 0
sound = 1
newstart= 0

		
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
	ucifile = "/home/pi/v2/messengine/" + enginename + ".uci"
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

def eturn(s):
	global nturn
	nturn = s
def ddone(t):
	global edone
	edone = t
def rungame(u):
	global sgame
	sgame = u
def neustart(g):
	global newstart
	newstart = g
	
def EngineThread():

	global kill
	global cboard
	global eingemove
	global movedone
	global engine
	global limit
	global options
	movenow = 0
	movedone = 0
	os.chdir("/home/pi/v2/messengine/")
	engine = chess.engine.SimpleEngine.popen_uci(r"/home/pi/v2/messengine/" + enginename)
	if ucioptions != {}:
		options = (ucioptions)
		engine.configure(options)
	limit = chess.engine.Limit(time=86400)
	print ("engine loaded")

	while kill == 0:
		if sgame == 1 and newstart == 1:
			os.system('/usr/bin/killall -9 mess')
			os.chdir("/home/pi/v2/messengine/")
			engine = chess.engine.SimpleEngine.popen_uci(r"/home/pi/v2/messengine/" + enginename)
			time.sleep(1)
			if ucioptions != {}:
				options = (ucioptions)
				engine.configure(options)
			limit = chess.engine.Limit(time=86400)
			neustart(0)
		#newgame(0)
		time.sleep(0.5)	
	engine.quit()
startthread = threading.Thread(target=EngineThread, args=())
startthread.daemon = True
startthread.start()
time.sleep(3)	

def keyCallback(key):
	# This function will receive any keys presses on the keys
	# under the display. Possibles:
	# gamemanager.BTNBACK  gamemanager.BTNTICK  gamemanager.BTNUP
	# gamemanager.BTNDOWN  gamemanager.BTNHELP  gamemanager.BTNPLAY
	global kill
	global sound 
	print("Key event received: " + str(key))
	if key == gamemanager.BTNBACK:
		os.system("/usr/bin/killall -9 mess")
		os.system("/usr/bin/killall -9 {enginename}")
		kill = 1
# open submenu - todo
#	if key == gamemanager.BTNHELP:
#		if sound == 0:
#			sound == 1
#		if sound == 1:
#			sound = 0
#		hallo = 0
#start the clock
#	if key == gamemanager.BTNPLAY:
#		if gamemanager.cboard.fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
#			gamemanager.setchessclock(whiteclock,blackclock,incr)
#			gamemanager.startchessclock()
#			Hallo = 1
		
		
def eventCallback(event):
	global curturn
	global engine
	global eloarg
	global kill
	global mv
	global movenow

	#movedone = 0
	#cmove = 0

	if event == gamemanager.EVENT_NEW_GAME:
				
		epaper.writeText(0,"New Game")
		epaper.writeText(1,"               ")
		epaper.writeText(13, "              ")
		epaper.writeText(14,"Play "+ enginename)
		if whiteclock !=0 and blackclock != 0:
			gamemanager.setchessclock(whiteclock,blackclock,incr)
			gamemanager.startchessclock()
		curturn = 1
		epaper.drawFen(gamemanager.cboard.fen())
		if sgame == 1:
			neustart(1)
			time.sleep(3)
			
		print('fertig')
		return
	if event == gamemanager.EVENT_WHITE_TURN:
		rungame(1)
		print("here we are")
		curturn = 1
		epaper.writeText(0,"White turn")
		if curturn == computeronturn:
			mv = engine.play(gamemanager.cboard, limit, info=chess.engine.INFO_ALL) 
			print(mv)
			mv = mv.move
			eturn(0)
			#engine.quit()
			gamemanager.computerMove(str(mv))
			if gamemanager.cboard.is_check():
				board.beep(board.SOUND_GENERAL)
				time.sleep(0.3)
				board.beep(board.SOUND_GENERAL)
				epaper.writeText(13, '   CHECK!')
				if gamemanager.cboard.is_checkmate():
					paper.writeText(13, '    MATE!')
					board.beep(board.SOUND_WRONG)
					time.sleep(0.3)
					board.beep(board.SOUND_WRONG)
		return
	if event == gamemanager.EVENT_BLACK_TURN:
		rungame(1)
		curturn = 0
		epaper.writeText(0,"Black turn")
		if curturn == computeronturn:
			print("come on")
			mv = engine.play(gamemanager.cboard, limit, info=chess.engine.INFO_ALL)
			print(mv)
			mv = mv.move
			eturn(0)
			epaper.writeText(12,"Engine: " + str(mv))
			gamemanager.computerMove(str(mv))
			if gamemanager.cboard.is_check():
				board.beep(board.SOUND_GENERAL)
				time.sleep(0.3)
				board.beep(board.SOUND_GENERAL)
				epaper.writeText(13, '   CHECK!')
				if gamemanager.cboard.is_checkmate():
					paper.writeText(13, '    MATE!')
					board.beep(board.SOUND_WRONG)
					time.sleep(0.3)
					board.beep(board.SOUND_WRONG)
		
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


time.sleep(3)

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

os.system("/usr/bin/killall -9 mess")
