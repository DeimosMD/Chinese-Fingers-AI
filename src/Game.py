import string


class Game:

    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()
        self.currentPlayer = self.p1
        self.concurrentPlayer = self.p2

    def getOptions(self):
        options = []
        if self.currentPlayer.handOne == 0 and self.currentPlayer.handTwo != 0 and self.currentPlayer.handTwo % 2 == 0:
            options.append("BUMP")
        elif self.currentPlayer.handTwo == 0 and self.currentPlayer.handOne != 0 and self.currentPlayer.handOne % 2 == 0:
            options.append("BUMP")
        if self.currentPlayer.handOne != 0:
            if self.concurrentPlayer.handOne != 0:
                options.append("ONE-ONE")
            if self.concurrentPlayer.handTwo != 0:
                options.append("ONE-TWO")
        if self.currentPlayer.handTwo != 0:
            if self.concurrentPlayer.handOne != 0:
                options.append("TWO-ONE")
            if self.concurrentPlayer.handTwo != 0:
                options.append("TWO-TWO")
        return options

    # Attempts to play move provided and return true, if move is illegal then returns false
    def playMove(self, move: string):
        if move in self.getOptions():
            match move:
                case "BUMP":
                    if self.currentPlayer.handOne == 0:
                        n = self.currentPlayer.handTwo / 2
                        self.currentPlayer.handOne = n
                        self.currentPlayer.handTwo = n
                    elif self.currentPlayer.handTwo == 0:
                        n = self.currentPlayer.handOne / 2
                        self.currentPlayer.handOne = n
                        self.currentPlayer.handTwo = n
                case "ONE-ONE":
                    self.concurrentPlayer.handOne += self.currentPlayer.handOne
                case "ONE-TWO":
                    self.concurrentPlayer.handTwo += self.currentPlayer.handOne
                case "TWO-ONE":
                    self.concurrentPlayer.handOne += self.currentPlayer.handTwo
                case "TWO-TWO":
                    self.concurrentPlayer.handTwo += self.currentPlayer.handTwo
            if self.concurrentPlayer.handOne >= 5:
                self.concurrentPlayer.handOne = 0
            if self.concurrentPlayer.handTwo >= 5:
                self.concurrentPlayer.handTwo = 0

            # switches which player is the current player
            if self.p1cur():
                self.currentPlayer = self.p2
                self.concurrentPlayer = self.p1
            else:
                self.currentPlayer = self.p1
                self.concurrentPlayer = self.p2
            return True
        return False

    # Checks if the game should be over
    # returns 1 or 2 depending on the player that has won if is over
    def checkOver(self):
        if self.p1.handOne == 0 and self.p1.handTwo == 0:
            return 2
        if self.p2.handOne == 0 and self.p2.handTwo == 0:
            return 1
        return 0

    def printHands(self):
        def getHandString(num):
            n = int(num)
            s = " "
            for i in range(n):
                s += "|"
            for i in range(5-n):
                s += "."
            return s

        def printPlayerOne():
            print("Player One:", getHandString(self.p1.handOne), getHandString(self.p1.handTwo))

        def printPlayerTwo():
            print("Player Two:", getHandString(self.p2.handOne), getHandString(self.p2.handTwo))

        if self.p1cur():
            printPlayerTwo()
            printPlayerOne()
        else:
            printPlayerOne()
            printPlayerTwo()

    def getCurrentPlayerAsString(self):
        if self.p1cur():
            return "Player One"
        return "Player Two"

    # returns true if p1 is currentPlayer, returns false if p2 is current player
    def p1cur(self):
        return self.currentPlayer == self.p1

    def toList(self) -> tuple[int, int, int, int]:
        if self.p1cur():
            return (
                self.p1.handOne,
                self.p1.handTwo,
                self.p2.handOne,
                self.p2.handTwo
            )
        else:
            return (
                self.p2.handOne,
                self.p2.handTwo,
                self.p1.handOne,
                self.p1.handTwo
            )


class Player:

    def __init__(self):
        self.handOne = 1
        self.handTwo = 1
