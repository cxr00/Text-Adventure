from random import randint
from enum import Enum

cmd = []


class Menu(Enum):

    START = "start"
    ACTION = "action"
    SHOP = "shop"
    FIGHT = "fight"
    BATTLE = "battle"


class Player:
    data = {
        "max health": 5,
        "current health": 5,
        "weapon": 2,
        "armor": 0,
        "accessory": 2,
        "credits": 1,
        "points": 0
    }

    # Player's current menu
    MENU = Menu.START

    @staticmethod
    def reset():
        Player.data = {
            "max health": 5,
            "current health": 5,
            "weapon": 2,
            "armor": 0,
            "accessory": 2,
            "credits": 1,
            "points": Player.data["points"]
        }

        Player.MENU = Menu.START

    @staticmethod
    def change_menu(menu: Menu):
        Player.MENU = menu

    @staticmethod
    def get_stats():
        out = "HEALTH: %s / %s\n" % (str(Player.data["current health"]), str(Player.data["max health"]))
        out += "WEAPON: %s\n" % str(Player.data["weapon"])
        out += "ARMOR: %s\n" % str(Player.data["armor"])
        out += "ACCESSORY: %s\n" % str(Player.data["accessory"])
        out += "CREDITS: %s\n" % str(Player.data["credits"])
        out += "POINTS: %s" % str(Player.data["points"])
        return out

    @staticmethod
    def heal():
        Player.data["current health"] = Player.data["max health"]


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


def start_menu():
    if check_cmd("start"):
        Player.change_menu(Menu.ACTION)
    elif check_cmd("points"):
        print("You have earned %s points." % str(Player.data["points"]))
    elif check_cmd("about"):
        print("Welcome to RatFighter 21XX.")
        print("Your task is to FIGHT rats and upgrade your stats in the SHOP.")
        print("Keep an eye on your health, and make sure to HEAL often!")
        print("Your weapon determines how much damage you deal.")
        print("Your armor determines how much less damage you take.")
        print("Your accessory determines how many credits you get for defeating a rat.")
        print("Good luck! Begin the game by saying 'start' at the main menu!")
    elif check_cmd("reset"):
        are_you_sure = input("Are you sure? This will delete your progress. (y/n) >>> ")
        if are_you_sure[0] == "y":
            Player.reset()


def action_menu():
    if check_cmd("fight"):
        Player.change_menu(Menu.FIGHT)
        return True
    elif check_cmd("shop"):
        Player.change_menu(Menu.SHOP)
        return True
    elif check_cmd("stats"):
        print(Player.get_stats())
        return True
    elif check_cmd("quit"):
        Player.change_menu(Menu.START)
        return True


def shop_menu():
    if check_cmd("upgrade", ["health", "hp"]) or check_cmd(["health", "hp"]):
        if Player.data["credits"] >= 3:
            Player.data["credits"] -= 3
            Player.data["max health"] += 1
            Player.heal()
            print("You upgrade your health. You are also fully healed.")
        else:
            print("You cannot afford to upgrade your health.")
        return True
    elif check_cmd("upgrade", "weapon") or check_cmd("weapon"):
        if Player.data["credits"] >= 5:
            Player.data["credits"] -= 5
            Player.data["weapon"] += 1
            print("You upgrade your weapon.")
        else:
            print("You cannot afford to upgrade your weapon.")
        return True
    elif check_cmd("upgrade", "armor") or check_cmd("armor"):
        if Player.data["credits"] >= 3:
            Player.data["credits"] -= 3
            Player.data["armor"] += 1
            print("You upgrade your armor.")
        else:
            print("You cannot afford to upgrade your armor")
        return True
    elif check_cmd("upgrade", ["accessory", "acc"]) or check_cmd(["accessory", "acc"]):
        if Player.data["credits"] >= 2:
            Player.data["credits"] -= 2
            Player.data["accessory"] += 1
            print("You upgrade your accessory.")
        else:
            print("You cannot afford to upgrade your accessory.")
        return True
    elif check_cmd("heal"):
        if Player.data["credits"] >= 1:
            if Player.data["current health"] == Player.data["max health"]:
                print("You do not need to be healed right now.")
            else:
                Player.data["credits"] -= 1
                Player.heal()
                print("Your health has been restored.")
        else:
            print("You cannot afford to upgrade your health")
        return True

    elif check_cmd(["leave", "exit"]):
        Player.change_menu(Menu.ACTION)
        return True

    return False


