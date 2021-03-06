from random import randint
from enum import Enum

cmd = []


class Room(Enum):

    AT_MACHINE = "machine"
    AT_WORKBENCH = "workbench"
    AT_COMPUTER = "computer"
    QUIT_GAME = "quit"


room = Room.AT_MACHINE

state_functions = {}

desc = {
    "machine": "You are at the recycling machine.",
    "workbench": "You are at the workbench.",
    "computer": "You are at the defunct computer."
}

menu = {
    "machine": "PROCESS TRASH\tWORKBENCH\tCOMPUTER\tINVENTORY\tQUIT",
    "workbench": "CRAFT\tMACHINE\tCOMPUTER\tINVENTORY\tQUIT",
    "computer": "CRAFT\tLOOK\tFIX\tMACHINE\tWORKBENCH\tINVENTORY\tQUIT"
}

computer = {
    "psu": False,
    "motherboard": False,
    "processor": False,
    "graphics card": False,
    "hard drive": False,
    "solid state drive": False,
    "ram": False
}

inventory = {
    "glass": 0,
    "scrap metal": 0,
    "plastic": 0,
    "copper wire": 0,

    "circuit board": 0,
    "cable": 0,
    "microchip": 0,
    "capacitor": 0,
    "casing": 0,

    "psu": 0,
    "motherboard": 0,
    "processor": 0,
    "graphics card": 0,
    "hard drive": 0,
    "solid state drive": 0,
    "ram": 0,

    "computer": 0
}

material_recipes = {
    "circuit board": (("glass", 1), ("plastic", 1), ("copper wire", 1)),
    "cable": (("copper wire", 2), ("plastic", 1)),
    "microchip": (("scrap metal", 1), ("plastic", 1), ("glass", 1)),
    "capacitor": (("scrap metal", 1), ("copper wire", 1), ("glass", 1)),
    "casing": (("scrap metal", 2), ("plastic", 1), ("glass", 1))
}

component_recipes = {
    "psu": (("casing", 1), ("cable", 2), ("capacitor", 3)),
    "motherboard": (("circuit board", 2), ("cable", 1), ("microchip", 1)),
    "processor": (("microchip", 2), ("cable", 2), ("capacitor", 1)),
    "graphics card": (("casing", 1), ("microchip", 2), ("circuit board", 1)),
    "hard drive": (("casing", 1), ("circuit board", 1), ("cable", 2)),
    "solid state drive": (("casing", 1), ("circuit board", 1), ("microchip", 1)),
    "ram": (("microchip", 1), ("cable", 1), ("circuit board", 1))
}


def computer_is_fixed():
    return all(computer.values())


def reset_computer():
    for each in computer:
        computer[each] = False


def reset_inventory():
    for each in inventory:
        if each != "computer":
            inventory[each] = 0


def view_inventory():
    for key, value in inventory.items():
        if inventory[key] > 0:
            print("%s: %s" % (key, value))


# Returns True if recipe make is successful
def craft(item_name, recipe):
    global inventory

    # Check that all materials are present in inventory
    for each in recipe:
        if inventory[each[0]] >= each[1]:
            pass
        else:
            print("You do not have sufficient materials to craft this.")
            for r in recipe:
                print(r[0], "%d / %d" % (inventory[r[0]], r[1]))
            return False

    # Remove items from player's inventory
    for each in recipe:
        inventory[each[0]] -= each[1]

    print("You craft a %s" % item_name)

    inventory[item_name] += 1

    return True


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


