from microgames.thriftech.recipes import MaterialRecipe, ComponentRecipe
from microgames.thriftech.states import Room, Computer

from random import randint

cmd = []
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
    "ram": 0
}
room = Room.AT_MACHINE


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
    elif check_cmd("quit"):
        room = Room.QUIT_GAME
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
    if check_cmd("craft") and len(cmd) == 1:
        print("CIRCUIT BOARD: " + str(MaterialRecipe.CIRCUIT_BOARD))
        print("CABLE: " + str(MaterialRecipe.CABLE))
        print("MICROCHIP: " + str(MaterialRecipe.MICROCHIP))
        print("CAPACITOR: " + str(MaterialRecipe.CAPACITOR))
        print("CASING: " + str(MaterialRecipe.CASING))
        return True
    elif check_cmd("craft", "circuit", "board"):
        craft("circuit board", MaterialRecipe.CIRCUIT_BOARD)
        return True
    elif check_cmd("craft", "cable"):
        craft("cable", MaterialRecipe.CABLE)
        return True
    elif check_cmd("craft", "microchip"):
        craft("microchip", MaterialRecipe.MICROCHIP)
        return True
    elif check_cmd("craft", "capacitor"):
        craft("capacitor", MaterialRecipe.CAPACITOR)
        return True
    elif check_cmd("craft", "casing"):
        craft("casing", MaterialRecipe.CASING)
        return True

    return False


# Build materials into components
# Place the components into the computer
def at_computer():
    if check_cmd(["look", "view", "check"], "computer"):
        if not Computer.PSU:
            print("The PSU is missing.")
        if not Computer.MOTHERBOARD:
            print("The MOTHERBOARD is missing.")
        if not Computer.PROCESSOR:
            print("The PROCESSOR is missing.")
        if not Computer.GRAPHICS_CARD:
            print("The GRAPHICS CARD is missing.")
        if not Computer.HARD_DRIVE:
            print("The HARD DRIVE is missing.")
        if not Computer.SOLID_STATE_DRIVE:
            print("The SOLID STATE DRIVE is missing.")
        if not Computer.RAM:
            print("The RAM is missing.")
        return True

    elif check_cmd("craft") and len(cmd) == 1:
        print("PSU: " + str(ComponentRecipe.PSU))
        print("MOTHERBOARD: " + str(ComponentRecipe.MOTHERBOARD))
        print("PROCESSOR: " + str(ComponentRecipe.PROCESSOR))
        print("GRAPHICS CARD: " + str(ComponentRecipe.GRAPHICS_CARD))
        print("HARD DRIVE: " + str(ComponentRecipe.HARD_DRIVE))
        print("SOLID STATE DRIVE: " + str(ComponentRecipe.SOLID_STATE_DRIVE))
        print("RAM: " + str(ComponentRecipe.RAM))
        return True
    elif check_cmd("craft", "psu"):
        craft("psu", ComponentRecipe.PSU)
        return True
    elif check_cmd("craft", "motherboard"):
        craft("motherboard", ComponentRecipe.MOTHERBOARD)
        return True
    elif check_cmd("craft", "processor"):
        craft("processor", ComponentRecipe.PROCESSOR)
        return True
    elif check_cmd("craft", "graphics", "card"):
        craft("graphics card", ComponentRecipe.GRAPHICS_CARD)
        return True
    elif check_cmd("craft", "hard", "drive"):
        craft("hard drive", ComponentRecipe.HARD_DRIVE)
        return True
    elif check_cmd("craft", "solid", "state", "drive"):
        craft("solid state drive", ComponentRecipe.SOLID_STATE_DRIVE)
        return True
    elif check_cmd("craft", "ram"):
        craft("ram", ComponentRecipe.RAM)
        return True

    elif check_cmd("fix", "computer"):
        if not Computer.PSU and inventory["psu"] >= 1:
            Computer.PSU = True
            print("You install the new PSU in the computer.")
        if not Computer.MOTHERBOARD and inventory["motherboard"] >= 1:
            inventory["motherboard"] -= 1
            Computer.MOTHERBOARD = True
            print("You install the new MOTHERBOARD in the computer.")
        if not Computer.PROCESSOR and inventory["processor"] >= 1:
            inventory["processor"] -= 1
            Computer.PROCESSOR = True
            print("You install the new PROCESSOR in the computer.")
        if not Computer.GRAPHICS_CARD and inventory["graphics card"] >= 1:
            inventory["graphics card"] -= 1
            Computer.GRAPHICS_CARD = True
            print("You install the new GRAPHICS CARD in the computer.")
        if not Computer.HARD_DRIVE and inventory["hard drive"] >= 1:
            inventory["hard drive"] -= 1
            Computer.HARD_DRIVE = True
            print("You install the new HARD DRIVE in the computer.")
        if not Computer.SOLID_STATE_DRIVE and inventory["solid state drive"] >= 1:
            inventory["solid state drive"] -= 1
            Computer.SOLID_STATE_DRIVE = True
            print("You install the new SOLID STATE DRIVE in the computer.")
        if not Computer.RAM and inventory["ram"] >= 1:
            inventory["ram"] -= 1
            Computer.RAM = True
            print("You install the new RAM in the computer.")
        return True

    return False


def run_thriftech():
    global room
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
            print("CRAFT\tLOOK COMPUTER\tFIX COMPUTER\tMACHINE\tWORKBENCH\tINVENTORY")
            get_cmd()
            if not universal_check():
                valid_command = at_computer()
            else:
                valid_command = True
            if Computer.computer_is_fixed():
                end = True
                print("You have completely fixed the computer.")
        elif room == Room.QUIT_GAME:
            room = Room.AT_MACHINE
            print("GOODBYE!")
            return end

        if not valid_command:
            print("I don't understand \"%s\"" % " ".join(cmd))

    print("GAME COMPLETE. CONGRATULATIONS!")

    return end