def fight_menu():
    if check_cmd(["l1", "1"]):
        battle("sewer rat", 5, 1, 0, 1)
        return True
    elif check_cmd(["l2", "2"]):
        battle("dire rat", 9, 2, 1, 2)
        return True
    elif check_cmd(["l3", "3"]):
        battle("forest rat", 15, 4, 2, 3)
        return True
    elif check_cmd(["l4", "4"]):
        battle("wererat", 25, 7, 4, 5)
        return True
    elif check_cmd(["l5", "5"]):
        battle("cyborg rat", 40, 12, 7, 8)
        return True
    elif check_cmd(["quit", "leave"]):
        Player.change_menu(Menu.ACTION)
        return True


# Rat stats are in this order: health, damage, armor, payout
def battle(*rat_stats):
    rat_name = rat_stats[0]
    rat_max_health = rat_stats[1]
    rat_current_health = rat_stats[1]
    rat_damage = rat_stats[2]
    rat_armor = rat_stats[3]
    rat_payout = rat_stats[4]

    print("You are now in a FIGHT with a %s!" % rat_name)

    while Player.data["current health"] > 0 and rat_current_health > 0:
        print("FIGHT\tSTATS\tENEMY\tFLEE")
        get_cmd()
        if check_cmd(["fight", "attack"]):
            rat_current_health -= Player.data["weapon"] - rat_armor
            print("You hit the rat for %s damage." % str(Player.data["weapon"] - rat_armor))
            if rat_current_health <= 0:
                credit_payout = randint(1, Player.data["accessory"]) + rat_payout
                Player.data["credits"] += credit_payout
                Player.data["points"] += rat_payout
                print("You have defeated the %s!" % rat_name)
                print("You gained %s credits and %s points!" % (credit_payout, rat_payout))
                Player.change_menu(Menu.ACTION)
                return True
            else:
                Player.data["current health"] -= rat_damage - Player.data["armor"]
                print("The %s hits you for %s damage." % (rat_name, str(rat_damage - Player.data["armor"])))
                if Player.data["current health"] <= 0:
                    print("You have been defeated!")
                    print("Your progress will be reset.")
                    Player.reset()
                    Player.change_menu(Menu.START)
                    return True
        elif check_cmd("stats"):
            print(Player.get_stats())
        elif check_cmd("enemy"):
            print(rat_name)
            print("HEALTH: %s / %s" % (str(rat_current_health), str(rat_max_health)))
            print("DAMAGE: " + str(rat_damage))
            print("ARMOR: " + str(rat_armor))
            print("CREDITS: " + str(rat_payout))
        elif check_cmd("flee"):
            print("You run away from the %s." % rat_name)
            Player.change_menu(Menu.ACTION)
            return True

    return True


def run_ratfighter_21xx(data=None):
    if data:
        Player.data = data
    end = False

    while not end:
        if Player.MENU == Menu.START:
            print("MAIN MENU")
            print("START\tPOINTS\tABOUT\tRESET\tQUIT")
            get_cmd()
            if check_cmd("quit"):
                end = True
                print("GOODBYE!")
            else:
                start_menu()
        elif Player.MENU == Menu.ACTION:
            print("ACTION MENU")
            print("FIGHT\tSHOP\tSTATS\tQUIT")
            get_cmd()
            action_menu()
        elif Player.MENU == Menu.FIGHT:
            print("Select a rat LEVEL:")
            print("L1: Sewer rat")
            print("L2: Dire rat")
            print("L3: Forest rat")
            print("L4: Wererat")
            print("L5: Cyborg rat")
            get_cmd()
            fight_menu()
        elif Player.MENU == Menu.SHOP:
            print("You have %s credits to spend." % str(Player.data["credits"]))
            print("SHOP UPGRADES:")
            print("HEALTH: 3 credits")
            print("WEAPON: 5 credits")
            print("ARMOR: 3 credits")
            print("ACCESSORY: 2 credits")
            print("HEAL: 1 credit")
            print("Decide what to UPGRADE or LEAVE this menu")
            get_cmd()
            shop_menu()

    return Player.data
