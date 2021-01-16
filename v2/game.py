import json
from v2.env import Env, Room
from microgames.ratfighter.game import run_ratfighter_21xx
from microgames.thriftech.game import run_thriftech
from microgames.stox.game import run_stox
from microgames.vocabuloid.game import run_vocabuloid
from microgames.growlike.game import run_growlike
from microgames.storio.game import run_storio
from microgames.farmageddon.game import run_farmageddon

ROOMS = {}
DESC = {}

end = False
cmd = []


def get_cmd():
    """
    Takes input and converts it into an array command
    """

    def log(s):
        with open("log.txt", "a+") as f:
            f.write(" ".join(s) + "\n")

    global cmd
    cmd = [e.lower() for e in input(">>> ").split(" ")]
    log(cmd)


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


def go(*loc):
    """
    Changes room based on given loc as long as the command starts with 'go' or 'go to'
    :param loc: The possible locations to travel and their associated commands
    """
    global cmd

    if check_cmd("go"):
        n = 2 if cmd[1] == "to" else 1
        for e in loc:
            # Synonym engine
            # Returns True if there is at least one match
            if isinstance(e[0], list):
                if cmd[n] in e[0]:
                    Env.change_room(e[1])
                    return True
            elif cmd[n] == e[0]:
                Env.change_room(e[1])
                return True
    return False


# For viewing things which have properties which can be viewed
def look(args):
    if check_cmd("look"):
        n = 2 if cmd[1] == "at" else 1
        # Synonym engine
        # Returns False if there is not at least one match
        if isinstance(args, list):
            if not cmd[n] in args:
                return False
        elif cmd[n] != args:
            return False
        return True
    return False


# For viewing information about the current room
def look_around(s):
    return check_cmd("look", "around") or look(s)


def inventory_check():
    return False


def charm_check():
    return False


def misc_check():
    return False


def debug_check():
    # Save the game with the given command as the file name
    if check_cmd("save"):
        if Env.save(cmd[1:]):
            print("Game '%s' saved." % " ".join(cmd[1:]))
        else:
            print("Failed to save game '%s'." % " ".join(cmd[1:]))
        return True
    # Load the game with the given command as the file name
    elif check_cmd("load"):
        if Env.load(cmd[1:]):
            print("Game '%s' loaded." % " ".join(cmd[1:]))
        else:
            print("Failed to load game '%s'." % " ".join(cmd[1:]))
        return True
    # View all save games
    elif check_cmd(["view", "look", "show"], ["save", "saves"]):
        Env.show_saves()
        return True
    # Quit the game
    elif check_cmd(["quit", "exit"]):
        are_you_sure = input("Are you sure you want to quit? [y/n] >>> ")
        if are_you_sure[0] == "y":
            print("Goodbye.")
            exit(0)
        else:
            return True
    elif check_cmd("debug"):
        pretty_data = json.dumps(Env.data, indent=2)
        print(pretty_data)
        return True
    return False


# Utility decorator for room functions
def register_room(room, description):
    DESC[room] = description

    # Commands which may be triggered from any room
    def universal_check(f):

        def wrapper():
            get_cmd()
            if inventory_check():
                pass
            elif charm_check():
                pass
            elif misc_check():
                pass
            elif debug_check():
                pass
            elif not f():
                print("I don't understand \"%s\"." % " ".join(cmd))

        return wrapper

    # registers the room's associated function for dictionary traversal
    def register_function(f):
        ROOMS[room] = universal_check(f)

    return register_function


