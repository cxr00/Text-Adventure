from enums import *
from states import Env
from player import Player
from words import Words

ROOMS = {}
DESC = {}

end = False
command = []


def get_command():
    """
    Takes input and converts it into an array command
    """
    global command
    out = input(">>> ").split(" ")
    command = [e.lower() for e in out]


# Checks a list for at least one match
# Used for primary command interpreters
def at_least_one_match(e, cmd):
    for each in e:
        if cmd == each:
            return True
    return False


def check_command(*args):
    """
    Determines if command matches args

    :param args: To match to the command
    :return: Whether args matches command
    """
    # global command
    # If the command is not at least as long as args, then it is obviously false
    if len(command) < len(args):
        return False
    for n in range(len(args)):
        # Synonym engine
        # Returns True if there is at least one match
        if isinstance(args[n], list):
            if not at_least_one_match(args[n], command[n]):
                return False
        elif command[n] != args[n].lower():
            return False
    return True


def go(*loc):
    """
    Changes room based on what command[1] matches provided command[0] is 'go'
    :param loc: The possible locations to travel
    """
    if command[0] == "go":
        for e in loc:
            # Synonym engine
            # Returns True if there is at least one match
            if isinstance(e[0], list):
                if at_least_one_match(e[0], command[1]):
                    Player.change_room(e[1])
                    return True
            elif command[1] == e[0]:
                Player.change_room(e[1])
                return True
    return False


# All commands associated with items in the player's inventory
# This is included in the all_room_check decorator
def inventory_check():

    def check_need_to_poop():
        if Player.needs_to_poop():
            print("Your tummy gurgles. Probably need a bathroom.")

    if Item.WIDGET in Player.inventory:
        if check_command("look", "widget"):
            print("It is a widget. Fascinating. You can PROCESS this.")
            return True
        elif check_command("process", "widget"):
            Player.give_credits(8)
            Player.take_item(Item.WIDGET)
            print("You process the widget. You earn 8 credits!")
            return True

    if Item.BURRITO in Player.inventory:
        if check_command("look", "burrito"):
            print("A burrito from the vending machine.")
            return True
        elif check_command("eat", "burrito"):
            Player.take_item(Item.BURRITO)
            Player.EATEN_BURRITO = True
            print("You eat the burrito. Scrumptch!")
            Player.give_item(Item.WRAPPER)
            print("You are left with the burrito WRAPPER.")
            check_need_to_poop()
            return True

    if Item.SODA in Player.inventory:
        if check_command("look", "soda"):
            print("A pepsi from the vending machine.")
            return True
        elif check_command("drink", "soda"):
            Player.take_item(Item.SODA)
            Player.DRANK_PEPSI = True
            print("You drink the soda. Scrumptch!")
            Player.give_item(Item.SODA_CAN)
            print("You are left with the soda CAN.")
            check_need_to_poop()
            return True

    if Item.BANANA in Player.inventory:
        if check_command("look", "banana"):
            print("A banana from the vending machine.")
            return True
        elif check_command("eat", "banana"):
            Player.take_item(Item.BANANA)
            Player.EATEN_BANANA = True
            print("You eat the banana. Scrumptch!")
            Player.give_item(Item.PEEL)
            print("You are left with the banana PEEL.")
            check_need_to_poop()
            return True
    return False


# All commands associated with the charms in the player's possession
def charm_check():
    if Charm.GENERATE in Player.charms:
        if check_command("generate"):
            if Item.WIDGET not in Player.inventory:
                Player.give_item(Item.WIDGET)
                print("You generate a widget.")
            else:
                print("You already have a widget in your possession.")
            return True
    return False


# Additional utility commands
def misc_check():
    if check_command("credits") or check_command("look", "credits"):
        print("You have %s credits." % Player.credits)
        return True
    elif check_command("reset"):
        Player.reset()
        return True
    elif check_command("look", "inventory"):
        print("You take a look at your possessions:")
        for e in Player.inventory:
            print(e.name)
        return True
    elif check_command("look", "charms"):
        print("You take a look at your charms:")
        for e in Player.charms:
            print(e.name)
        return True

    # Whatever I need to speed up testing
    elif check_command("debug"):
        Player.change_room(Room.CELLAR)
        return True
    return False


# Utility decorator for room functions
def register_room(room, description):
    DESC[room] = description

    # Commands which may be triggered from any room
    def universal_check(f):

        def wrapper():
            get_command()
            if inventory_check():
                pass
            elif charm_check():
                pass
            elif misc_check():
                pass
            elif not f():
                print("I don't understand %s." % " ".join(command))

        return wrapper

    # registers the room's associated function for dictionary traversal
    def register_function(f):
        ROOMS[room] = universal_check(f)

    return register_function