def universal_check():
    global room
    if check_cmd(["inventory", "items"]):
        view_inventory()
        return True
    elif check_cmd("look", "around"):
        print("There is a trash-processing MACHINE.")
        print("Your WORKBENCH is here.")
        print("The defunct COMPUTER is here too.")
        return True
    elif check_cmd("machine"):
        room = Room.AT_MACHINE
        return True
    elif check_cmd("workbench"):
        room = Room.AT_WORKBENCH
        return True
    elif check_cmd("computer"):
        room = Room.AT_COMPUTER
        return True
    elif check_cmd(["quit", "exit"]):
        room = Room.QUIT_GAME
        return True
    elif check_cmd("reset"):
        reset_computer()
        reset_inventory()
        room = Room.AT_MACHINE
        print("You have reset your progress.")
        return True
    elif check_cmd("debug"):
        inventory["psu"] += 1
        inventory["motherboard"] += 1
        inventory["processor"] += 1
        inventory["graphics card"] += 1
        inventory["hard drive"] += 1
        inventory["solid state drive"] += 1
        inventory["ram"] += 1
        return True
    return False


def register_room(room):

    def register_func(f):
        state_functions[room.value] = f

    return register_func


# Process trash for ingredients
@register_room(Room.AT_MACHINE)
def at_machine():
    if check_cmd("process"):
        a = randint(0, 2)
        inventory["glass"] += a
        if a > 0:
            print("You get %s glass." % str(a))

        a = randint(0, 2)
        inventory["scrap metal"] += a
        if a > 0:
            print("You get %s scrap metal." % str(a))

        a = randint(0, 2)
        inventory["plastic"] += a
        if a > 0:
            print("You get %s plastic." % str(a))

        a = randint(0, 2)
        inventory["copper wire"] += a
        if a > 0:
            print("You get %s copper wire." % str(a))

        return True

    return False


# Craft ingredients into materials
@register_room(Room.AT_WORKBENCH)
def at_workbench():
    if check_cmd("craft"):
        if len(cmd) == 1:
            for each in material_recipes:
                print(each + ":", end=" ")
                for piece in material_recipes[each]:
                    print("%s %d / %d" % (piece[0], inventory[piece[0]], piece[1]), end=", ")
                print()
            return True
        else:
            for each in material_recipes:
                if check_cmd("craft", *[k for k in (each.split(" "))]):
                    craft(each, material_recipes[each])
                    return True

    return False


# Build materials into components
# Place the components into the computer
@register_room(Room.AT_COMPUTER)
def at_computer():
    if check_cmd(["look", "view", "check", "computer"]):
        for each in computer:
            if not computer[each]:
                print("The %s is missing." % each)
        return True

    elif check_cmd("craft"):
        if len(cmd) == 1:
            for each in component_recipes:
                if not computer[each]:
                    print(each + ":", end=" ")
                    for piece in component_recipes[each]:
                        print("%s %d / %d" % (piece[0], inventory[piece[0]], piece[1]), end=", ")
                    print()
            return True
        else:
            for each in component_recipes:
                if check_cmd("craft", *[k for k in (each.split(" "))]):
                    craft(each, component_recipes[each])
                    return True

    elif check_cmd("fix"):
        at_least_one = False
        for each in computer:
            if not computer[each] and inventory[each] >= 1:
                inventory[each] -= 1
                computer[each] = True
                at_least_one = True
                print("You install the new %s in the computer." % each)
        if not at_least_one:
            print("You have no components to put in the computer.")
        return True

    return False


def run_thriftech(data=None):
    global inventory
    global room
    global computer

    if data:
        inventory = data["inventory"]
        computer = data["computer"]
    end = False

    while not end:
        valid_command = False

        if room == Room.QUIT_GAME:
            room = Room.AT_MACHINE
            end = True
            valid_command = True
        else:
            for each_room in Room:
                if room == each_room:
                    print(desc[room.value], menu[room.value], sep="\n")
                    break

            get_cmd()

            valid_command = True if universal_check() else state_functions[room.value]()

            if computer_is_fixed():
                end = True
                print("You have completely fixed the computer.")

        if not valid_command:
            print("I don't understand \"%s\"" % " ".join(cmd))

    if computer_is_fixed():
        print("GAME COMPLETE. CONGRATULATIONS!")
        inventory["computer"] += 1
        reset_computer()
        room = Room.AT_MACHINE

    return {"computer": computer, "inventory": inventory}
