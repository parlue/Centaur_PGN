#!/bin/bash
while date; do
  inotifywait -e modify "/home/pi/centaur/settings/chessgame_1_2.dat"
  pythonv3.6 /home/pi/v2/createFEN.py
  echo "fertig"
done