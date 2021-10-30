#!/usr/bin/python3.6 

# DGT Centaur V2
# Dirk Sommerfeld dso@vpilots.de
# July, 7th 2021


import urllib
import pickle
import sys
sys.path.append("/home/pi/centaur/")
sys.path.append("/home/pi/v2")
import chess
import chess.pgn
import pathlib
import os
from board import boardfunctions
import time
import urllib
import requests
import socket

from datetime import date
from types import SimpleNamespace
from pathlib import Path

cgame = pathlib.Path("settings/chessgame_1_2.dat")
configfile = pathlib.Path("./v2conf.py")
# updatefile = pathlib.Path("/media/update.tar")



def connectiontest():
	boardfunctions.clearScreen()
	time.sleep(1)
	boardfunctions.writeText(1, "check onlinesatus")
	url = "http://www.google.com"
	timeout = 5
	try:
		request = requests.get(url, timeout=timeout)
		boardfunctions.writeText(2, "Internet alive")
		host_name = socket.gethostname() 
#		host_ip = socket.gethostbyname(host_name) 
		host_ip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
		
		boardfunctions.writeText(3, "IP="+ str(host_ip))
		boardfunctions.writeText(4, "Hostname= " + str(host_name))

	except (requests.ConnectionError, requests.Timeout) as exception:
		boardfunctions.writeText(5, "No connection")	 
	boardfunctions.writeText(6, "ciao...")
	time.sleep(6)



def chessgame():
	boardfunctions.clearScreen()
	#boardfunctions.initScreen()
	time.sleep(1)
	boardfunctions.writeText(1, "check stick ")
	boardfunctions.writeText(2, "check game")
	if (usbstick.exists() and cgame.exists()) :
		# print("in")
		os.system('mount -t vfat /dev/sda1 /media')
		boardfunctions.writeText(3, "stick found")
		counter = pathlib.Path("/media/gamecount.pkl")
		if counter.exists()  :
			f = open('/media/gamecount.pkl', 'rb')
			data = pickle.load(f)
			f.close()
			data = data + 1
			f = open ('/media/gamecount.pkl', 'wb')
			pickle.dump(data, f)
			f.close()

			filecount = str(data)
			
		else :
			data=(1)
			output = open('/media/gamecount.pkl', 'wb')
			pickle.dump(data, output)
			output.close()
			filecount=str(data)

		game = chess.pgn.Game()
		
		game.headers["Event"] = "Centaurgameexport by dso"
		game.headers["White"] = "White"
		game.headers["Black"] = "Black"
		game.headers["Site"] = ""
		game.headers["Date"] = ""
		game.headers["Round"] = ""
		boardfunctions.writeText(4, "open game")


		def create_dummy_module(type_names):
			return SimpleNamespace(**{name: type(name, (), {}) for name in type_names})


		def main():
			sys.modules.update(
				{
				 "chess_game": create_dummy_module(["Chess_Game", "Bitboard_Move"]),
				 "engine": create_dummy_module(["Score_data"]),
				}
			)
			with open("/mnt/chessgame_1_2.dat", "rb") as file:
				boardfunctions.writeText(5, "read game")
				chess_game = pickle.load(file)
				b=len(chess_game.board.move_stack)
				i=1
				cmove=chess_game.board.move_stack[0]
				node = game.add_variation(chess.Move.from_uci(str(cmove)))
				while i < b:
					cmove=chess_game.board.move_stack[i]
					node = node.add_variation(chess.Move.from_uci(str(cmove)))
					i += 1
				#write pgn to disk 
				boardfunctions.writeText(6, "write game")
				filename = "/media/" + filecount + "_mygame.pgn"
				print(game, file=open(filename, "w"), end="\n\n")
				os.system('umount /media')
				boardfunctions.writeText(7, "done..")

		if __name__ == "__main__":
			main()
	else:
		boardfunctions.writeText(3, "no stick or game")
		boardfunctions.writeText(4, "ciao...")
		time.sleep(1)