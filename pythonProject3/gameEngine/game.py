from gameEngine import board as b


class Game:

    def __init__(self, rows, columns, gameID, player1Nick):
        self.isOngoing = 1
        self.blackStonesSet = 0
        self.whiteStonesSet = 0

        self.gameID = gameID
        self.player1Nick = player1Nick
        self.player2Nick = ""
        self.started = False
        self.rows = rows
        self.columns = columns
        self.board = b.Board(rows, columns)
        self.toKill = set()
        self.koRock = None
        self.turn = 2
        self.passCounter = 0

    def getCurrentBoard(self):
        return self.board

    def setTurn(self, turn):
        self.turn = turn

    def getTurn(self):
        return self.turn

    def checkNoBreath(self, rock):
        toCheck = set()
        for neighbour in rock.neighbours:
            if neighbour in self.toKill:
                continue
            if neighbour.stoneColour == 0:
                self.toKill.clear()
                return False
            elif neighbour.stoneColour == rock.stoneColour:
                toCheck.add(neighbour)
        self.toKill.add(rock)
        for rockCheck in toCheck:
            if not self.checkNoBreath(rockCheck):
                return False
        return True

    def checkTerritoryForPoints(self, rock, oponentColor, points, used):
        checkPoint = set()
        for neighbour in rock.neighbours:
            if neighbour in points:
                continue
            if neighbour.stoneColour == oponentColor:
                points.clear()
                return False
            elif neighbour.stoneColour == rock.stoneColour:
                checkPoint.add(neighbour)
        points.add(rock)
        used.add(rock)
        for rockCheck in checkPoint:
            if not self.checkTerritoryForPoints(rockCheck, oponentColor, points, used):
                return False
        return True

    def getTerritoryPoints(self, oponentColor):
        points = 0
        used = set()
        pointsList = set()
        for i in range(self.board.rowNumber):
            for j in range(self.board.columnNumber):
                if self.board.matrix[i, j].stoneColour == 0 and self.board.matrix[i, j] not in used:
                    self.checkTerritoryForPoints(self.board.matrix[i, j], oponentColor, pointsList, used)
                    points += len(pointsList)
                    pointsList.clear()
        if points == self.rows * self.columns:
            points = 0
        return points

    def passTurn(self):
        self.changeTour()
        self.passCounter += 1
        if self.passCounter >= 2:
            return True
        else:
            return False

    def insertStone(self, x, y):
        if self.checkValidPositionForInsert(x, y):
            self.board.setRock(x, y, self.turn)
            self.changeTour()
            self.killStones(self.turn)
            if not self.checkSuicide(x, y):
                self.board.makeEmpty(x, y)
                self.changeTour()
                return False
            if self.board.matrix[x, y].stoneColour == 1:
                self.whiteStonesSet += 1
            elif self.board.matrix[x, y].stoneColour == 2:
                self.blackStonesSet += 1
            self.passCounter = 0

            return True
        else:
            return False

    def removeStone(self, row, column):
        if self.checkValidPositionForRemove(row, column):
            self.board.makeEmpty(row, column)
            self.changeTour()
            self.passCounter = 0
            return True
        else:
            return False

    def checkValidPositionForInsert(self, x, y):
        if self.board.getRock(x, y).stoneColour != 0:
            return False
        elif self.koRock is not None:
            if self.koRock.row == x and self.koRock.column == y:
                self.board.setRock(x, y, self.turn)
                count = 0
                for n in self.board.matrix[x, y].neighbours:
                    if self.checkNoBreath(n):
                        if len(self.toKill) == 1:
                            count += 1
                        else:
                            count = 0
                            break
                self.board.makeEmpty(x, y)
                if count == 1:
                    return False
            self.koRock = None
            return True
        else:
            return True

    def checkValidPositionForRemove(self, x, y):
        if self.board.getRock(x, y).stoneColour == 1 or self.board.getRock(x, y).stoneColour == 2:
            return True
        else:
            return False

    def checkSuicide(self, x, y):
        if self.checkNoBreath(self.board.matrix[x, y]):
            return False
        else:
            return True

    def killStones(self, colorToKill):
        for i in range(self.board.rowNumber):
            for j in range(self.board.columnNumber):
                if self.board.matrix[i, j].stoneColour == colorToKill:
                    self.checkNoBreath(self.board.matrix[i, j])
                    for rock in self.toKill:
                        if len(self.toKill) == 1:
                            self.koRock = rock
                        self.board.makeEmpty(rock.row, rock.column)
                    self.toKill.clear()

    def changeTour(self):
        if self.turn == 2:
            self.turn = 1
        elif self.turn == 1:
            self.turn = 2

    def countStones(self, color):
        count = 0
        for i in range(self.board.rowNumber):
            for j in range(self.board.columnNumber):
                if self.board.matrix[i, j].stoneColour == color:
                    count += 1
        return count
