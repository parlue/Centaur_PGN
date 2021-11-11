# dso lichess  module based from Version 1 from EdNebeko
# Run a standalone game on lichess
# This is version four so we do it directly and with screen control!

# Castling - move king, wait for beep, move rook
# pawn promotion not yet implemented. Pick up pawn, put down queen

# python3 lichess.py [current|New]

# This is our lichess access token, the game id we're playing, fill it
# in in v2conf.py
#
# the chessclock only update after a move from any player. I won't struggle the display with permant
# updates. If you need livetime data, please follow the game on lichess via web.
# Button up, offer a draw
# Button down resign the game
# Button back will abort the game.... hard :-)
# Button ? will toggle the board in a sielence mode

# Please play exact and slowly


import sys
import berserk
import ssl
import time
import threading
from board import boardfunctions
import chess
import v2conf
import os
import ratingconf
#sys.path.append('/home/pi/v2/board')
from display import epaper

global ratingrange

token = v2conf.lichesstoken
ratingrange = ratingconf.rating_range


pid = -1
boardfunctions.clearSerial()
epaper.initEpaper()

if str(token) == "":
	epaper.writeText(1, "No lichesstoken")
	epaper.writeText(2, "try later")
	time.sleep(3)
	sys.exit()

if (len(sys.argv) == 1):
#	print("python3 lichess.py [current|New1]")
	sys.exit()

if (len(sys.argv) > 1):
	if (str(sys.argv[1]) != "current" and str(sys.argv[1]) != "New"):
		#print("python3 lichess.py [current|New2]")
		sys.exit()

session = berserk.TokenSession(token)
client = berserk.Client(session=session)

remotemoves = ""
#changed dso
status = ""
cboard = chess.Board()

# First start up the screen
# boardfunctions.initScreen()
if (sys.argv[1] == "current"):
	epaper.writeText(0, 'Joining Game')
else:
	epaper.writeText(0, 'New Game')
epaper.writeText(1, 'on Lichess')
#boardfunctions.writeText(2, 'LEDs Off')
boardfunctions.ledsOff()

# Get the current player's username
who = client.account.get()
player = str(who.get('username'))
epaper.writeText(2, 'Player:')
epaper.writeText(3, player)

# We'll use this thread to start a game. Probably not the best way to do it but
# let's make the thread pause 5 seconds when it starts up so that we can be
# sure that client.board.stream_incoming_events() has started well

running = True

	
def newGameThread():
	time.sleep(5)


