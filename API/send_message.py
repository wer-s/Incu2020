from flask import Flask, request
import requests
import json
#import ncclient
#from ncclient import manager
import xml.dom.minidom
from random import randrange
import time

############## Bot details ##############

bot_name = 'titato@webex.bot'
#roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vYTI5Y2I4ZTItOTU4Yi0zZmRhLWI0YzItZTE0YjY1YTQ3MTk5'
token = 'Mzg0N2ViYjgtMDhmZC00Yzc2LTk4YzAtM2MxYmQwNjE4YmU0MmJjZmM4YzQtYjI4_PF84_consumer'
header = {"content-type": "application/json; charset=utf-8", 
		  "authorization": "Bearer " + token}


############## TTT ##############
def DisplayBoard(board):
    vis_board = ""
    #vis_board = """+-------+-------+-------+\n\n"""
    for row in range(3):
        #vis_board += """|            """ * 3 + "|\n\n"
        for col in range(3):
            vis_board += "|     " + str(board[row][col]) + "    "
        vis_board += "|\n\n"
        #vis_board += "|\n\n" + "|           " * 3 + "|\n\n" + "+-------" * 3 + "+\n\n"
    return vis_board


def EnterMove(board, move):
    print(move)
    correctMove = False
    while not correctMove:
        #move = input("Enter your move: ")
        correctMove = len(move) == 1 and move >= '1' and move <= '9'
        if not correctMove:
            return "Wrong move, try again!"
            continue
        move = int(move) - 1
        row = move // 3
        col = move % 3
        correctMove = board[row][col] not in ['O', 'X']
        if not correctMove:
            return "Field is occupied, try again!"
            continue
    board[row][col] = 'O'
    return DisplayBoard(board)


def MakeListOfFreeFields(board):
    free = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O', 'X']:
                free.append((row,col))
    return free


def VictoryFor(board, sign):
    if sign == 'X':
        who = "comp"
    elif sign == 'O':
        who = "player"
    else:
        who = None
    cross1 = cross2 = True
    for rc in range(3):
        if board[rc][0] == sign and board[rc][1] == sign and board[rc][2] == sign:
            return who
        elif board[0][rc] == sign and board[1][rc] == sign and board[2][rc] == sign:
            return who
        if board[rc][rc] != sign:
            cross1 = False
        if board[2 - rc][2 - rc] != sign:
            cross2 = False
    if cross1 or cross2:
        return who
    return None


def DrawMove(board):
    free = MakeListOfFreeFields(board)
    freeAmount = len(free)
    if freeAmount > 0:
        this = randrange(freeAmount)
        row, col = free[this]
        board[row][col] = 'X'
    return DisplayBoard(board)


board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
board[1][1] = 'X'
free = MakeListOfFreeFields(board)
playerturn = True
##while len(free):
##	DisplayBoard(board)
##	if playerturn:
##		EnterMove(board)
##		victor = VictoryFor(board,'O')
##	else:
##		DrawMove(board)
##		victor = VictoryFor(board,'X')
##	if victor != None:
##		break
##	playerturn = not playerturn
##	free = MakeListOfFreeFields(board)

##DisplayBoard(board)
##if victor == 'player':
##	print("You won!")
##elif victor == 'comp':
##	print("I won")
##else:
##	print("Tie!")

def test():
    return "success"

############## Flask Application ##############

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sendMessage():
	webhook = request.json
	url = 'https://api.ciscospark.com/v1/messages'
	msg = {"roomId": webhook["data"]["roomId"]}
	sender = webhook["data"]["personEmail"]
	message = getMessage()
	if (sender != bot_name):
		if (message == "help"):
			msg["markdown"] = "Welcome to **TicTacToeBot**!\n\n Enter 'start game' to start game, if you would like to choose field enter the number"
		elif (message >= '1' and message <= '9' and len(message) == 1):
			response = str(EnterMove(board, message))
			winner = ""			
			if VictoryFor(board, 'O') == "player":
                            winner = "player"			
			response += "\n\nMy turn:\n\n" + DrawMove(board)
			if VictoryFor(board, 'X') == "comp":
                            winner = "comp"
			if winner == "comp":
                            msg["markdown"] = str(DisplayBoard(board)) + "\n\nI won!"
			elif winner == "player":
                            msg["markdown"] = str(DisplayBoard(board)) + "\n\nYou won!"                            
			else:
                            msg["markdown"] = response
		elif (message >= '1' and message <= '9'):
                        msg["markdown"] = "Wrong field"
		elif (message == "start game"):
                        msg["markdown"] = "Welcome to **TicTacToeBot**! I'm first :)\n\n" + str(DisplayBoard(board)) + "\nEnter your move: "
		else:
                        msg["markdown"] = "I'm sorry, but I don't understand :("
		requests.post(url,data=json.dumps(msg), headers=header, verify=True)

def getMessage():
	webhook = request.json
	url = 'https://api.ciscospark.com/v1/messages/' + webhook["data"]["id"]
	get_msgs = requests.get(url, headers=header, verify=True)
	message = get_msgs.json()['text']
	return message

app.run(debug = True)
