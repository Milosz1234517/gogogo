from gameEngine import rock as r
import numpy as np


class Board:

    def __init__(self, rows, columns):
        self.rowNumber = rows + 2
        self.columnNumber = columns + 2
        self.matrix = np.ndarray(shape=(self.rowNumber, self.columnNumber), dtype=r.Rock)
        self.setBoard()

    def setBoard(self):
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if i == 0 or j == 0 or i == self.rowNumber - 1 or j == self.columnNumber - 1:
                    self.matrix[i, j] = r.Rock(i, j, 3)
                else:
                    self.matrix[i, j] = r.Rock(i, j, 0)
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if i != 0 and j != 0 and i != self.rowNumber - 1 and j != self.columnNumber - 1:
                    self.matrix[i, j].setNeighbours(self.matrix[i - 1, j], self.matrix[i + 1, j],
                                                    self.matrix[i, j + 1], self.matrix[i, j - 1])

    def resetBoard(self):
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if i == 0 or j == 0 or i == self.rowNumber - 1 or j == self.columnNumber - 1:
                    self.matrix[i, j].setColour(3)
                else:
                    self.makeEmpty(i, j)

    def getRock(self, x, y):
        return self.matrix[x, y]

    def setRock(self, x, y, colour):
        self.matrix[x, y].setColour(colour)

    def makeEmpty(self, x, y):
        self.matrix[x, y].stoneColour = 0
