import urllib
import boardfunctions
boardfunctions.clearScreen()
try :
    stri = "https://www.google.com"
    data = urllib.urlopen(stri)
    boardfunctions.writeText(10, "internet alive")
except e:
    boardfunctions.writeText(10, "No Internet connection") 

