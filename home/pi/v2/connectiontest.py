import urllib
import boardfunctions
import time()
boardfunctions.clearScreen()
boardfunctions.writeText(1, "check onlinesatus")
try :
    stri = "https://www.google.com"
    data = urllib.urlopen(stri)
    boardfunctions.writeText(2, "internet alive")
except e:
    boardfunctions.writeText(2, "No connection") 
boardfunctions.writeText(3, "ciao...")
time.sleep(1)