#mod by dso 3.10.21
	gtime = str(sys.argv[2])
	ginc = str(sys.argv[3])
	grated = str(sys.argv[4])
	gcolor = str(sys.argv[5])



	epaper.writeText(5, f'time {gtime} , {ginc}')
	epaper.writeText(6, f'ratedt={grated}')
	epaper.writeText(7, f'color={gcolor}')
	epaper.writeText(8, f'ratingrange={ratingrange}')
	if (gtime=='10' and ginc=='5' and grated=="False" and gcolor=="white"):
		client.board.seek(10, 5, rated=False, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='10' and ginc=='5' and grated=="False" and gcolor=="black"):
		client.board.seek(10, 5, rated=False, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='10' and ginc=='5' and grated=="False" and gcolor=="random"):
		client.board.seek(10, 5, rated=False, variant='standard', color='random', rating_range=f'{ratingrange}')
	if (gtime=='10' and ginc=='5' and grated=="True" and gcolor=="white"):
		client.board.seek(10, 5, rated=True, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='10' and ginc=='5' and grated=="True" and gcolor=="black"):
		client.board.seek(10, 5, rated=True, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='10' and ginc=='5' and grated=="True" and gcolor=="random"):
		client.board.seek(10, 5, rated=True, variant='standard', color='random', rating_range=f'{ratingrange}')
	
	if (gtime=='15' and ginc=='10' and grated=="False" and gcolor=="white"):
		client.board.seek(15, 10, rated=False, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='15' and ginc=='10' and grated=="False" and gcolor=="black"):
		client.board.seek(15, 10, rated=False, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='15' and ginc=='10' and grated=="False" and gcolor=="random"):
		client.board.seek(15, 10, rated=False, variant='standard', color='random', rating_range=f'{ratingrange}')
	if (gtime=='15' and ginc=='10' and grated=="True" and gcolor=="white"):
			client.board.seek(15, 10, rated=True, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='15' and ginc=='10' and grated=="True" and gcolor=="white"):
		client.board.seek(15, 10, rated=True, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='15' and ginc=='10' and grated=="True" and gcolor=="random"):
		client.board.seek(15, 10, rated=True, variant='standard', color='random', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='0' and grated=="False" and gcolor=="white"):
		client.board.seek(30, 0, rated=False, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='0' and grated=="False" and gcolor=="black"):
		client.board.seek(30, 0, rated=False, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='0' and grated=="False" and gcolor=="random"):
		client.board.seek(30, 0, rated=False, variant='standard', color='random', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='0' and grated=="True" and gcolor=="white"):
		client.board.seek(30, 0, rated=True, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='0' and grated=="True" and gcolor=="black"):
		client.board.seek(30, 0, rated=True, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='0' and grated=="True" and gcolor=="random"):
		client.board.seek(30, 0, rated=True, variant='standard', color='random', rating_range=f'{ratingrange}')
	
	if (gtime=='30' and ginc=='20' and grated=="False" and gcolor=="white"):
		client.board.seek(30, 20, rated=False, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='20' and grated=="False" and gcolor=="black"):
		client.board.seek(30, 20, rated=False, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='20' and grated=="False" and gcolor=="random"):
		client.board.seek(30, 20, rated=False, variant='standard', color='random', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='20' and grated=="True" and gcolor=="white"):
		client.board.seek(30, 20, rated=True, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='20' and grated=="True" and gcolor=="black"):
		client.board.seek(30, 20, rated=True, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='30' and ginc=='20' and grated=="True" and gcolor=="random"):
		client.board.seek(30, 20, rated=True, variant='standard', color='random', rating_range=f'{ratingrange}')
	
	if (gtime=='60' and ginc=='20' and grated=="False" and gcolor=="white"):
		client.board.seek(60, 20, rated=False, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='60' and ginc=='20' and grated=="False" and gcolor=="black"):
		client.board.seek(60, 20, rated=False, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='60' and ginc=='20' and grated=="False" and gcolor=="random"):
		client.board.seek(60, 20, rated=False, variant='standard', color='random', rating_range=f'{ratingrange}')
	if (gtime=='60' and ginc=='20' and grated=="True" and gcolor=="white"):
		client.board.seek(60, 20, rated=True, variant='standard', color='white', rating_range=f'{ratingrange}')
	if (gtime=='60' and ginc=='20' and grated=="True" and gcolor=="black"):
		client.board.seek(60, 20, rated=True, variant='standard', color='black', rating_range=f'{ratingrange}')
	if (gtime=='60' and ginc=='20' and grated=="True" and gcolor=="random"):
		client.board.seek(60, 20, rated=True, variant='standard', color='random', rating_range=f'{ratingrange}')
	

# Wait for a game to start and get the game id!
gameid = ""
if (str(sys.argv[1]) == "New"):
	epaper.writeText(4, 'gamesearch')
	#print("Looking for a game")
	gt = threading.Thread(target=newGameThread, args=())
	gt.daemon = True
	gt.start()
while gameid == "":
	for event in client.board.stream_incoming_events():
		if ('type' in event.keys()):
			if (event.get('type') == "gameStart"):
				
				#print("is gameStart")
				if ('game' in event.keys()):
					#print(event)
					gameid = event.get('game').get('id')
					break

epaper.writeText(9, gameid)

playeriswhite = -1
whiteplayer = ""
blackplayer = ""

