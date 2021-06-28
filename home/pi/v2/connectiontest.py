import urllib
try :
    stri = "https://www.google.com"
    data = urllib.urlopen(stri)
    print "Connected"
except e:
    print "not connected" ,e 
