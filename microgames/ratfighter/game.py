from microgames.ratfighter.enums import Menu
from microgames.ratfighter.player import Player


cmd = []


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
        print("You have earned %s points." % str(Player.POINTS))
    elif check_cmd("reset"):
        are_you_sure = input("Are you sure? This will delete your progress but not your %s points. (y/n) >>> " % str(Player.POINTS))
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
        if Player.CREDITS >= 3:
            Player.CREDITS -= 3
            Player.MAX_HEALTH += 1
            Player.heal()
            print("You upgrade your health. You are also fully healed.")
        else:
            print("You cannot afford to upgrade your health.")
        return True
    elif check_cmd("upgrade", "weapon") or check_cmd("weapon"):
        if Player.CREDITS >= 5:
            Player.CREDITS -= 5
            Player.WEAPON += 1
            print("You upgrade your weapon.")
        else:
            print("You cannot afford to upgrade your weapon.")
        return True
    elif check_cmd("upgrade", "armor") or check_cmd("armor"):
        if Player.CREDITS >= 3:
            Player.CREDITS -= 3
            Player.ARMOR += 1
            print("You upgrade your armor.")
        else:
            print("You cannot afford to upgrade your armor")
        return True
    elif check_cmd("upgrade", ["accessory", "acc"]) or check_cmd(["accessory", "acc"]):
        if Player.CREDITS >= 2:
            Player.CREDITS -= 2
            Player.ACCESSORY += 1
            print("You upgrade your accessory.")
        else:
            print("You cannot afford to upgrade your accessory.")
        return True
    elif check_cmd("heal"):
        if Player.CREDITS >= 1:
            Player.CREDITS -= 1
            Player.heal()
            print("Your health has been restored")
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

    while Player.CURRENT_HEALTH > 0 and rat_current_health > 0:
        print("FIGHT\tSTATS\tENEMY\tFLEE")
        get_cmd()
        if check_cmd(["fight", "attack"]):
            rat_current_health -= Player.WEAPON - rat_armor
            print("You hit the rat for %s damage." % str(Player.WEAPON - rat_armor))
            if rat_current_health <= 0:
                total_payout = Player.get_credit_reward(rat_payout)
                Player.POINTS += total_payout
                print("You have defeated the %s!" % rat_name)
                print("You gained %s credits and %s points!" % (total_payout, total_payout))
                Player.change_menu(Menu.ACTION)
                return True
            else:
                Player.CURRENT_HEALTH -= rat_damage - Player.ARMOR
                print("The %s hits you for %s damage." % (rat_name, str(rat_damage - Player.ARMOR)))
                if Player.CURRENT_HEALTH <= 0:
                    print("You have been defeated.")
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


def run_ratfighter_21xx(points=0):
    Player.POINTS = points
    end = False

    while not end:
        if Player.MENU == Menu.START:
            print("MAIN MENU")
            print("START\tPOINTS\tRESET\tQUIT")
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
            print("You have %s credits to spend." % str(Player.CREDITS))
            print("SHOP UPGRADES:")
            print("HEALTH: 3 credits")
            print("WEAPON: 5 credits")
            print("ARMOR: 3 credits")
            print("ACCESSORY: 2 credits")
            print("HEAL: 1 credit")
            print("Decide what to UPGRADE or LEAVE this menu")
            get_cmd()
            shop_menu()

    return Player.POINTS