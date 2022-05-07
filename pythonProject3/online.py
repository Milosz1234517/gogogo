from gameEngine import game as g
import os
from flask import Flask, jsonify

app = Flask(__name__)

posX = -1
posY = -1
iterator = 0
game = g.Game(9, 9)


@app.route("/board")
def showBoard():
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


@app.route("/points")
def showPoints():
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


@app.route("/cords/<int:x>,<int:y>")
def insertCoordinates(x, y):
    game.posX = -1
    game.posY = -1
    while game.posX < 1 or game.posX > game.getCurrentBoard().rowNumber - 1 \
            or game.posY < 1 or game.posY > game.getCurrentBoard().rowNumber - 1:
        game.posX = x
        game.posY = y
    if not game.insertStone(game.posX, game.posY):
        return jsonify({"response": "Bad Move!"})


if __name__ == '__main__':
    app.run()
