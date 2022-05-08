import uuid

from gameEngine import game as g
import os
from flask import Flask, jsonify

app = Flask(__name__)

posX = -1
posY = -1
games = {}

iterator = -1


@app.route("/create/<string:nick>")
def createGame(nick):
    global iterator
    iterator += 1
    games[iterator] = g.Game(9, 9, iterator, nick)
    return jsonify({"gameId": games[iterator].gameID})


@app.route("/join/<string:nick>")
def joinGame(nick):
    ng = None
    for gm in games.keys():
        if not games[gm].started:
            games[gm].started = True
            games[gm].player2Nick = nick
            ng = gm
            break
    return jsonify({"gameId": ng})


@app.route("/leave/<int:gameId>")
def leaveGame(gameId):
    if not games[gameId].isOngoing:
        games.pop(gameId)
        return jsonify({"remove": "Game: " + str(gameId) + " was removed"})
    else:
        games[gameId].isOngoing = False
        return jsonify({"remove": "Game: " + str(gameId) + " is being removed"})


@app.route("/onGoing/<int:gameId>")
def isOnGoing(gameId):
    return jsonify({"onGoing": games[gameId].isOngoing})


@app.route("/end/<int:gameId>")
def finishGame(gameId):
    games.pop(gameId)
    return jsonify({"remove": "Game: " + str(gameId) + " was removed"})


@app.route("/pass/<int:gameId>")
def passMove(gameId):
    games[gameId].passTurn()
    return jsonify({"response": "Turn passed", "passCounter": games[gameId].passCounter})


@app.route("/checkT/<int:gameId>")
def turn(gameId):
    return jsonify({"turn": games[gameId].turn})


@app.route("/board/<int:gameId>")
def showBoard(gameId):
    board = games[gameId].board
    numberInZeroRow = 1
    numberInZeroColumn = 1
    numberInLastRow = 1
    numberInLastColumn = 1
    line = ""
    for i in range(board.rowNumber):
        for j in range(board.columnNumber):
            if board.matrix[i, j].stoneColour == 0:
                char = " "
            elif board.matrix[i, j].stoneColour == 1:
                char = "W"
            elif board.matrix[i, j].stoneColour == 2:
                char = "B"
            elif board.matrix[i, j].stoneColour == 3:
                if board.rowNumber < 12 or board.columnNumber < 12:
                    if (i == 0 or i == board.rowNumber - 1) and (j == 0 or j == board.columnNumber - 1):
                        char = "O"
                    elif i == 0:
                        char = numberInZeroColumn
                        numberInZeroColumn += 1
                    elif i == board.rowNumber - 1:
                        char = numberInLastColumn
                        numberInLastColumn += 1
                    elif j == 0:
                        char = numberInZeroRow
                        numberInZeroRow += 1
                    else:
                        char = numberInLastRow
                        numberInLastRow += 1
                else:
                    char = "O"
            else:
                char = "E"
            line += "|" + str(char)
        line += "|"
        line += "\n"
    return jsonify({"board": line, "turn": games[gameId].turn})


@app.route("/points/<int:gameId>")
def showPoints(gameId):
    blackTerritoryPoints = games[gameId].getTerritoryPoints(1)
    whiteTerritoryPoints = games[gameId].getTerritoryPoints(2)
    blackStonePoints = games[gameId].countStones(2)
    whiteStonePoints = games[gameId].countStones(1)
    return jsonify({"points": "Black Territory: "
                              + str(blackTerritoryPoints) +
                              "\nBlack Stones: " +
                              str(blackStonePoints) +
                              "\nBlack Points: " +
                              str(blackTerritoryPoints +
                                  blackStonePoints) +
                              "\n" + "\nWhite Territory: " +
                              str(whiteTerritoryPoints) +
                              "\nWhite Stones: " +
                              str(whiteStonePoints) +
                              "\nWhite Points: "
                              + str(whiteTerritoryPoints +
                                    whiteStonePoints + 7.5)
                              + "\n"})


@app.route("/cords/<int:y>,<int:x>,<int:gameId>")
def insertCoordinates(y, x, gameId):
    games[gameId].posX = -1
    games[gameId].posY = -1
    while games[gameId].posX < 1 or games[gameId].posX > games[gameId].getCurrentBoard().rowNumber - 1 \
            or games[gameId].posY < 1 or games[gameId].posY > games[gameId].getCurrentBoard().rowNumber - 1:
        games[gameId].posX = x
        games[gameId].posY = y
    if not games[gameId].insertStone(games[gameId].posX, games[gameId].posY):
        return jsonify({"response": "Bad Move!"})
    return jsonify({"response": "Move x = " + str(x) + " y = " + str(y)})


if __name__ == '__main__':
    app.run()
