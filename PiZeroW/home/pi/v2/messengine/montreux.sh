#!/bin/bash

cd /home/pi/v2/mess; SDL_VIDEODRIVER=dummy /usr/games/mame -skip_gameinfo -lightgunprovider none -video none -plugin chessengine montreux

