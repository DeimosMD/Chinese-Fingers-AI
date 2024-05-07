import math
import random
import string

from Game import Game


class MemUnit:

    def __init__(self, options):
        self.preferredMove = MemUnit.randMove(options)
        self.reinforcements: dict[int, string] = {}
        for s in options:
            self.reinforcements[s] = 0

    @staticmethod
    def randMove(options) -> string:
        return options[random.randint(0, len(options) - 1)]


class Bot:
    maxMovesInTrainingGame = 50

    def __init__(self):
        self.longTermMemory: dict[tuple[int, int, int, int], MemUnit] = {
            (1, 1, 1, 1): MemUnit(Game().getOptions())
        }
        self.shortTermMemory: dict[tuple[int, int, int, int], string] = {}
        self.totalTraining = 0
        self.mutating = False

    def move(self, game: Game, verbose: bool):
        p = game.getCurrentPlayerAsString()
        if game.toList() in self.longTermMemory:
            if self.mutating:
                k = game.toList()
                r = self.longTermMemory[k].reinforcements[self.longTermMemory[k].preferredMove]
                if r < 1:
                    r = 1
                r = math.ceil(math.sqrt(r))
                if random.randint(0, r) == 0:
                    self.longTermMemory[k].preferredMove = MemUnit.randMove(game.getOptions())
        else:
            # picks random move out of options to fill blank element in long term memory
            self.longTermMemory[game.toList()] = MemUnit(game.getOptions())
        move = self.longTermMemory[game.toList()].preferredMove
        self.shortTermMemory[game.toList()] = move
        # plays move from long term memory
        game.playMove(move)
        if verbose:
            print(p + ": ", move)

    @staticmethod
    def play(bot1, bot2, verbose: bool):
        bot1.shortTermMemory, bot2.shortTermMemory = {}, {}
        game = Game()
        if verbose:
            print("------------------------| GAME STARTED |------------------------")
            game.printHands()
        currentPlayer = bot1
        i = 0
        while game.checkOver() == 0:
            i += 1
            if i == Bot.maxMovesInTrainingGame:
                if verbose:
                    print("Game has reached", str(Bot.maxMovesInTrainingGame), "moves and ended in a draw")
                return -1
            if verbose:
                print("Options: ", game.getOptions())
            currentPlayer.move(game, verbose)
            # Switches out current player
            if currentPlayer == bot1:
                currentPlayer = bot2
            else:
                currentPlayer = bot1
            if verbose:
                game.printHands()
        if verbose:
            if game.checkOver() == 1:
                print("Player One has won!")
            else:
                print("Player Two has won!")
        return game.checkOver()

    def reinforceShortTermMemory(self, opp):
        for longSit in self.longTermMemory:
            for shortSit in self.shortTermMemory:
                if shortSit == longSit:
                    for i, enumeratedSit in enumerate(self.shortTermMemory.keys()):
                        if enumeratedSit == shortSit:
                            self.longTermMemory[longSit].reinforcements[self.shortTermMemory[shortSit]] += i + 1
                            break
            for shortSit in opp.shortTermMemory:
                if shortSit == longSit:
                    for i, enumeratedSit in enumerate(opp.shortTermMemory.keys()):
                        if enumeratedSit == shortSit:
                            self.longTermMemory[longSit].reinforcements[opp.shortTermMemory[shortSit]] -= i + 1
                            break

    def train(self, gameNum: int, verbose: bool):
        for i in range(gameNum):
            opp = Bot()
            opp.longTermMemory = self.longTermMemory.copy()
            opp.mutating = True
            if i % 2 == 0:
                match Bot.play(self, opp, verbose):
                    case -1:
                        self.longTermMemory = opp.longTermMemory.copy()
                    case 1:
                        self.reinforceShortTermMemory(opp)
                    case 2:
                        self.longTermMemory = opp.longTermMemory.copy()
            else:
                match Bot.play(opp, self, verbose):
                    case -1:
                        self.longTermMemory = opp.longTermMemory.copy()
                    case 2:
                        self.reinforceShortTermMemory(opp)
                    case 1:
                        self.longTermMemory = opp.longTermMemory.copy()
            self.totalTraining += 1

    def printData(self):
        for k in self.longTermMemory:
            print(k, self.longTermMemory[k].preferredMove, self.longTermMemory[k].reinforcements)

    def test(self, gameNum: int, verbose: bool):
        w = 0
        for i in range(gameNum):
            if i % 2 == 0:
                if Bot.play(self, Bot(), verbose) == 1:
                    w += 1
            else:
                if Bot.play(Bot(), self, verbose) == 2:
                    w += 1
        print("The bot won", str((w / gameNum) * 100) + "%", "of the time in", str(gameNum),
              "games against an untrained bot, with", str(self.totalTraining), "games of prior training.")
        print("Specifically", w, "wins and", str(gameNum - w), "losses")
