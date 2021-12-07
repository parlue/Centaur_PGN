#!/usr/bin/python3.6 


# This file is part of the Centaur V2 Mod open source software
# ( https://github.com/dsommerfeld/DGTCentaur-2.0-by-dso )
#
# DGTCentaur Mods is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# DGTCentaur Mods is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see
#
# https://github.com/dsommerfeld/DGTCentaur-2.0-by-dso/blob/master/LICENSE.md
#
# This and any other notices must remain intact and unaltered in any
# distribution, modification, variant, or derivative of this software.

# PGN Game exporter
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
			
			
			if b == 0:
				fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
				fenlog = "/home/pi/centaur/fen.log"
				f = open(fenlog,"w")
				f.write(fen)
				f.close()
			
			else :
				b = b -1
				cmove=chess_game.board.move_stack[b]
				chess.Move.from_uci(str(cmove))
				fenlog = "/home/pi/centaur/fen.log"
				f = open(fenlog,"w")
				f.write(chess.board.fen())
				f.close()
			
			
			

	if __name__ == "__main__":
		main()
else:
	print('No Game')