@register_room(Room.BEDROOM, "You are in your bedroom.")
def bedroom():
    if look_around("bedroom"):
        print("Your bedroom.")
        print("Your Game Engine 2 and a television are in here with you.")
        if not Env.data["bedroom"]["bed made"]:
            print("Your BED needs to be made.")
        else:
            print("Your bed is made.")
        if not Env.data["bedroom"]["room tidied"]:
            print("Your ROOM could use a TIDY.")
        else:
            print("Your room is tidy.")
        return True

    elif check_cmd("play", "ratfighter"):
        if Env.data["games"]["owned"]["ratfighter"]:
            Env.data["ratfighter"] = run_ratfighter_21xx(Env.data["ratfighter"])
            if Env.data["ratfighter"]["points"] >= 50:
                Env.data["games"]["completed"]["ratfighter"] = True
        else:
            print("You do not have RatFighter.")
        return True
    elif check_cmd("play", "thriftech"):
        if Env.data["games"]["owned"]["thriftech"]:
            Env.data["thriftech"] = run_thriftech(Env.data["thriftech"])
            if all(Env.data["thriftech"]["computer"].values()):
                Env.data["games"]["completed"]["thriftech"] = True
        else:
            print("You do not have ThrifTech.")
        return True
    elif check_cmd("play", "stox"):
        if Env.data["games"]["owned"]["stox"]:
            Env.data["stox"] = run_stox(Env.data["stox"])
            if Env.data["stox"]["credits"] >= 200:
                Env.data["games"]["completed"]["stox"] = True
        else:
            print("You do not have Stox")
        return True
    elif check_cmd("play", "vocabuloid"):
        if Env.data["games"]["owned"]["vocabuloid"]:
            game_complete = run_vocabuloid(Env.data["vocabuloid"]["best time"])
            if game_complete:
                Env.data["games"]["completed"]["vocabuloid"] = True
                if game_complete < Env.data["vocabuloid"]["best time"] or Env.data["vocabuloid"]["best time"] == 0:
                    Env.data["vocabuloid"]["best time"] = game_complete
        else:
            print("You do not have Vocabuloid.")
        return True
    elif check_cmd("play", "growlike"):
        if Env.data["games"]["owned"]["growlike"]:
            game_complete = run_growlike()
            if game_complete:
                Env.data["games"]["completed"]["growlike"] = True
        else:
            print("You do not have GrowLike.")
        return True
    elif check_cmd("play", "storio"):
        if Env.data["games"]["owned"]["storio"]:
            Env.data["storio"] = run_storio(Env.data["storio"])
            if Env.data["storio"]["credits"] > 260:
                Env.data["games"]["completed"]["storio"] = True
        else:
            print("You do not have Storio.")
        return True
    elif check_cmd("play", "farmageddon"):
        if Env.data["games"]["owned"]["farmageddon"]:
            Env.data["farmageddon"] = run_farmageddon(Env.data["farmageddon"])
        else:
            print("You do not have Farmageddon")
        return True

    elif check_cmd("make", "bed"):
        if not Env.data["bedroom"]["bed made"]:
            Env.data["bedroom"]["bed made"] = True
            print("You make your bed. That's nice.")
        else:
            print("Your bed is already made.")
        return True
    elif check_cmd(["tidy", "clean"], "room"):
        if not Env.data["bedroom"]["room tidied"]:
            Env.data["bedroom"]["room tidied"] = True
            print("You tidy your room. Much better.")
        else:
            print("You have already tidied up.")
        return True

    elif go(("bathroom", Room.BATHROOM), ("chamber", Room.CHAMBER)):
        return True

    return False


@register_room(Room.BATHROOM, "You are in your very own bathroom.")
def bathroom():
    if look_around("bathroom"):
        print("Nothing remarkable. A shower but no tub.")
        print("The toilet lid is up.")
        if Env.data["bathroom"]["thriftech"]:
            print("There is a ThrifTech module on the floor.")
        return True
    elif check_cmd(["take", "get", "grab"], ["thriftech", "module"]) and Env.data["bathroom"]["thriftech"]:
        Env.data["bathroom"]["thriftech"] = False
        Env.data["games"]["owned"]["thriftech"] = True
        print("You grab the ThrifTech module.")
        print("You can now PLAY it in your bedroom.")
        return True

    elif go((["bedroom", "room"], Room.BEDROOM)):
        return True

    return False


@register_room(Room.CHAMBER, "You are in the digital chamber.")
def chamber():
    if go((["bedroom", "room"], Room.BEDROOM)):
        return True

    return False


def run_game():
    global end

    while not end:

        for room in Room:

            if Env.data["player"]["location"] == room.value:
                if Env.data["player"]["previous location"] != room.value:
                    print(DESC[room])
                    Env.change_room(room)
                ROOMS[room]()

    print("Game Complete! Congratulations!")


run_game()
