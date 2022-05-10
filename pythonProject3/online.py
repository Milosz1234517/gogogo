from gameEngine import game as g
from flask import Flask, jsonify
import dialog

app = Flask(__name__)

games = {}

globalID = -1


@app.route("/players/<int:gameId>")
def players(gameId):
    return jsonify({"player1": games[gameId].player1Nick, "player2": games[gameId].player2Nick})


@app.route("/load/<int:gameId>/<string:data>")
def loadGame(gameId, data):
    dataTable = data.split("\n")
    for line in dataTable:
        rock = line.split(",")
        games[gameId].getCurrentBoard().setRock(int(rock[0]), int(rock[1]), int(rock[2]))
    return jsonify({"load": "load"})


@app.route("/create/<string:nick>")
def createGame(nick):
    global globalID
    globalID += 1
    games[globalID] = g.Game(9, 9, globalID, nick)
    return jsonify({"gameId": games[globalID].gameID})


@app.route("/join/<string:nick>")
def joinGame(nick):
    myGameID = -1
    for gameKeyId in list(games.keys())[:]:
        if gameKeyId in games:
            if not games[gameKeyId].started:
                games[gameKeyId].started = True
                games[gameKeyId].player2Nick = nick
                myGameID = gameKeyId
                break
    return jsonify({"gameId": myGameID})


@app.route("/leave/<int:gameId>")
def leaveGame(gameId):
    if games[gameId].isOngoing == 0 or games[gameId].player2Nick == "":
        games.pop(gameId)
        return jsonify({"remove": "Game: " + str(gameId) + " was removed"})
    else:
        games[gameId].isOngoing = 0
        return jsonify({"remove": "Game: " + str(gameId) + " is being removed"})


@app.route("/onGoing/<int:gameId>")
def isOnGoing(gameId):
    return jsonify({"onGoing": games[gameId].isOngoing})


@app.route("/pass/<int:gameId>")
def passMove(gameId):
    if games[gameId].passTurn():
        games[gameId].isOngoing = 0
    return jsonify({"passCounter": games[gameId].passCounter})


@app.route("/checkT/<int:gameId>")
def turn(gameId):
    return jsonify({"turn": games[gameId].turn})


@app.route("/board/<int:gameId>")
def showBoard(gameId):
    return jsonify({"board": dialog.makeBoardString(games[gameId].board)})


@app.route("/points/<int:gameId>")
def showPoints(gameId):
    return jsonify({"points": dialog.makePointsString(games[gameId])})


@app.route("/cords/<int:y>,<int:x>,<int:gameId>")
def insertCoordinates(y, x, gameId):
    return jsonify({"response": dialog.makeMove(games[gameId], x, y)})


if __name__ == '__main__':
    app.run()
