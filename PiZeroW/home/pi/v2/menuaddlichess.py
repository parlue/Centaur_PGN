if result == "Lichess":
		lichessmenu = {'Current': 'Current', 'New': 'New Game'}
		result = boardfunctions.doMenu(lichessmenu)
		print(result)
		# Current game will launch the screen for the current
		if (result != "BACK"):
			if (result == "Current"):
				boardfunctions.clearScreen()
				os.chdir("/home/pi/v2")
				os.system("/usr/bin/python3.6 /home/pi/v2/lichessV4.py current")
				sys.exit()

			livemenu = {'Rated': 'Rated', 'Unrated': 'Unrated'}
			result = boardfunctions.doMenu(livemenu)
			if result == "Rated":
				rated=True
			else:	
				rated=False
			colormenu = {'white': 'White', 'random': 'Random', 'black': 'Black'}
			result = boardfunctions.doMenu(colormenu)
			color = result
			timemenu = {'10 , 5': '10+5 minutes' , '15 , 10': '15+10 minutes', '30': '30 minutes', '30 , 20': '30+20 minutes', '60 , 20': '60+20 minutes'}
			result = boardfunctions.doMenu(timemenu)
			if result =='10 , 5':
				gtime = '10'
				gincrement = '5'
			if result == '15 , 10':
				gtime = '15'
				gincrement = '10'
			if result == '30':
				gtime = '30'
				gincrement = '0'
			if result == '30 , 20':	
				gtime = '30'
				gincrement = '20'
			if result == "60 , 20":
				gtime = '60'
				gincrement = '20'
		
			os.chdir("/home/pi/v2")
			os.system(f"/usr/bin/python3.6 /home/pi/v2/lichessV4.py New {gtime} {gincrement} {rated} {color}")