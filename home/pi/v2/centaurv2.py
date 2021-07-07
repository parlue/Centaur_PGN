#!/usr/bin/python3.6 

# DGT Centaur V2
# Dirk Sommerfeld dso@vpilots.de
# July, 7th 2021


import urllib
import pickle
import sys
sys.path.append("/home/pi/centaur/")
import chess
import chess.pgn
import pathlib
import os
import boardfunctions
import time
from datetime import date
from types import SimpleNamespace
from pathlib import Path

usbstick = pathlib.Path("/dev/sda1")
cgame = pathlib.Path("/mnt/chessgame_1_2.dat")
configfile = pathlib.Path("/media/v2conf.py")
updatefile = pathlib.Path("/media/update.tar")

def update();
	boardfunctions.clearScreen()
	boardfunctions.writeText(1, "check stick )
	if usbstick.exists() :
		os.system('mount -t vfat /dev/sda1 /media')
		boardfunctions.writeText(2, "stick found")
		boardfunctions.writeText(3, "check update")
		if updatefile.exists():
			boardfunctions.writeText(4, "update found")
			boardfunctions.writeText(5, "process update")
			os.system('mkdir /media/tmp')
			os.system('tar xvf /media/update.tar /media/tmp/')
			os.system('/media/tmp/update.sh')
			os.system('rm -rf /media/tmp')
			os.system('rm /media/update.tar')
			os.system('umount /media')
			boardfunctions.writeText(6, "done")
			boardfunctions.writeText(7, "reboot now")
			time.sleep(1)
			boardfunctions.clearScreen()
			boardfunctions.sleepScreen()
			boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
			os.system("/sbin/reboot")
			sys.exit()
		
		else :
			boardfunctions.writeText(4, "update missed")
			boardfunctions.writeText(5, "ciao...")
			time.sleep(1)
		
	else :
		boardfunctions.writeText(2, "no stick found")
		boardfunctions.writeText(3, "ciao...")
		time.sleep(1)

def connectiontest():
	boardfunctions.clearScreen()
	time.sleep(1)
	boardfunctions.writeText(1, "check onlinesatus")
	try :
		stri = "https://www.google.com"
		data = urllib.urlopen(stri)
		boardfunctions.writeText(2, "internet alive")
	except e:
		boardfunctions.writeText(2, "No connection") 
	boardfunctions.writeText(3, "ciao...")
	time.sleep(1)

def getconfig():
	boardfunctions:clearScreen()
	time.sleep(1)
	boardfunctions.writeText(1, "check stick ")
	if usbstick.exists() :
			os.system('mount -t vfat /dev/sda1 /media')
			boardfunctions.writeText(2, "stick found")
			boardfunctions.writeText(3, "check update")
			if configfilefile.exists():
				boardfunctions.writeText(4, "config found")
				os.system('mount -o remount,rw /')
				boardfunctions.writeText(5, "import config")
				os.system('cp /media/v2conf.py /home/pi/v2/')
				os.system('sync')
				os.system('mount -o remount,r /')
				boardfunctions.writeText(6, "done")
				time.sleep(1)
				os.system('unount /media')
				boardfunctions.writeText(7, "reboot now")
				boardfunctions.clearScreen()
				boardfunctions.sleepScreen()
				boardfunctions.beep(boardfunctions.SOUND_POWER_OFF)
				os.system("/sbin/reboot")
				sys.exit()
			
			else :
				boardfunctions.writeText(4, "no config")
				time.sleep(2)
			
	else :
		boardfunctions.writeText(2, "No stick")
		boardfunctions.writeText(3, "ciao....")
		time.sleep(2)

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