whiteclock = 0
blackclock = 0
whiteincrement = 0
blackincrement = 0
winner= ''
fenlog = "/home/pi/centaur/fen.log"
f = open(fenlog, "w")
f.write("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
f.close()

# Lichess doesn't start the clocks until white moves
starttime = -1

# This thread keeps track of the moves made on lichess
def stateThread():
	global remotemoves
	global status
	global playeriswhite
	global player
	global whiteplayer
	global blackplayer
	global whiteclock
	global blackclock
	global whiteincrement
	global blackincrement
	global resign
	global winner
	global cwinner
	global wtime
	global btime
	global whitetime
	global blacktime
	global whiterating
	global blackrating
	global message1
	global sound
	global wking
	global bking
	status =""
	while running and status != "mate" and status != "draw" and status != "resign" and status != "aborted" and status != "outoftime" and status != "timeout":
		buttonPress=0
		gamestate = client.board.stream_game_state(gameid)
		for state in gamestate:
			print(state)
			message1=str(state)
			#print(message1)
			if message1.find('moves'):
				c=message1.find("wtime")
				messagehelp = message1[c:len(message1)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				whitetimemin=messagehelp[1:c]
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				whitetimesec=messagehelp[1:c]
				if whitetimesec[:2]=="tz" or whitetimesec[1:3]=="st" :
					whitetimesec = "0"
				print (whitetimesec)
				whitetime = str(whitetimemin)+"min "+str(whitetimesec) +"sec"
				c=message1.find("btime")
				messagehelp = message1[c:len(message1)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				blacktimemin=messagehelp[1:c]
				messagehelp = messagehelp[c+1:len(messagehelp)]
				c = messagehelp.find(", ")
				blacktimesec=messagehelp[1:c]
				print(blacktimesec)
				if blacktimesec[:2]=="tz" or blacktimesec[1:3]=="st":
					blacktimesec = "0"
				blacktime = str(blacktimemin)+"min "+str(blacktimesec)+ "sec"
#mod by dso 4.1021
			if ('state' in state.keys()):
				remotemoves = state.get('state').get('moves')
				status = state.get('state').get('status')
			else:
				if ('moves' in state.keys()):
					remotemoves = state.get('moves')
				if ('status' in state.keys()):
					status = state.get('status')
			if status == "mate":
				winner = str(state.get('winner'))

			remotemoves = str(remotemoves)
			print("direkt aus dem fred "+remotemoves)
			status = str(status)
# dso add events and stop the game
			if ('text' in state.keys()):
				message = state.get('text')
				if message == "Takeback sent":
					client.board.post_message(gameid, 'Sorry , external boards can\'t handle takeback', spectator=False)
					
				if message == "Black offers draw":
					client.board.decline_draw(gameid)
				
				if message == "White offers draw":
					client.board.decline_draw(gameid)				

					
			if status == 'resign':
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				epaper.writeText(11, 'Resign')
				cwinner = str(state.get('winner'))
				epaper.writeText(12, cwinner +' wins')
				epaper.writeText(13,'pls wait restart..')
				time.sleep(15)
				os._exit(0)
				#running = False
			if status == 'aborted':
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				epaper.writeText(11, 'Game aborted')
				winner = 'No Winner'
				epaper.writeText(12, 'No winner')
				epaper.writeText(13,'pls wait restart..')
				time.sleep(15)
				os._exit(0)
				
			if status == 'outoftime':
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				epaper.writeText(11, 'Out of time')
				cwinner = str(state.get('winner'))
				epaper.writeText(12, cwinner +' wins')
				epaper.writeText(13,'pls wait restart..')
				time.sleep(15)
				os._exit(0)
			if status == 'timeout':
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				epaper.writeText(11, 'Out of time')
				cwinner = str(state.get('winner'))
				epaper.writeText(12, cwinner +' wins')
				epaper.writeText(13,'pls wait restart..')
				time.sleep(15)
				os._exit(0)
			if status == 'draw':
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				epaper.writeText(11, 'Draw')
				cwinner = str(state.get('winner'))
				epaper.writeText(12, cwinner +' No Winner')
				epaper.writeText(13,'pls wait restart..')
				time.sleep(15)
				os._exit(0)
				
						
			if (remotemoves == "None"):
				print("direkt aus dem fred 2 "+remotemoves)
				remotemoves = ""
			if ('black' in state.keys()):
				if ('name' in state.get('white')):
					print(str(state.get('white').get('name')) +
						  " vs " + str(state.get('black').get('name')))
					whiteplayer = str(state.get('white').get('name'))
					whiterating = str(state.get('white').get('rating'))
					blackplayer = str(state.get('black').get('name'))
					blackrating = str(state.get('black').get('rating'))
					
					if (str(state.get('white').get('name')) == player):
						playeriswhite = 1
					else:
						playeriswhite = 0
				

			time.sleep(0.2)
# dso start lichess message threat
st = threading.Thread(target=stateThread, args=())
st.daemon = True
st.start()
#print("Started")

boardfunctions.beep(boardfunctions.SOUND_GENERAL)
boardmoves = ""
lastboardmove = ""
beeped = 0
newgame=1
lastmove=""
while playeriswhite == -1:
	time.sleep(0.1)

if playeriswhite == 0:
	lastmove = "1234"
	remotemoves = "1234"

# ready for white
ourturn = 1


boardfunctions.clearBoardData()

oldremotemoves = ""
correcterror = -1
halfturn = 0
castled = ""
sound = "off"

epaper.clearScreen()
epaper.writeText(0,blackplayer + " " + blackrating)
epaper.writeText(9,whiteplayer + " " + whiterating)
fen = cboard.fen()
sfen = fen[0 : fen.index(" ")]
baseboard = chess.BaseBoard(sfen)
pieces = []
for x in range(0,64):
	pieces.append(str(chess.BaseBoard(sfen).piece_at(x)))
epaper.drawBoard(pieces)

client.board.post_message(gameid, 'I\'m playing with an external board, can\'t chat - I\'m not a bot, sry if it struggle, - have fun' , spectator=False)
resign = 1
bking = 0
wking = 0
while (status == "started") and ourturn != 0 :

	if ourturn == 1:
		if playeriswhite == 1:
			currentmover = 1
		else:
			currentmover = 0
	if ourturn == 0:
		if playeriswhite == 1:
			currentmover = 1
		else:
			currentmover = 0

	if ourturn == 1 and status == "started" and lastmove != '1234':
		# Wait for the player's move
		epaper.writeText(10,whitetime)
		epaper.writeText(1, blacktime)
		move = []
		while len(move) <=1 :
				move = boardfunctions.MywaitMove()
			boardfunctions.beep(boardfunctions.SOUND_GENERAL)
			if len(move) == 1:
				if move[0] == 200: #back
					os._exit()
			
				#if move[0] == 201: #tick
				if move[0] == 202: #UP
					client.board.offer_draw(gameid)
				if move[0] == 203: #down
					client.board.resign_game(gameid)
					
				if move[0] == 204: # help
					print("soundoption")
			time.sleep(0.2)
	
			
		if (len(move) == 2):
			fromsq = move[0] * -1
			mylastfrom = fromsq
			tosq = move[1]
			#boardfunctions.writeText(12, 'normal move')
		if (len(move) == 3):
			#boardfunctions.writeText(12, 'kick move')
			# This move should consist of two lifted and one place (two positives, 1 negative)
			# it is a piece take. So the negative that is not the inverse of the positive
			# is the piece that has moved and the positive is the tosq
				
#mod by dso 4.10.21
			tosq = -1

			tosq = move[2]

			fromsq = -1
			if move[0] != (tosq * -1): 
				fromsq = move[0] * -1
			if move[1] != (tosq * -1):
				fromsq = move[1] * -1
#dso field corection
		fromsq = fromsq -1
		tosq = tosq -1
		mylastfrom = fromsq
		# Convert to letter number square format
		fromln = boardfunctions.convertField(fromsq)
		#print(fromln)
		
		toln = boardfunctions.convertField(tosq)
		
		# If the piece is a pawn we should take care of promotion here. You could choose it from
		# the board screen. 	 But I'll do that later!
		# Send the move
		lastmove = fromln + toln
		

		try:
			
			mv = chess.Move.from_uci(lastmove)
			print("Checked")
			if (mv in cboard.legal_moves):
				
				#print("Castled")
				if lastmove == "e1g1" and wking == 0:
					castled = "h1f1"
				if lastmove == "e1c1" and wking == 0:
					castled = "a1d1"
				if lastmove == "e8g8" and bking == 0:
					castled = "h8f8"
				if lastmove == "e8c8" and bking == 0:
					castled = "a8d8"
				
							
				
# new dso 21.10.21 fix castled problem
				if castled =="h1f1" or castled == "a1d1" or castled == "h8f8" or castled == "a8d8" :
					print("move the rook")
					lrfromcalc = (ord(castled[:1]) - 97) + ((int(castled[1:2]) - 1) * 8)
					lrtocalc = (ord(castled[2:3]) - 97) + ((int(castled[3:4]) - 1) * 8)
					
					boardfunctions.clearBoardData()
					boardfunctions.ledFromTo(lrfromcalc, lrtocalc)
					while movedto != lrtocalc and status == "started":
						move = boardfunctions.MywaitMove()
						valid = 1
			# dso todo prüfen ob der zug richtig abgesetzt wurde
						#if move[0] == lrtocalc:
						#	valid = 1
						#	castled=""
						
						#if len(move) > 1:
						##	tomove = move[1] * -1
						#	if tomove == lrtocalc:
						#		print(lrtocalc)
						#		valid = 1
						castled=""
						
						if valid == 0:
							boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
						else:
							boardfunctions.beep(boardfunctions.SOUND_GENERAL)
						movedto = lrtocalc
					boardfunctions.ledsOff()
					boardfunctions.clearSerial()
				playertime=time.time()
				
				#check if lichess accept this move
				ret = client.board.make_move(gameid, fromln + toln)
				if ret :
					cboard.push(mv)
					ourturn = 0
					halfturn = halfturn + 1
					if fromln == "e1":
						wking = 1
					if fromln == "e8":
						bking = 1
#dso todo zugrückführung bei falschen zug										
# old place outturn ans halfturn
			else:
				#print("not a legal move checking for half turn")
				if halfturn != 0:
					#print("Not a legal move!")
					#print(board.legal_moves)
					boardfunctions.clearBoardData()
					boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
					correcterror = fromsq
		except:
			#print("exception checking for half turn")
			if halfturn != 0:
				#print("Not a legal move!")
				#print(board.legal_moves)
				boardfunctions.clearBoardData()
				boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
				correcterror = fromsq
				
		
		

	
		fen = cboard.fen()
		sfen = fen[0 : fen.index(" ")]
		baseboard = chess.BaseBoard(sfen)
		pieces = []
		for x in range(0,64):
			pieces.append(str(chess.BaseBoard(sfen).piece_at(x)))
		fenlog = "/home/pi/centaur/fen.log"
		f = open(fenlog, "w")
		f.write(sfen)
		f.close()
		
		
		epaper.writeText(12,str(mv))
		epaper.drawBoard(pieces)
	if playeriswhite == 0 and newgame == 1 : 
		ourturn = 0
		if str(remotemoves)!= '1234':
			lastmove = '3456'
	print (playeriswhite)
	print('Achtung: '+ lastmove)
	print('Achtung= '+ str(remotemoves)[-4:])
	print('ourturn sollte 0 sein ' + str(ourturn))
	print('sound='+sound)
	if ourturn == 0 and (status == "started" or status=="mate"):
        # Here we wait to get a move from the other player on lichess
		
		startzeit = time.time()
		epaper.writeText(10,whitetime)
		epaper.writeText(1, blacktime)
		while (status == "started" or status == "mate") and str(remotemoves)[-4:] == lastmove and winner != 'white' : 
#			print(winner)
			time.sleep(0.5)
		movestart= time.time()
		if status == "started" or status == 'mate' or winner != "white":
			# There's an incoming move to deal with			
			boardfunctions.beep(boardfunctions.SOUND_GENERAL)
			rr = "   " + str(remotemoves)
			lrmove = rr[-5:].strip()
			lrmove = lrmove[:4]
			lrfrom = lrmove[:2]
			lrto = lrmove[2:4]
			lrfromcalc = (ord(lrfrom[:1]) - 97) + ((int(lrfrom[1:2]) - 1) * 8)
			lrtocalc = (ord(lrto[:1]) - 97) + ((int(lrto[1:2]) - 1) * 8)
			boardfunctions.clearBoardData()
			boardfunctions.ledFromTo(lrfromcalc, lrtocalc)
			# Then wait for a piece to be moved TO that position
			movedto = -1
			while movedto != lrtocalc and winner != 'white' and (status == "started" or status =="mate"):
				move = boardfunctions.MywaitMove()
				valid = 0
# dso todo prüfen ob der zug richtig abgesetzt wurde
				#if move[0] == lrtocalc:
				#	valid = 1
				if len(move) > 1:
					if move[1] == lrtocalc:
						valid = 1
						
						
				if len(move) == 3:
					if move[2] == lrtocalc:
						valid = 1

				if valid == 0:
					boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
					
				
				movedto = lrtocalc 
			boardfunctions.beep(boardfunctions.SOUND_GENERAL)

# check for caslte
			if lrmove == "e1g1" and wking == 0:
				castled = "h1f1"
			if lrmove == "e1c1" and wking == 0:
				castled = "a1d1"
			if lrmove == "e8g8" and bking == 0:
				castled = "h8f8"
			if lrmove == "e8c8" and bking == 0:
				castled = "a8d8"
			if castled =="h1f1" or castled == "a1d1" or castled == "h8f8" or castled == "a8d8" :
				print("move the rook")
				lrfromcalc = (ord(castled[:1]) - 97) + ((int(castled[1:2]) - 1) * 8)
				lrtocalc = (ord(castled[2:3]) - 97) + ((int(castled[3:4]) - 1) * 8)
				
				boardfunctions.clearBoardData()
				boardfunctions.ledFromTo(lrfromcalc, lrtocalc)
				while movedto != lrtocalc and status == "started":
					
					move = boardfunctions.waitMove()
					valid = 1
					castled=""
		# dso todo prüfen ob der zug richtig abgesetzt wurde
#					
#					cmove = move[1] * -1
#					if cmove == lrtocalc:
#							print(cmove)
#							valid = 1
#							castled=""
				
					if valid == 0:
						boardfunctions.beep(boardfunctions.SOUND_WRONG_MOVE)
					else:
						boardfunctions.beep(boardfunctions.SOUND_GENERAL)
					movedto = lrtocalc	
	
			boardfunctions.clearSerial()
			 
			if fromln == "e1":
				wking = 1
			if fromln == "e8":
				bking = 1
			mv = chess.Move.from_uci(rr[-5:].strip())
			cboard.push(mv)
			boardfunctions.ledsOff()
			newgame = 0
			ourturn = 1
			lastmove="2345"
	
		# dso timefix 5.10.21
		
		fen = cboard.fen()
		sfen = fen[0 : fen.index(" ")]
		baseboard = chess.BaseBoard(sfen)
		pieces = []
		for x in range(0,64):
			pieces.append(str(chess.BaseBoard(sfen).piece_at(x)))
		fenlog = "/home/pi/centaur/fen.log"
		f = open(fenlog, "w")
		f.write(sfen)
		f.close()
		epaper.writeText(12,str(mv))
		epaper.drawBoard(pieces)

running = False
epaper.writeText(11, 'Game over')
epaper.writeText(12, f'Winner: {winner}')
epaper.writeText(13, 'reason =' + status)
time.sleep(10)
#epaper.clearScreen()
#boardfunctions.clearSerial()
time.sleep(2)
os._exit(0)
