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
import urllib
import sys
import chess
import chess.pgn
import pathlib
import os
import boardfunctions
import time
import smtplib
import v2.conf
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from datetime import date
from types import SimpleNamespace
from pathlib import Path


cgame = pathlib.Path("/mnt/chessgame_1_2.dat")
boardfunctions.clearSerial()
boardfunctions.initScreen()
boardfunctions.writeText(1, "check connection")
cStatus = 0
try :
	stri = "https://www.google.com"
	data = urllib.urlopen(stri)
	boardfunctions.writeText(2, "internet alive")
	cStatus = 1
except e:
	boardfunctions.writeText(2, "No connection")
	boardfunctions.writeText(3, "check internet")
if (cgame.exists() and (cStatus == 1)):
	# print("in")

	filecount= ""

	game = chess.pgn.Game()
	
	game.headers["Event"] = "Centaurgameexport by dso"
	game.headers["White"] = "White"
	game.headers["Black"] = "Black"
	game.headers["Site"] = ""
	game.headers["Date"] = ""
	game.headers["Round"] = ""
	boardfunctions.writeText(3, "open game")


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
			boardfunctions.writeText(4, "read game")
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
			boardfunctions.writeText(5, "write game")
			filename = "/mmt/" + filecount + "_mygame.pgn"
			print(game, file=open(filename, "w"), end="\n\n")
			boardfunctions.writeText(6, "process mail")
			## mailcode here
			"""		
			def send_mail(send_from, send_to, subject, message, files=[/mnt/_mygame],
			server="localhost", port=587, username='', password='',
			use_tls=True):	
			msg = MIMEMultipart()
			msg['From'] = send_from
			msg['To'] = COMMASPACE.join(send_to)
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = subject
			msg.attach(MIMEText(message))
			for path in files:
				part = MIMEBase('application', "octet-stream")
				with open(path, 'rb') as file:
				part.set_payload(file.read())
				encoders.encode_base64(part)
				part.add_header('Content-Disposition',
				'attachment; filename="{}"'.format(Path(path).name))
				msg.attach(part)
				smtp = smtplib.SMTP(server, port)
				if use_tls:
					smtp.starttls()
				smtp.login(username, password)
				smtp.sendmail(send_from, send_to, msg.as_string())
				smtp.quit()
			
			"""

	if __name__ == "__main__":
		main()
else:
	boardfunctions.writeText(3, "no game found")
	boardfunctions.writeText(4, "ciao...")
	time.sleep(1)