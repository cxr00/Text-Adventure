from random import shuffle
from enum import Enum
from copy import deepcopy
from time import time

words = [
    "sensplicious",
    "boggerty",
    "heteroscedasticity",
    "palilalia",
    "screamnastic",
    "complexor",
    "dioxyribonucleic",
    "conflagration",
    "grugnalious",
    "pasghetti",
    "indruxtable",
    "gerrymandering",
    "antediluvian",
    "grandiloquent",
    "infratumescent",
    "zjinkonnerism",
    "pavlovically",
    "disembuttholed"
]


def run_vocabuloid(best_time):
    strikes = 0
    test = deepcopy(words)
    shuffle(test)
    start_time = time()

    print("Welcome to Vocabuloid!")
    print("Type the words as they appear on screen.")
    print("You LOSE if you make two mistakes.")
    while not (len(test) == 0 or strikes >= 2):
        # Select the next word
        challenge = test.pop(0)
        # Get user's attempt
        attempt = input(challenge + " >>> ")
        if challenge != attempt:
            strikes += 1
            print("WRONG!")

    if len(test) == 0:
        game_time = round(time() - start_time, 2)
        print("You have won the game!")
        print("Your time was %s seconds" % str(game_time))
        if strikes > 0:
            game_time += strikes * 5
            print("Plus 5 seconds for your strike.")
        print("Your final time is %s seconds." % str(game_time))
        if game_time < best_time or best_time == 0:
            print("NEW RECORD!")
        print("Goodbye.")
        return game_time
    if strikes >= 2:
        print("You have lost the game!")
        print("Goodbye.")
        return False

    # If it somehow gets here, the default return value is False
    return False
