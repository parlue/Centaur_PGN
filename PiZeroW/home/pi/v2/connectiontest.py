import urllib
import time
import requests
print("check onlinesatus")
url = "http://www.google.com"
timeout= 5
try:
	request = requests.get(url, timeout=timeout)
	print("internet alive")
except (requests.ConnectionError, requests.Timeout) as exception:
	print("No connection") 
print ("ciao...")
time.sleep(1)

