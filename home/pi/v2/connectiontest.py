import urllib
try :
    stri = "https://www.google.com"
    data = urllib.urlopen(stri)
    echo "Connected"
except e:
    echo "not connected" ,e 
