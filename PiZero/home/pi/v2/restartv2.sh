#!/bin/sh
sleep 45

if ps -ef | grep -v grep | grep menu.py ; then

     exit 0

else
	cd /home/pi/v2
    sudo python3 menu.py &


    exit 0

fi