@register_room(Room.BEDROOM, "You are in your bedroom.")
def bedroom():
    if go(("bathroom", Room.BATHROOM), ("kitchen", Room.KITCHEN)):
        return True
    else:
        if check_command("look", ["around", "bedroom"]):
            print("It is your bedroom.")
            print("The door to your bathroom is open.")
            print("The door to your kitchen is also open.\n")
            return True
    return False


@register_room(Room.BATHROOM, "You are in your bathroom.")
def bathroom():
    if Env.Bathroom.SITTING_ON_TOILET:
        if check_command(["poop", "shit"]) or check_command("take", ["dump", "shit"]):
            if Player.NEEDS_TO_POOP:
                Player.NEEDS_TO_POOP = False
                Player.HAS_POOPED = True
                print("Ah, sweet relief!")
            else:
                print("You don't need to do that right now.")
            return True
        elif check_command("stand"):
            Env.Bathroom.SITTING_ON_TOILET = False
            print("You get off the toilet.")
            return True
    elif go((["bedroom", "room"], Room.BEDROOM)):
        return True
    elif check_command("look", ["around", "bathroom"]):
        print("Your own bathroom. How lucky!")
        print("Your toilet lid is up.")
        if Env.Bathroom.KEY_ON_FLOOR:
            print("There is a key on the floor.")
        return True
    elif check_command("sit", "toilet"):
        Env.Bathroom.SITTING_ON_TOILET = True
        print("You sit on the toilet.")
        return True
    elif check_command(Words.TAKE, "key"):
        if Env.Bathroom.KEY_ON_FLOOR:
            Player.give_item(Item.KEY)
            Env.Bathroom.KEY_ON_FLOOR = False
            print("You pick up the key from the floor.")
        else:
            print("There is nothing on the floor.")
        return True
    return False


@register_room(Room.KITCHEN, "You are in your kitchen.")
def kitchen():
    if go(("bedroom", Room.BEDROOM), ("vendor", Room.VENDOR), ("monetizor", Room.MONETIZOR), ("outside", Room.OUTSIDE)):
        return True
    else:
        if check_command("look", ["around", "kitchen"]):
            print("This is definitely a kitchen.")
            print("There is a vendor.")
            print("There is also a monetizor.")
            print("The trash can is there if you want to THROW AWAY anything.")
            return True
        elif check_command("throw", "away") or check_command(["look", "go"], "trash"):
            Player.change_room(Room.TRASH_CAN)
            return True


@register_room(Room.VENDOR, "You are standing at the vendor. What will you BUY?")
def vendor():

    def buy(name, item):
        Player.take_credits(10)
        Player.give_item(item)
        print("You buy a %s." % name)

    if Player.credits >= 10:
        if check_command("buy", "burrito"):
            buy("burrito", Item.BURRITO)
            return True
        elif check_command("buy", "banana"):
            buy("banana", Item.BANANA)
            return True
        elif check_command("buy", "soda"):
            buy("soda", Item.SODA)
            return True
    elif check_command("buy"):
        print("You cannot afford anything.")
        return True

    if check_command("leave") or check_command("go", "kitchen"):
        Player.change_room(Room.KITCHEN)
        return True
    elif check_command("look", ["around", "vendor"]):
        print("BURRITO, BANANA, or SODA?")
        return True

    return False


@register_room(Room.MONETIZOR, "You are standing at the monetizor.")
def monetizor():
    if check_command("look", ["around", "monetizor"]):
        print("There is a sticker on the side of the monetizor which reads:")
        print("INSERT contraband for a credit reward.")
        return True
    elif check_command(["insert", "put", "place", "give"], ["charm", "generate"]):
        Player.give_credits(50)
        Player.take_charm(Charm.GENERATE)
        print("You put the generate charm into the monetizor.")
        print("It whirs and spits out 50 credits. Sweet!")
        Player.change_room(Room.KITCHEN)
        return True
    elif check_command("leave") or check_command("go", "kitchen"):
        print("You leave the monetizor.")
        Player.change_room(Room.KITCHEN)
        return True
    return False


