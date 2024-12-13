import os
import sys
from shlex import split

from Bot import Bot
from Game import Game


def helps():
    print("Commands:\n")
    print("help         \n#prints this command list")
    print("exit         \n#exits program")
    print("play person-person         \n#starts a game of person versus person")
    print("play bot-bot         \n#starts a game of bot versus bot")
    print("play person-bot         \n#starts a game of bot versus person where the person moves first")
    print("play bot-person         \n#starts a game of bot versus person where the bot moves first")
    print(
        "bot train <game_num> [<verbose (write true or false; default false)>]         \n#trains bot for a certain amount of games")
    print(
        "bot test <game_num> [<verbose (write true or false; default false)>]         \n#tests bot against an untrained bot for a certain amount of games and returns results")
    print("bot reset         \n#resets the bot")
    print("bot data         \n#prints out the bots long-term memory")


def meansTrue(s) -> bool:
    lower = s.lower()
    return lower == "true" or lower == "t" or lower == "y" or lower == "yes"


class App:
    bot = Bot()


if __name__ == "__main__":
    print("\n")
    helps()
    print("\n\n")
    while True:
        args = split(input("> ").lower())
        if len(args) > 0:
            match args[0]:
                case "exit":
                    sys.exit(0)
                case "help":
                    helps()
                case "play":
                    match args[1]:
                        case "person-person":
                            game = Game()
                            print("------------------------| GAME STARTED |------------------------")
                            while game.checkOver() == 0:
                                game.printHands()
                                print("Options: ", game.getOptions())
                                while not game.playMove(input(game.getCurrentPlayerAsString() + ": ").upper()):
                                    print("Illegal move | Try again")
                            game.printHands()
                            if game.checkOver() == 1:
                                print("Player One has won!")
                            else:
                                print("Player Two has won!")
                        case "bot-bot":
                            bot2 = Bot()
                            bot2.longTermMemory = App.bot.longTermMemory.copy()
                            Bot.play(App.bot, bot2, True)
                        case "person-bot":
                            game = Game()
                            print("------------------------| GAME STARTED |------------------------")
                            while game.checkOver() == 0:
                                game.printHands()
                                print("Options: ", game.getOptions())
                                if game.p1cur():
                                    while not game.playMove(input(game.getCurrentPlayerAsString() + ": ").upper()):
                                        print("Illegal move | Try again")
                                else:
                                    App.bot.move(game, True)
                            game.printHands()
                            if game.checkOver() == 1:
                                print("Player One has won!")
                            else:
                                print("Player Two has won!")
                        case "bot-person":
                            game = Game()
                            print("------------------------| GAME STARTED |------------------------")
                            while game.checkOver() == 0:
                                game.printHands()
                                print("Options: ", game.getOptions())
                                if game.p1cur():
                                    App.bot.move(game, True)
                                else:
                                    while not game.playMove(input(game.getCurrentPlayerAsString() + ": ").upper()):
                                        print("Illegal move | Try again")
                            game.printHands()
                            if game.checkOver() == 1:
                                print("Player One has won!")
                            else:
                                print("Player Two has won!")
                        case _:
                            print("Invalid Argument")
                case "bot":
                    match args[1]:
                        case "reset":
                            App.bot = Bot()
                            print("Bot has been reset")
                        case "train":
                            if len(args) == 3:
                                App.bot.train(int(args[2]), False)
                                print("Finished training for", args[2], "games ( Total:", App.bot.totalTraining, ")")
                            elif len(args) == 4:
                                App.bot.train(int(args[2]), meansTrue(args[3]))
                                print("Finished training for", args[2], "games ( Total:", App.bot.totalTraining, ")")
                            else:
                                print("Invalid Argument")
                        case "data":
                            App.bot.printData()
                        case "test":
                            if len(args) == 3:
                                App.bot.test(int(args[2]), False)
                            elif len(args) == 4:
                                App.bot.test(int(args[2]), meansTrue(args[3]))
                            else:
                                print("Invalid Argument")
                        case _:
                            print("Invalid Argument")
                case _:
                    print("Invalid Argument")
