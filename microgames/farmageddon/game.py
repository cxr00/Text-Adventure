from enum import Enum
import json
import random


class Room(Enum):
    FARM = "farm"
    CAVE = "cave"
    DEEP = "deep"
    FOREST = "forest"
    BEACH = "beach"


data = {
    "location": "farm",
    "previous location": None,

    "inventory":
        {
            "gold": 0,
            "silver": 0,
            "copper": 0,

            "shroomlet": 0,
            "cooked shroomlet": 0,
            "twig": 0,
            "egg spawn": 0
        },

    "farm":
        {
            "fire lit": False
        }
}


ROOMS = {}
DESC = {}
MENUS = {
    "farm": "CAVE\tFOREST\tBEACH\tLOOK AROUND\tQUIT",
    "cave": "FARM\tFOREST\tBEACH\tLOOK AROUND\tQUIT",
    "deep": "CAVE\tLOOK AROUND\tQUIT",
    "forest": "FARM\tCAVE\tBEACH\tLOOK AROUND\tQUIT",
    "beach": "FARM\tCAVE\tFOREST\tLOOK AROUND\tQUIT"
}

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


def change_room(new_room=None):

    def update_location(room):
        data["previous location"] = data["location"]
        data["location"] = room.value

    for room in Room:
        if check_cmd(room.value):
            update_location(room)
            return True
        elif new_room and new_room == room.value:
            update_location(room)
            return True


def inventory_check():
    if look(["items", "inventory"]):
        at_least_one = False
        for key, value in data["inventory"].items():
            if data["inventory"][key] > 0:
                at_least_one = True
                print("%s: %d" % (key, data["inventory"][key]))
        if not at_least_one:
            print("Your inventory is empty.")
        return True

    elif check_cmd("eat", "shroomlet"):
        if data["inventory"]["cooked shroomlet"] > 0:
            data["inventory"]["cooked shroomlet"] -= 1
            print("You eat the cooked shroomlet. Yummy!")
        elif data["inventory"]["shroomlet"] > 0:
            print("You don't want to eat this shroomlet without COOKing it first.")
        else:
            print("You have no shroomlet to eat.")
        return True

    return False


def debug_check():
    if check_cmd(["quit", "exit"]):
        if input("Are you sure you wish to quit? >>> ")[0] == "y":
            global end
            end = True
            return True
    elif check_cmd("debug"):
        print(json.dumps(data, indent=2))
        return True

    return False


# Utility decorator for room functions
def register_room(room, description):
    DESC[room] = description

    # Commands which may be triggered from any room
    def universal_check(f):

        def wrapper():
            print(MENUS[room])
            get_cmd()
            if inventory_check():
                pass
            elif debug_check():
                pass
            elif change_room():
                pass
            elif not f():
                print("I don't understand \"%s\"." % " ".join(cmd))

        return wrapper

    # registers the room's associated function for dictionary traversal
    def register_function(f):
        ROOMS[room] = universal_check(f)

    return register_function


@register_room("farm", "You are on the farm.")
def farm():
    if look_around("farm"):
        print("Your farm. There is a TENT you can SLEEP in.")
        print("There is also a CAMPFIRE spot. ", end="")
        if data["farm"]["fire lit"]:
            print("You could COOK things here.")
        else:
            print("You need to LIGHT it first.")
        return True
    elif look("campfire"):
        if data["farm"]["fire lit"]:
            print("Warm and toasty.")
        else:
            print("It's out. You need to LIGHT it.")
        return True

    elif check_cmd(["rest", "sleep", "nap"]) or check_cmd("use", "tent"):
        print("You rest in your tent. You feel refreshed.")
        return True

    elif check_cmd(["start", "light"], ["fire", "campfire"]):
        if data["farm"]["fire lit"]:
            print("The fire is already lit.")
        elif data["inventory"]["twig"] > 0:
            data["inventory"]["twig"] -= 1
            data["farm"]["fire lit"] = True
            print("You light the campfire. Now you can COOK things.")
        else:
            print("You do not have the materials to light the fire.")
            print("Perhaps a TWIG of some sorts would help?")
        return True

    elif check_cmd("cook", ["shroomlet", "shroomlets"]):
        if data["farm"]["fire lit"]:
            if data["inventory"]["shroomlet"] > 0:
                data["inventory"]["shroomlet"] -= 1
                data["inventory"]["cooked shroomlet"] += 1
                print("You cook the shroomlet. Good job!")
            else:
                print("You do not have any shroomlets to cook.")
        else:
            print("You need to START the FIRE before you can cook anything.")
        return True

    return False


@register_room("cave", "You are in the dank cave.")
def cave():
    if look_around("cave"):
        print("A dank and damp cave.")
        print("There are SHROOMLETS on the ground. You can PICK them.")
        print("You can also VENTURE into the DEEP.")
        return True

    elif check_cmd(["pick", "harvest", "take", "grab", "gather"], ["shroomlet", "shroomlets"]):
        data["inventory"]["shroomlet"] += 1
        print("You pick a shroomlet. It is very fuzzy.")
        return True

    elif check_cmd(["go", "venture"], "deep") or check_cmd(["go", "venture"], ["to", "into"], "deep"):
        change_room("deep")
        print("You venture further into the cave.")
        return True

    return False


@register_room("deep", "You are in the deepest part of the cave.")
def deep():
    if check_cmd("go", ["out", "back", "cave"]):
        change_room("cave")
        return True

    elif look_around("deep"):
        print("There is a gently pulsating SNAKEMESH.")
        print("You can HARVEST it for egg spawn.")
        return True

    elif check_cmd(["take", "harvest", "grab", "gather", "get"], ["snakemesh", "spawn", "mesh"]):
        data["inventory"]["egg spawn"] += 1
        print("You harvest the EGG SPAWN")
        return True

    return False


@register_room("forest", "You are in the lush forest.")
def forest():
    if look_around("forest"):
        print("A shady grove of trees.")
        print("You can GATHER TWIGS here.")
        return True

    elif check_cmd(["pick", "harvest", "take", "grab", "gather"], ["twig", "twigs"]):
        data["inventory"]["twig"] += 1
        print("You gather a twig. Perfect for a campfire.")
        return True

    return False


@register_room("beach", "You are on the sandy beach.")
def beach():
    if look_around("beach"):
        print("A sandy beach. Don't DRINK the WATER!")
        print("You can COMB the BEACH for trinkets.")
        return True

    elif check_cmd("comb", "beach"):
        print("You comb through the sand...")
        # Find gold, silver, or copper trinket
        r = random.randint(0, 10)
        if r > 7:
            data["inventory"]["gold"] += 1
            print("You find a gold coin!")
        elif r > 5:
            data["inventory"]["silver"] += 1
            print("You find a silver coin.")
        elif r > 2:
            data["inventory"]["copper"] += 1
            print("You find a measly copper coin.")
        else:
            print("You don't manage to find anything.")
        return True

    return False


def run_farmageddon(input_data=None):
    global data
    global end

    end = False
    data["previous location"] = None

    if input_data:
        data = input_data

    print("Welcome to Farmageddon!")
    print("Things are pretty bad here.")
    print("You subsist on mushrooms and sleep in a tent.")
    print("For fun you can comb the beach for trinkets.")
    input("Press enter to begin.")

    while not end:
        for room in Room:
            if data["location"] == room.value:
                if data["previous location"] != room.value:
                    print(DESC[room.value])
                    change_room(room.value)
                ROOMS[room.value]()

    print("Goodbye.")

    return data
