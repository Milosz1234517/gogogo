def makePointsString(game):
    blackTerritoryPoints = game.getTerritoryPoints(1)
    whiteTerritoryPoints = game.getTerritoryPoints(2)
    blackStonePoints = game.countStones(2)
    whiteStonePoints = game.countStones(1)
    return "Black Territory: " + str(blackTerritoryPoints) \
           + "\nBlack Stones: " + str(blackStonePoints) \
           + "\nBlack Points: " + str(blackTerritoryPoints + blackStonePoints) \
           + "\n" + "\nWhite Territory: " + str(whiteTerritoryPoints) \
           + "\nWhite Stones: " + str(whiteStonePoints) + "\nWhite Points: " \
           + str(whiteTerritoryPoints + whiteStonePoints + 7.5) + "\n"


def makeBoardString(board):
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
    return line


def makeMove(game, x, y):
    posX = -1
    posY = -1
    while posX < 1 or posX > game.getCurrentBoard().rowNumber - 1 \
            or posY < 1 or posY > game.getCurrentBoard().rowNumber - 1:
        posX = x
        posY = y
    if not game.insertStone(posX, posY):
        return "Bad Move!"
    return "Move x = " + str(x) + " y = " + str(y)
