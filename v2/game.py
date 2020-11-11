from v2.env import Env, Room
from microgames.ratfighter.game import run_ratfighter_21xx
from microgames.thriftech.game import run_thriftech

ROOMS = {}
DESC = {}

end = False
cmd = []

current_room = Room.BEDROOM
previous_loc = None


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


def go(*loc):
    """
    Changes room based on given loc as long as the command starts with 'go' or 'go to'
    :param loc: The possible locations to travel and their associated commands
    """
    global current_room

    if check_cmd("go"):
        n = 2 if cmd[1] == "to" else 1
        for e in loc:
            # Synonym engine
            # Returns True if there is at least one match
            if isinstance(e[0], list):
                if cmd[n] in e[0]:
                    # Player.change_room(e[1])
                    current_room = e[1]
                    return True
            elif cmd[n] == e[0]:
                # Player.change_room(e[1])
                current_room = e[1]
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
    if check_cmd("save"):
        if Env.save(cmd[1:]):
            print("Game saved.")
        else:
            print("Failed to save game.")
        return True
    elif check_cmd("load"):
        if Env.load(cmd[1:]):
            print("Game loaded.")
        else:
            print("Failed to load game.")
        return True
    elif check_cmd("debug"):
        print(Env.data)
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
        if Env.data["games"]["ratfighter"]:
            Env.data["ratfighter"] = run_ratfighter_21xx(Env.data["ratfighter"])
        else:
            print("You do not have RATFIGHTER.")
        return True
    elif check_cmd("play", "thriftech"):
        if Env.data["games"]["thriftech"]:
            victory = run_thriftech()
            print("victory: %s" % str(victory))
        else:
            print("You do not have THRIFTECH.")
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

    elif go(("bathroom", Room.BATHROOM)):
        return True


@register_room(Room.BATHROOM, "You are in your very own bathroom.")
def bathroom():
    if look_around("bathroom"):
        print("Nothing remarkable. A shower but no tub.")
        print("The toilet lid is up.")
        if Env.data["bathroom"]["thriftech"]:
            print("There is a THRIFTECH cartridge on the floor.")
        return True
    elif check_cmd(["take", "get", "grab"], ["thriftech", "cartridge"]):
        Env.data["bathroom"]["thriftech"] = False
        Env.data["games"]["thriftech"] = True
        print("You grab the THRIFTECH cartridge.")
        print("You can now PLAY it in your bedroom.")
        return True

    elif go(("bedroom", Room.BEDROOM)):
        return True


def run_game():
    global end
    global current_room
    global previous_loc

    while not end:

        for room in Room:
            if current_room == room:

                # Only print room description when you enter a room
                if previous_loc != room:
                    print(DESC[room])
                previous_loc, current_room = current_room, room

                # Run the specific room function
                ROOMS[room]()

                break

            # if Env.data["player"]["current room"] == room.value:
            #
            #     if Env.data["player"]["previous room"] != room:.value
            #         print(DESC[room])
            #
            #     Env.data["player"]["previous room"] = Env.data["player"]["current room"]
            #     Env.data["player"]["current room"] = room.value

    print("Game Complete! Congratulations!")


run_game()