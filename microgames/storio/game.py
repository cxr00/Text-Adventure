from random import randint

cmd = []

items = [
    "plunger",
    "tea",
    "cheese",
    "wine",
    "lip balm"
]

data = {
    "credits": 50,
    "stock":
        {
            "plunger": 1,
            "tea": 3,
            "cheese": 2,
            "wine": 3,
            "lip balm": 4
        },
}

price = {
    "plunger": 10,
    "tea": 20,
    "cheese": 15,
    "wine": 25,
    "lip balm": 12
}


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


def execute_day():
    print("A customer comes into your store.")
    # Get random item
    item = items[randint(0, len(items) - 1)]
    print("'Hello, I am looking for a %s." % item)
    # Set slightly random price
    sell_price = price[item] + randint(-1, 4)
    print("I will pay %d credits for it.'\n" % sell_price)

    print("ACCEPT\tREJECT\tORDER\tSTATS\tQUIT")
    get_cmd()
    if check_cmd("accept"):
        if data["stock"][item] >= 1:
            data["stock"][item] -= 1
            data["credits"] += sell_price
            print("You sell the %s for %d credits.\n" % (item, sell_price))
            return True
        else:
            print("You do not have that item in stock")
            return True
    elif check_cmd("reject"):
        print("You reject the customer's offer.")
        return True
    elif check_cmd("order"):
        if data["credits"] > price[item]:
            data["stock"][item] += 1
            data["credits"] -= price[item]
            print("You order the %s. It is delivered right away." % item)
        else:
            print("You cannot afford the %s" % item)
        return True

    return False


def run_storio(input_data=None):
    global data
    if input_data:
        data = input_data

    end = False

    print("Welcome to Storio!")
    print("You are in charge of a general store.")
    print("Decide whether to ACCEPT customer offers on your items,")
    print("or REJECT their offers in case something better comes along.")
    print("If you don't have an item, you can ORDER one for the next customer.")
    print()

    while True:
        if not execute_day():
            if check_cmd(["quit", "exit"]):
                end = True
                print("Goodbye!")
                return data
            elif check_cmd("stats"):
                print("credits: %d" % data["credits"])
                print("ITEM STOCK:")
                for each in items:
                    print("%s: %d" % (each, data["stock"][each]))
                print()
            else:
                print("I don't understand %s." % " ".join(cmd))
        if data["credits"] > 260:
            end = True
            print("You have earned 260 credits.")
            print("Congratulations! You have won the game.")
            return data
