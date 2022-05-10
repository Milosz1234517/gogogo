import dialog
from gameEngine import game as g
from gameEngine import rock as r
import os
from flask import Flask, jsonify

app = Flask(__name__)

idList = {}

globalID = -1


def saveToFile(game):
    file = open(str(game.gameID) + ".txt", "w")
    separator = "\n"
    data = str(game.gameID).replace("\n", "") + separator \
        + str(game.player1Nick).replace("\n", "") + separator \
        + str(game.player2Nick).replace("\n", "") + separator \
        + str(game.turn).replace("\n", "") + separator \
        + str(game.passCounter).replace("\n", "") + separator \
        + str(game.blackStonesSet).replace("\n", "") + separator \
        + str(game.whiteStonesSet).replace("\n", "") + separator \
        + str(game.started).replace("\n", "") + separator \
        + str(game.isOngoing).replace("\n", "") + separator
    if game.koRock is not None:
        data += str(game.koRock.row).replace("\n", "") + "," + str(game.koRock.column).replace("\n", "") \
             + "," + str(game.koRock.stoneColour).replace("\n", "") + separator
    else:
        data += "-1" + "," + "-1" + "," + "-1" + separator
    for i in range(11):
        for j in range(11):
            if not (i == 0 or j == 0 or i == 10 or j == 10):
                data += str(i).replace("\n", "") + "," + str(j).replace("\n", "") + "," \
                     + str(game.board.matrix[i, j].stoneColour).replace("\n", "") + separator
    file.write(data)
    file.close()


def loadStateFromFile(pathToFile):
    file = open(pathToFile, "r")
    lineNumber = 0
    game = g.Game(9, 9, -1, "")
    for line in file:
        if lineNumber == 0:
            game.gameID = int(line.replace("\n", ""))
        elif lineNumber == 1:
            game.player1Nick = line.replace("\n", "")
        elif lineNumber == 2:
            game.player2Nick = line.replace("\n", "")
        elif lineNumber == 3:
            game.turn = int(line.replace("\n", ""))
        elif lineNumber == 4:
            game.passCounter = int(line.replace("\n", ""))
        elif lineNumber == 5:
            game.blackStonesSet = int(line.replace("\n", ""))
        elif lineNumber == 6:
            game.whiteStonesSet = int(line.replace("\n", ""))
        elif lineNumber == 7:
            game.started = bool(line.replace("\n", ""))
        elif lineNumber == 8:
            game.isOngoing = int(line.replace("\n", ""))
        elif lineNumber == 9:
            kor = line.split(",")
            if int(kor[0].replace("\n", "")) == -1 and int(kor[1].replace("\n", "")) == -1 \
                    and int(kor[2].replace("\n", "")) == -1:
                game.koRock = None
            else:
                game.koRock = r.Rock(int(kor[0].replace("\n", "")), int(kor[1].replace("\n", "")),
                                     int(kor[2].replace("\n", "")))
        else:
            rr = line.split(",")
            game.board.setRock(int(rr[0].replace("\n", "")), int(rr[1].replace("\n", "")),
                               int(rr[2].replace("\n", "")))
        lineNumber += 1
    file.close()
    return game


@app.route("/load/<int:gameId>/<string:data>")
def loadGame(gameId, data):
    game = loadStateFromFile(str(gameId) + ".txt")
    dataTable = data.split("\n")
    for s in dataTable:
        rock = s.split(",")
        game.getCurrentBoard().setRock(int(rock[0]), int(rock[1]), int(rock[2]))
    saveToFile(game)
    return jsonify({"load": "Data loaded"})


@app.route("/create/<string:nick>")
def createGame(nick):
    global globalID
    globalID += 1
    gameID = globalID
    idList[gameID] = False
    saveToFile(g.Game(9, 9, gameID, nick))
    return jsonify({"gameId": gameID})


@app.route("/players/<int:gameId>")
def players(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"player1": game.player1Nick, "player2": game.player2Nick})


@app.route("/join/<string:nick>")
def joinGame(nick):
    myGameId = -1
    for gameIdKey in list(idList.keys())[:]:
        if gameIdKey in idList:
            if not idList[gameIdKey]:
                idList[gameIdKey] = True
                game = loadStateFromFile(str(gameIdKey) + ".txt")
                game.player2Nick = nick
                saveToFile(game)
                myGameId = game.gameID
                break
    return jsonify({"gameId": myGameId})


@app.route("/leave/<int:gameId>")
def leaveGame(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    if game.isOngoing == 0 or game.player2Nick == "":
        idList.pop(gameId)
        os.remove(str(gameId) + ".txt")
        return jsonify({"remove": "Game: " + str(gameId) + " was removed"})
    else:
        game.isOngoing = 0
        saveToFile(game)
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
    saveToFile(game)
    return jsonify({"passCounter": game.passCounter})


@app.route("/checkT/<int:gameId>")
def turn(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"turn": game.turn})


@app.route("/board/<int:gameId>")
def showBoard(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"board": dialog.makeBoardString(game.board)})


@app.route("/points/<int:gameId>")
def showPoints(gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"points": dialog.makePointsString(game)})


@app.route("/cords/<int:y>,<int:x>,<int:gameId>")
def insertCoordinates(y, x, gameId):
    game = loadStateFromFile(str(gameId) + ".txt")
    dialog.makeMove(game, x, y)
    saveToFile(game)
    return jsonify({"response": "Move x = " + str(x) + " y = " + str(y)})


if __name__ == '__main__':
    app.run()
