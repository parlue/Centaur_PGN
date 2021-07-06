#!/usr/bin/python3.6 

# DGT Centaur game exporter version 0.99
# Dirk Sommerfeld dso@vpilots.de
# May, 19th 2021
# Please play your game and if you want to get a PGN file of the actual board, please swicth off the centaur.
# Insert a USB stick and switch on the centaur, after the game is restarted
# you can remove the USB stick. The PGN file was stored on it.
# You will found a (No)_mygame.pgn on it. That's all
# Please use unly USB-Sticks with a Windows fat partition


import pickle
import sys
import chess
import chess.pgn
import pathlib
import os
import boardfuntions
import time
from datetime import date
from types import SimpleNamespace
from pathlib import Path

# check stick
usbstick = pathlib.Path("/dev/sda1")
cgame = pathlib.Path("/mnt/chessgame_1_2.dat")
boardfunctions.clearScreen()
boardfunctions.writeText(1, "check stick")
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