@register_room(Room.TRASH_CAN, "You are standing at the trash can.")
def trash_can():

    def check_trash_is_full():
        if Env.trash_is_full() and not Env.Kitchen.TRASH_TAKEN:
            print("The trash is full. Better TAKE it out.")

    if check_command("leave") or check_command("go", "kitchen"):
        Player.change_room(Room.KITCHEN)
        return True
    elif check_command("look", "trash", "can"):
        if Env.trash_is_full():
            if Env.Kitchen.TRASH_TAKEN:
                print("The trash can is empty.")
            else:
                print("The trash can is full.")
        else:
            print("There's still a bit of room in the trash can.")
        return True
    elif check_command(Words.TAKE, "trash") and Env.trash_is_full() and not Env.Kitchen.TRASH_TAKEN:
        Player.give_item(Item.TRASH)
        Env.Kitchen.TRASH_TAKEN = True
        print("You take the TRASH bag out of the can.")
        print("The garbage bin is OUTSIDE.")
        Player.change_room(Room.KITCHEN)
        return True

    if Item.WRAPPER in Player.inventory:
        if check_command("toss", "wrapper") or check_command("throw", "away", "wrapper"):
            Player.take_item(Item.WRAPPER)
            Env.Kitchen.WRAPPER_IN_TRASH = True
            print("You throw away the burrito wrapper.")
            check_trash_is_full()
            return True
    if Item.PEEL in Player.inventory:
        if check_command("toss", "peel") or check_command("throw", "away", "peel"):
            Player.take_item(Item.PEEL)
            Env.Kitchen.PEEL_IN_TRASH = True
            print("You throw away the banana peel.")
            check_trash_is_full()
            return True
    if Item.SODA_CAN in Player.inventory:
        if check_command("toss", "can") or check_command("throw", "away", "can"):
            Player.take_item(Item.SODA_CAN)
            Env.Kitchen.CAN_IN_TRASH = True
            print("You throw away the soda can.")
            check_trash_is_full()
            return True
    return False


@register_room(Room.OUTSIDE, "You are outside. What a place to be.")
def outside():
    if go((["inside", "kitchen"], Room.KITCHEN)):
        return True
    else:
        if check_command("look", ["around", "outside"]):
            print("Ah, to be outside.")
            print("The trash bin is on your left.")
            if Env.Outside.TRASH_IN_BIN:
                print("The trash is in the bin.")
            print("The CELLAR is on your right.")
            return True

        if Item.TRASH in Player.inventory:
            if check_command("toss", "trash") or check_command("throw", "away", "trash"):
                Player.take_item(Item.TRASH)
                Env.Outside.TRASH_IN_BIN = True
                print("You throw away the trash in the bin. Chores done!")
                return True

        if Item.KEY in Player.inventory:
            if check_command("use", "key") or check_command("unlock", "cellar") and Env.Outside.CELLAR_DOOR_LOCKED:
                Env.Outside.CELLAR_DOOR_LOCKED = False
                print("You unlock the cellar door with the key.")
                return True

        if check_command("go", "cellar"):
            if Env.Outside.CELLAR_DOOR_LOCKED:
                if Item.KEY in Player.inventory:
                    Env.Outside.CELLAR_DOOR_LOCKED = False
                    print("You unlock the door and go down into the cellar.")
                    Player.change_room(Room.CELLAR)
                else:
                    print("You try to open the cellar door but it is locked.")
            else:
                print("You go down into the cellar.")
                Player.change_room(Room.CELLAR)
            return True
    return False


@register_room(Room.CELLAR, "You are in the cellar. It's very dusty.")
def cellar():
    if go((["upstairs", "outside"], Room.OUTSIDE)):
        return True
    else:
        if check_command("look", ["around", "cellar"]):
            print("It's mostly empty, but there's a few pieces of old furniture.")
            if Env.Cellar.CHARM_ON_TABLE:
                print("There is some sort of CHARM on an end table.")
            return True
        elif check_command(Words.TAKE, "charm") and Env.Cellar.CHARM_ON_TABLE:
            Player.give_charm(Charm.GENERATE)
            Env.Cellar.CHARM_ON_TABLE = False
            print("You take the GENERATE charm from the table.")
            return True
    return False


print("Welcome to Burrito Eater 2021")

while not end:

    for room in Room:
        if Player.location == room:

            # Only print room description when you enter a room
            if Player.previous_loc != room:
                print(DESC[room])
            Player.change_room(room)

            # Run the specific room function
            ROOMS[room]()

            # Check win condition
            if Env.Outside.TRASH_IN_BIN and Player.HAS_POOPED:
                end = True

            break


print("Game Complete! Congratulations!")
