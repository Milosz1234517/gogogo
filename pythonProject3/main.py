from gameEngine import game as g
import os


posX = -1
posY = -1
game = g.Game(9, 9, None, None)


def showBoard(board):
    numberInZeroRow = 1
    numberInZeroColumn = 1
    numberInLastRow = 1
    numberInLastColumn = 1
    for i in range(board.rowNumber):
        line = ""
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
        print(line)


def showPoints():
    blackTerritoryPoints = game.getTerritoryPoints(1)
    whiteTerritoryPoints = game.getTerritoryPoints(2)
    blackStonePoints = game.countStones(2)
    whiteStonePoints = game.countStones(1)
    print("\nBlack Territory: " + str(blackTerritoryPoints))
    print("Black Stones: " + str(blackStonePoints))
    print("Black Points: " + str(blackTerritoryPoints + blackStonePoints) + "\n")
    print("White Territory: " + str(whiteTerritoryPoints))
    print("White Stones: " + str(whiteStonePoints))
    print("White Points: " + str(whiteTerritoryPoints + whiteStonePoints + 7.5) + "\n")


def insertCoordinates():
    game.posX = -1
    game.posY = -1
    while game.posX < 1 or game.posX > game.getCurrentBoard().rowNumber - 1 \
            or game.posY < 1 or game.posY > game.getCurrentBoard().rowNumber - 1:
        game.posX = int(input("Insert X:\n"))
        game.posY = int(input("Insert Y\n"))
    if not game.insertStone(game.posX, game.posY):
        print("Bad Move!")


def inGameMenu():
    showBoard(game.getCurrentBoard())
    showPoints()
    if game.getTurn() == 2:
        player = "Black"
    else:
        player = "White"
    print(player + " Player Turn\n")
    choice = int(input("1.Insert Stone\n2.Pass\n"))
    if choice == 1:
        insertCoordinates()
    elif choice == 2:
        if game.passTurn():
            return True
    return False


def endGameMenu():
    choice = -1
    while choice != 2:
        showBoard(game.getCurrentBoard())
        showPoints()
        choice = int(input("1.Delete Stones\n2.End\n"))
        if choice == 1:
            insertCoordinates()
    showBoard(game.getCurrentBoard())
    showPoints()
    os.system("pause")
    game.setTurn(2)
    game.passCounter = 0


def mainMenu():
    while True:
        choice = int(input("1.New Game\n2.Load From File\n3.Quit\n"))
        if choice == 1:
            game.getCurrentBoard().resetBoard()
            game.setTurn(2)
            while True:
                if inGameMenu():
                    break
            endGameMenu()
        elif choice == 2:
            readGameStateFromFile("data.txt")
            while True:
                if inGameMenu():
                    break
            endGameMenu()
        elif choice == 3:
            break


def readGameStateFromFile(pathToFile):
    game.getCurrentBoard().resetBoard()
    file = open(pathToFile, "r")
    for s in file:
        r = s.split(",")
        game.getCurrentBoard().setRock(int(r[0]), int(r[1]), int(r[2]))


if __name__ == '__main__':
    mainMenu()
