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
import time
from datetime import date
from types import SimpleNamespace
from pathlib import Path

cgame = pathlib.Path("/home/pi/centaur/settings/chessgame_1_2.dat")

if cgame.exists() :
	# print("in")
	
	counter = pathlib.Path("/home/pi/centaur/settings/gamecount.pkl")
	if counter.exists()  :
		f = open('/home/pi/centaur/settings/gamecount.pkl', 'rb')
		data = pickle.load(f)
		f.close()
		data = data + 1
		f = open ('/home/pi/centaur/settings/gamecount.pkl', 'wb')
		pickle.dump(data, f)
		f.close()

		filecount = str(data)
		
	else :
		data=(1)
		output = open('/home/pi/centaur/settings/gamecount.pkl', 'wb')
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
	


	def create_dummy_module(type_names):
		return SimpleNamespace(**{name: type(name, (), {}) for name in type_names})


	def main():
		sys.modules.update(
			{
             "chess_game": create_dummy_module(["Chess_Game", "Bitboard_Move"]),
             "engine": create_dummy_module(["Score_data"]),
			}
		)
		with open("/home/pi/centaur/settings/chessgame_1_2.dat", "rb") as file:
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
			filename = "/home/pi/centaur/settings/" + filecount + "_mygame.pgn"
			print(game, file=open(filename, "w"), end="\n\n")
			

	if __name__ == "__main__":
		main()
else:
	print('No Game')