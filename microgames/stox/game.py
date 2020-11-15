from random import randint, random
from math import ceil

cmd = []
stonk = ["cxr", "vlt", "zot", "nem"]

data = {
    "credits": 100.00,
    "stox":
        {
            "cxr": 0,
            "vlt": 0,
            "zot": 0,
            "nem": 0
        },
    "day price":
        {
            "cxr": 10,
            "vlt": 10,
            "zot": 10,
            "nem": 10
        },
    "previous day price":
        {
            "cxr": 0,
            "vlt": 0,
            "zot": 0,
            "nem": 0
        }
}


def reset_data():
    global data
    data["credits"] = 100.00
    for each in stonk:
        data["stox"][each] = 0
        data["day price"][each] = 10
        data["previous day price"][each] = 0


def round_everything():
    global data
    data["credits"] = round(data["credits"], 1)
    for each in stonk:
        data["stox"][each] = round(data["stox"][each], 1)
        data["day price"][each] = round(data["day price"][each], 1)
        data["previous day price"][each] = round(data["previous day price"][each], 1)


def get_cmd():
    """
    Takes input and converts it into an array command
    """
    global cmd
    cmd = [e.lower() for e in input(">>> ").split(" ")]


def check_cmd(*args):
    """
    Determines if command matches args

    :param args: To match to the command
    :return: Whether args matches command
    """

    def arg_matches_cmd(n):
        # Synonym engine
        # Returns False if there is not at least one match
        if isinstance(args[n], list):
            if not cmd[n] in args[n]:
                return False
        elif cmd[n] != args[n].lower():
            return False
        return True

    # If the command is not at least as long as the args, it is obviously False
    if len(cmd) < len(args):
        return False

    n = 0
    while n < len(args):
        if not arg_matches_cmd(n):
            return False
        n += 1

    return True


def process_day():
    for each in stonk:
        data["previous day price"][each] = data["day price"][each]
        positive = True if random() < .5 else False
        stonk_change = ceil(random() * 10) / 10 + randint(0, 5)
        if stonk_change > data["day price"][each]:
            data["day price"][each] += stonk_change
        else:
            data["day price"][each] += stonk_change * (1 if positive else -1)
        data["day price"][each] = data["day price"][each]


def show_stats():
    print("your credits:", data["credits"])
    for each in stonk:
        print(each, end=" :: ")
        print(data["stox"][each], end=" :: ")
        print(data["day price"][each], end=" :: ")
        day_difference = round(data["day price"][each] - data["previous day price"][each], 1)
        positive = True if (day_difference > 0) else False
        print(("+" if positive else "") + str(day_difference))


def check_buy():
    if check_cmd("buy"):
        try:
            buy_stock = cmd[1]
        except IndexError:
            print("Which stox you want to buy?")
            return False
        valid_stock = False
        for each in stonk:
            if buy_stock == each:
                valid_stock = True

        if not valid_stock:
            print("%s is not a valid stox" % buy_stock)
            return False

        try:
            amount = int(cmd[2])
        except IndexError:
            print("What number of stox do you want to buy?")
            return False
        except ValueError:
            print("%s is not a number. What number of stox do you want to buy?")
            return False

        if data["credits"] < amount * data["day price"][buy_stock]:
            print("You cannot afford that many %s stox" % buy_stock)
            return False

        data["credits"] -= amount * data["day price"][buy_stock]
        data["credits"] = ceil(data["credits"] * 10) / 10
        data["stox"][buy_stock] += amount
        return True


def check_sell():
    if check_cmd("sell"):
        try:
            sell_stock = cmd[1]
        except IndexError:
            print("Which stox you want to sell?")
            return False
        valid_stock = False
        for each in stonk:
            if sell_stock == each:
                valid_stock = True

        if not valid_stock:
            print("%s is not a valid stox" % sell_stock)
            return False

        try:
            amount = int(cmd[2])
        except IndexError:
            print("What number of stox do you want to sell?")
            return False
        except ValueError:
            print("%s is not a number.\nWhat number of stox do you want to sell?")
            return False

        if data["stox"][sell_stock] < amount:
            print("You do not have that many %s stox to sell" % sell_stock)
            return False

        data["credits"] += amount * data["day price"][sell_stock]
        data["credits"] = ceil(data["credits"] * 10) / 10
        data["stox"][sell_stock] -= amount
        return True


def run_stox(input_data=None):
    global data
    if input_data:
        data = input_data

    process_day()

    end = False

    while not end:
        valid_command = False
        round_everything()
        show_stats()
        print("HELP\tBUY/SELL:\t\tCXR\tVLT\tZOT\tNEM")
        get_cmd()

        if check_cmd("help"):
            print("Buy more stox or sell the stox you have.")
            print("For example, type 'buy cxr 3' or 'sell nem 2'")
            print("You can only buy stox you can afford,")
            print("and you can only sell stox you have.")
            print("Achieve 200.00 credits to win the game!")
        if check_buy():
            print("You buy %s %s stox." % (cmd[2], cmd[1]))
            valid_command = True
        elif check_sell():
            print("You sell %s %s stox." % (cmd[2], cmd[1]))
            valid_command = True
        elif check_cmd("reset"):
            confirm = input("Are you sure you want to reset? [y/n]")
            if confirm[0].lower() == "y":
                reset_data()
        elif check_cmd(["quit", "exit"]):
            print("Goodbye!")
            return data
        elif check_cmd("debug"):
            data["credits"] += 100
        else:
            print("I don't understand %s" % " ".join(cmd))

        if valid_command:
            process_day()

        if data["credits"] >= 200:
            print("You have achieved 200.00 credits!")
            print("Congratulations! You have won the game.")
            return data
