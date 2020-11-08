from microgames.thriftech.recipes import MaterialRecipe, ComponentRecipe
from microgames.thriftech.states import Room, Computer

from random import randint

cmd = []
inventory = {
    "glass": 2,
    "scrap metal": 0,
    "plastic": 2,
    "copper wire": 2,

    "circuit board": 1,
    "cable": 2,
    "microchip": 0,
    "capacitor": 0,
    "casing": 1,

    "psu": 0,
    "motherboard": 0,
    "processor": 0,
    "graphics card": 0,
    "hard drive": 0,
    "solid state drive": 0,
    "ram": 0
}
room = Room.AT_MACHINE


def view_inventory():
    for key, value in inventory.items():
        if inventory[key] > 0:
            print("%s: %s" % (key, value))


# Returns True if recipe make is successful
def make(item_name, recipe):
    global inventory

    # Check that all materials are present in inventory
    for each in recipe:
        if inventory[each[0]] >= each[1]:
            pass
        else:
            return False

    # Remove items from player's inventory
    for each in recipe:
        inventory[each[0]] -= each[1]

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
    return False


# Process trash for ingredients
def at_machine():
    if check_cmd("process", "trash"):
        a = randint(0, 2)
        inventory["glass"] += a
        print("You get %s glass." % str(a))

        a = randint(0, 2)
        inventory["scrap metal"] += a
        print("You get %s scrap metal." % str(a))

        a = randint(0, 2)
        inventory["plastic"] += a
        print("You get %s plastic." % str(a))

        a = randint(0, 2)
        inventory["copper wire"] += a
        print("You get %s copper wire." % str(a))

        return True

    return False


# Craft ingredients into materials
def at_workbench():
    return False


# Build materials into components
# Place the components into the computer
def at_computer():
    return False


end = False

while not end:
    valid_command = False
    if room == Room.AT_MACHINE:
        print("You are at the recycling machine.")
        print("PROCESS TRASH\tWORKBENCH\tCOMPUTER\tINVENTORY")
        get_cmd()
        if not universal_check():
            valid_command = at_machine()
        else:
            valid_command = True
    elif room == Room.AT_WORKBENCH:
        print("You are at the workbench.")
        print("CRAFT\tMACHINE\tCOMPUTER\tINVENTORY")
        get_cmd()
        if not universal_check():
            valid_command = at_workbench()
        else:
            valid_command = True
    elif room == Room.AT_COMPUTER:
        print("You are at the defunct computer.")
        print("CRAFT\tMACHINE\tWORKBENCH\tINVENTORY")
        get_cmd()
        if not universal_check():
            valid_command = at_computer()
        else:
            valid_command = True
        if Computer.computer_is_fixed():
            end = True
            print("You have completely fixed the computer.")

    if not valid_command:
        print("I don't understand \"%s\"" % " ".join(cmd))


print("GAME COMPLETE. CONGRATULATIONS!")
