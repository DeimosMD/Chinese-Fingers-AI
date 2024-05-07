import os
import sys
from shlex import split

import jsonpickle

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
    print("bot save <save_name>        \n#saves data of current bot to disc")
    print("bot load <save_name>        \n#loads data of specified bot from disc")


class App:
    bot = Bot()


if __name__ == "__main__":
    print("\n")
    helps()
    print("\n\n")
    directory = os.path.expanduser('~') + "/.Chinese_Fingers_AI/"
    dirSaves = directory + "saves/"
    if not os.path.exists(directory):
        os.mkdir(directory)
    if not os.path.exists(dirSaves):
        os.mkdir(dirSaves)
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
                                App.bot.train(int(args[2]), args[3].lower() == "true" or args[3].lower() == "t" or args[
                                    3].lower() == "y" or args[3].lower() == "yes")
                                print("Finished training for", args[2], "games ( Total:", App.bot.totalTraining, ")")
                            else:
                                print("Invalid Argument")
                        case "data":
                            App.bot.printData()
                        case "test":
                            if len(args) == 3:
                                App.bot.test(int(args[2]), False)
                            elif len(args) == 4:
                                App.bot.test(int(args[2]), args[3].lower() == "true" or args[3].lower() == "t" or args[
                                    3].lower() == "y" or args[3].lower() == "yes")
                        case "save":
                            if len(args) == 3:
                                file = open(dirSaves + args[2] + ".json", "w")
                                file.write(jsonpickle.encode(App.bot, unpicklable=True))
                                file.close()
                                print("Successfully saved bot as '" + args[2] + "'")
                            else:
                                print("Invalid Argument")
                        case "load":
                            if len(args) == 3:
                                file = open(dirSaves + args[2] + ".json", "r")
                                App.bot = jsonpickle.decode(file.read())
                                file.close()
                                print("Successfully loaded bot from '" + args[2] + "'")
                            else:
                                print("Invalid Argument")
                        case _:
                            print("Invalid Argument")
                case _:
                    print("Invalid Argument")
