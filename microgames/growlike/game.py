import random


max_levels = {
    "rock": 1,
    "burrito": 2,
    "lighter": 3,
    "plungus": 4,
    "vacuum": 5,
    "charm": 6
}

current_levels = {
    "lighter": 0,
    "burrito": 0,
    "charm": 0,
    "vacuum": 0,
    "rock": 0,
    "plungus": 0,
}

is_in_play = {
    "rock": False,
    "burrito": False,
    "lighter": False,
    "plungus": False,
    "vacuum": False,
    "charm": False
}


def level_up():
    for key, value in is_in_play.items():
        if value and not current_levels[key] == "M":
            current_levels[key] += 1
            if current_levels[key] == max_levels[key]:
                current_levels[key] = "M"
            print("Your %s is level %s" % (key, current_levels[key]))


def run_growlike():
    print("WELCOME TO GROWLIKE!")
    print("SELECT THE ITEMS IN THE CORRECT ORDER TO WIN!")
    print("THE GOAL IS TO GET EVERYTHING TO LEVEL M!")
    print()
    print("THE MAX LEVELS ARE THE SAME IN EVERY PLAYTHROUGH!")
    print("KEEP TRYING UNTIL YOU GET IT RIGHT!")

    amount_picked = 0

    while amount_picked < 6:
        print(current_levels)
        gain_level = False
        cmd = input("Which one would you like to start growing next?\n>>> ")

        for key, value in is_in_play.items():
            if cmd == key and not is_in_play[key]:
                amount_picked += 1
                is_in_play[key] = True
                gain_level = True

        if gain_level:
            level_up()
        else:
            print("Invalid selection.")

    # Check for win
    def check_for_win():
        for key, value in current_levels.items():
            if current_levels[key] != "M":
                return False
        return True

    print(current_levels)

    if check_for_win():
        print("YOU HAVE WON! CONGRATULATIONS!")
        return True
    else:
        print("YOU HAVE LOST THE GAME!")
        return False
