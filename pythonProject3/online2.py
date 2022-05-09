import uuid

from gameEngine import game as g
from gameEngine import rock as r
import os
from flask import Flask, jsonify

app = Flask(__name__)

idList = {}

iterator = -1


def saveToFile(gameId, tempgame):
    f = open(str(gameId) + ".txt", "w")

    sep = "\n"
    s = str(gameId).replace("\n", "") + sep \
        + str(tempgame.player1Nick).replace("\n", "") + sep \
        + str(tempgame.player2Nick).replace("\n", "") + sep \
        + str(tempgame.turn).replace("\n", "") + sep \
        + str(tempgame.passCounter).replace("\n", "") + sep \
        + str(tempgame.blackStonesSet).replace("\n", "") + sep \
        + str(tempgame.whiteStonesSet).replace("\n", "") + sep \
        + str(tempgame.started).replace("\n", "") + sep \
        + str(tempgame.isOngoing).replace("\n", "") + sep
    if tempgame.koRock is not None:
        s += str(tempgame.koRock.row).replace("\n", "") + "," + str(tempgame.koRock.column).replace("\n", "")\
             + "," + str(tempgame.koRock.stoneColour).replace("\n", "") + sep
    else:
        s += "-1" + "," + "-1" + "," + "-1" + sep
    for i in range(11):
        for j in range(11):
            if not (i == 0 or j == 0 or i == 10 or j == 10):
                s += str(i).replace("\n", "") + "," + str(j).replace("\n", "") + "," \
                     + str(tempgame.board.matrix[i, j].stoneColour).replace("\n", "") + sep

    f.write(s)
    f.close()


def loadStateFromFile(pathToFile):
    f = open(pathToFile, "r")
    itera = 0
    tempgame = g.Game(9, 9, -22, "temp")
    for x in f:
        if itera == 0:
            tempgame.gameID = int(x.replace("\n", ""))
        elif itera == 1:
            tempgame.player1Nick = x.replace("\n", "")
        elif itera == 2:
            tempgame.player2Nick = x.replace("\n", "")
        elif itera == 3:
            tempgame.turn = int(x.replace("\n", ""))
        elif itera == 4:
            tempgame.passCounter = int(x.replace("\n", ""))
        elif itera == 5:
            tempgame.blackStonesSet = int(x.replace("\n", ""))
        elif itera == 6:
            tempgame.whiteStonesSet = int(x.replace("\n", ""))
        elif itera == 7:
            tempgame.started = bool(x.replace("\n", ""))
        elif itera == 8:
            print(x + "kukuku")
            tempgame.isOngoing = int(x.replace("\n", ""))
            print(tempgame.isOngoing)
        elif itera == 9:
            kor = x.split(",")
            print(kor)
            if int(kor[0].replace("\n", "")) == -1 and int(kor[1].replace("\n", "")) == -1 \
                    and int(kor[2].replace("\n", "")) == -1:
                tempgame.koRock = None
            else:
                tempgame.koRock = r.Rock(int(kor[0].replace("\n", "")), int(kor[1].replace("\n", "")),
                                         int(kor[2].replace("\n", "")))
        else:
            rr = x.split(",")
            tempgame.board.setRock(int(rr[0].replace("\n", "")), int(rr[1].replace("\n", "")),
                                   int(rr[2].replace("\n", "")))
        itera += 1
    f.close()
    print(str(tempgame.isOngoing)+ "llllllllllllllllllll")
    return tempgame


@app.route("/load/<int:gameId>/<string:data>")
def loadGame(gameId, data):
    game = loadStateFromFile(str(gameId) + ".txt")
    xyz = data.split("\n")
    for s in xyz:
        rock = s.split(",")
        game.getCurrentBoard().setRock(int(rock[0]), int(rock[1]), int(rock[2]))
    saveToFile(gameId, game)
    return jsonify({"load": "load"})


@app.route("/create/<string:nick>")
def createGame(nick):
    global iterator
    iterator += 1
    gameID = iterator
    idList[gameID] = False
    #createFile(gameID)
    saveToFile(gameID, g.Game(9, 9, gameID, nick))
    return jsonify({"gameId": gameID})


@app.route("/join/<string:nick>")
def joinGame(nick):
    ng = -1
    for gm in list(idList.keys())[:]:
        if gm in idList:
            if not idList[gm]:
                idList[gm] = True
                game = loadStateFromFile(str(gm) + ".txt")
                game.player2Nick = nick
                saveToFile(game.gameID, game)
                ng = game.gameID
                break
    return jsonify({"gameId": ng})


@app.route("/leave/<int:gameId>")
def leaveGame(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    if game.isOngoing == 0 or game.player2Nick == "":
        idList.pop(gameId)
        os.remove(str(gameId) + ".txt")
        return jsonify({"remove": "Game: " + str(gameId) + " was removed"})
    else:
        game.isOngoing = 0
        print(game.isOngoing)
        saveToFile(gameId, game)
        return jsonify({"remove": "Game: " + str(gameId) + " is being removed"})


@app.route("/onGoing/<int:gameId>")
def isOnGoing(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"onGoing": game.isOngoing})


@app.route("/pass/<int:gameId>")
def passMove(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    if game.passTurn():
        game.isOngoing = 0
    saveToFile(gameId, game)
    return jsonify({"passCounter": game.passCounter})


@app.route("/checkT/<int:gameId>")
def turn(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"turn": game.turn})


@app.route("/board/<int:gameId>")
def showBoard(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    board = game.board
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
    return jsonify({"board": line})


@app.route("/points/<int:gameId>")
def showPoints(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    blackTerritoryPoints = game.getTerritoryPoints(1)
    whiteTerritoryPoints = game.getTerritoryPoints(2)
    blackStonePoints = game.countStones(2)
    whiteStonePoints = game.countStones(1)
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
    game = loadStateFromFile(str(gameId) + ".txt")
    print(str(game.isOngoing) + "ppppppp")
    print(str(game.turn) + "-----------")
    posX = -1
    posY = -1
    while posX < 1 or posX > game.getCurrentBoard().rowNumber - 1 \
            or posY < 1 or posY > game.getCurrentBoard().rowNumber - 1:
        posX = x
        posY = y
    if not game.insertStone(posX, posY):
        return jsonify({"response": "Bad Move!"})
    saveToFile(gameId, game)
    print(game.turn)
    return jsonify({"response": "Move x = " + str(x) + " y = " + str(y)})


if __name__ == '__main__':
    app.run()
