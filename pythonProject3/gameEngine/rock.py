class Rock:
    def __init__(self, posX, posY, colour):
        self.row = posX
        self.column = posY
        self.stoneColour = colour
        self.neighbours = []

    def setColour(self, colour):
        self.stoneColour = colour

    def setNeighbours(self, nN, nS, nW, nE):
        self.neighbours.append(nN)
        self.neighbours.append(nS)
        self.neighbours.append(nE)
        self.neighbours.append(nW)
