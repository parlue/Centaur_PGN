import sys
sys.path.append("/home/pi/centaur/")
import ssl
import time
import threading
import boardfunctions
import chess
import v2conf

# Run a Centaur as an DGT Smartboard
# Open the serial port, baudrate is 115200
ser = serial.Serial("/dev/ttyUSB1", baudrate=115200, timeout=0.2)

# wait for boardmove
def waitMove():
    # Wait for a player to lift a piece and set it down somewhere different
    lifted = -1
    placed = -1
    moves = []
    while placed == -1:
        ser.read(100000)
        tosend = bytearray(b'\x83\x06\x50\x59')
        ser.write(tosend)
        expect = bytearray(b'\x85\x00\x06\x06\x50\x61')
        resp = ser.read(10000)
        resp = bytearray(resp)
        if (bytearray(resp) != expect):
            if (resp[0] == 133 and resp[1] == 0):
                for x in range(0, len(resp) - 1):
                    if (resp[x] == 64):
                        # Calculate the square to 0(a1)-63(h8) so that
                        # all functions match
                        square = resp[x + 1]
                        squarerow = (square // 8)
                        squarecol = (square % 8)
                        squarerow = 7 - squarerow
                        newsquare = (squarerow * 8) + squarecol
                        lifted = newsquare
                        print(lifted)
                        moves.append(newsquare * -1)
                    if (resp[x] == 65):
                        # Calculate the square to 0(a1)-63(h8) so that
                        # all functions match
                        square = resp[x + 1]
                        squarerow = (square // 8)
                        squarecol = (square % 8)
                        squarerow = 7 - squarerow
                        newsquare = (squarerow * 8) + squarecol
                        placed = newsquare
                        moves.append(newsquare)
                        print(placed)
        tosend = bytearray(b'\x94\x06\x50\x6a')
        ser.write(tosend)
        expect = bytearray(b'\xb1\x00\x06\x06\x50\x0d')
        resp = ser.read(10000)
        resp = bytearray(resp)
    print(moves)
    return moves
	


# read board

def poll():
 
    ser.read(100000)
    tosend = bytearray(b'\x83\x06\x50\x59')
    ser.write(tosend)
    expect = bytearray(b'\x85\x00\x06\x06\x50\x61')
    resp = ser.read(10000)
    resp = bytearray(resp)
    if (bytearray(resp) != expect):
        if (resp[0] == 133 and resp[1] == 0):
            for x in range(0, len(resp) - 1):
                if (resp[x] == 64):
                    print("PIECE LIFTED")
                    # Calculate the square to 0(a1)-63(h8) so that
                    # all functions match
                    square = resp[x + 1]
                    squarerow = (square // 8)
                    squarecol = (square % 8)
                    squarerow = 7 - squarerow
                    newsquare = (squarerow * 8) + squarecol
                    print(newsquare)
                if (resp[x] == 65):
                    print("PIECE PLACED")
                    # Calculate the square to 0(a1)-63(h8) so that
                    # all functions match
                    square = resp[x + 1]
                    squarerow = (square // 8)
                    squarecol = (square % 8)
                    squarerow = 7 - squarerow
                    newsquare = (squarerow * 8) + squarecol
                    print(newsquare)
    tosend = bytearray(b'\x94\x06\x50\x6a')
    ser.write(tosend)
    expect = bytearray(b'\xb1\x00\x06\x06\x50\x0d')
    resp = ser.read(10000)
    resp = bytearray(resp)
    if (resp != expect):
        if (resp.hex() == "b10011065000140a0501000000007d4700"):
            print("BACK BUTTON")
        if (resp.hex() == "b10011065000140a0510000000007d175f"):
            print("TICK BUTTON")
        if (resp.hex() == "b10011065000140a0508000000007d3c7c"):
            print("UP BUTTON")
        if (resp.hex() == "b10010065000140a050200000000611d"):
            print("DOWN BUTTON")
        if (resp.hex() == "b10010065000140a0540000000006d67"):
            print("HELP BUTTON")
        if (resp.hex() == "b10010065000140a0504000000002a68"):
            print("PLAY BUTTON")


SOUND_GENERAL = 1
SOUND_FACTORY = 2
SOUND_POWER_OFF = 3
SOUND_POWER_ON = 4
SOUND_WRONG = 5
SOUND_WRONG_MOVE = 6



