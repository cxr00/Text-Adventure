from random import shuffle
from enum import Enum

words = [
    "sensplicious",
    "boggerty",
    "heteroscedasticity",
    "palilalia",
    "screamnastic",
    "complexor"

]


def run_vocabuloid():
    strikes = 0
    test = words
    shuffle(test)

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
        print("You have won the game!")
        print("Goodbye.")
        return True
    if strikes >= 2:
        print("You have lost the game!")
        print("Goodbye.")
        return False

    # If it somehow gets here, the default return value is False
    return False
