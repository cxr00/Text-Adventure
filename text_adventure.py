from enums import *
from states import Env
from player import Player
from words import Words, GameText

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

    def fun(args, n):
        # Synonym engine
        # Returns True if there is at least one match
        if isinstance(args[n], list):
            if not at_least_one_match(args[n], command[n]):
                return False
        elif command[n] != args[n].lower():
            return False
        return True

    if len(command) < len(args):
        return False

    n = 0
    while n < len(args):
        if not fun(args, n):
            return False
        n += 1

    return True


def go(*loc):
    """
    Changes room based on given loc as long as the command starts with 'go' or 'go to'
    :param loc: The possible locations to travel and their associated commands
    """
    if check_command("go"):
        n = 2 if command[1] == "to" else 1
        for e in loc:
            # Synonym engine
            # Returns True if there is at least one match
            if isinstance(e[0], list):
                if at_least_one_match(e[0], command[n]):
                    Player.change_room(e[1])
                    return True
            elif command[n] == e[0]:
                Player.change_room(e[1])
                return True
    return False


# For viewing things which have properties which can be viewed
def look(args):
    if check_command("look"):
        n = 2 if command[1] == "at" else 1
        if isinstance(args, list):
            if not at_least_one_match(args, command[n]):
                return False
        elif command[n] != args:
            return False
        return True
    return False


# For viewing information about the current room
def look_around(s):
    return check_command("look", "around") or look(s)


# All commands associated with items in the player's inventory
def inventory_check():

    def check_need_to_poop():
        if Player.needs_to_poop():
            print("Your tummy gurgles. Probably need a bathroom.")

    if Item.WIDGET in Player.inventory:
        if look("widget"):
            print("It is a widget. Fascinating. You can PROCESS this.")
            return True
        elif check_command("process", "widget"):
            Player.give_credits(8)
            Player.take_item(Item.WIDGET)
            Player.HAS_ILLEGAL_CURRENCY = True
            print("You process the widget. You earn 8 credits!")
            return True

    if Item.BURRITO in Player.inventory:
        if look("burrito"):
            print("A burrito from the vendor.")
            return True
        elif check_command("eat", "burrito"):
            Player.take_item(Item.BURRITO)
            Player.EATEN_BURRITO = True
            print("You eat the burrito. Scrumptch!")
            Player.give_item(Item.BURRITO_WRAPPER)
            print("You are left with the burrito WRAPPER.")
            check_need_to_poop()
            return True

    if Item.SODA in Player.inventory:
        if look("soda"):
            print("A pepsi from the vendor.")
            return True
        elif check_command("drink", "soda"):
            Player.take_item(Item.SODA)
            Player.DRANK_PEPSI = True
            print("You drink the soda. Scrumptch!")
            Player.give_item(Item.SODA_CAN)
            print("You are left with the soda CAN.")
            check_need_to_poop()
            return True

    if Item.BANANA in Player.inventory or Item.PEELED_BANANA in Player.inventory:
        if look("banana"):
            print("A banana from the vendor.")
            if Item.BANANA in Player.inventory:
                print("I need to PEEL it")
            return True
        elif check_command("eat", "banana"):
            if Item.PEELED_BANANA in Player.inventory:
                Player.take_item(Item.PEELED_BANANA)
                Player.EATEN_BANANA = True
                print("You eat the banana. Scrumptch!")
                check_need_to_poop()
                return True
            elif Item.BANANA in Player.inventory:
                print("You need to PEEL it first.")
                return True
        elif check_command("peel", "banana"):
            Player.take_item(Item.BANANA)
            Player.give_item(Item.PEELED_BANANA)
            Player.give_item(Item.BANANA_PEEL)
            print("You peel the banana.")
            print("You are left with a peeled banana and a banana peel.")
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
    if check_command("credits") or look("credits") or check_command("check", "credits"):
        print("You have %s credits." % Player.credits)
        return True
    elif check_command("reset"):
        Player.reset()
        return True
    elif look(["inventory", "items"]):
        print("You take a look at your possessions:")
        for e in Player.inventory:
            print(e.value)
        return True
    elif look("charms"):
        print("You take a look at your charms:")
        for e in Player.charms:
            print(e.value)
        return True

    # Whatever I need to speed up testing
    elif check_command("debug"):
        Player.HAS_ILLEGAL_CURRENCY = True
        Player.give_credits(10)
        Player.change_room(Room.VENDOR)
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
                print("I don't understand \"%s\"." % " ".join(command))

        return wrapper

    # registers the room's associated function for dictionary traversal
    def register_function(f):
        ROOMS[room] = universal_check(f)

    return register_function


@register_room(Room.BEDROOM, GameText.RoomDescriptions.bedroom)
def bedroom():
    if go(("bathroom", Room.BATHROOM), ("kitchen", Room.KITCHEN)):
        return True
    else:
        if look_around("bedroom"):
            print("It is your bedroom.")
            print("The door to your bathroom is open.")
            print("The door to your kitchen is also open.\n")
            return True
        elif look("floor"):
            print("There is nothing on the floor.")
            return True
    return False


@register_room(Room.BATHROOM, GameText.RoomDescriptions.bathroom)
def bathroom():
    if not Env.Bathroom.SITTING_ON_TOILET:
        if go((["bedroom", "room"], Room.BEDROOM)):
            return True
        elif look_around("bathroom"):
            print("Your own bathroom. How lucky!")
            print("Your toilet lid is up.")
            if Env.Bathroom.KEY_ON_FLOOR:
                print("There is a key on the floor.")
            return True
        elif look("floor"):
            if Env.Bathroom.KEY_ON_FLOOR:
                print("There is a KEY on the floor.")
                return True
            else:
                print("There is nothing on the floor.")
                return True
        elif check_command("sit", "toilet"):
            Env.Bathroom.SITTING_ON_TOILET = True
            print("You sit on the toilet.")
            return True
        elif check_command(Words.TAKE, "key"):
            if Env.Bathroom.KEY_ON_FLOOR:
                Player.give_item(Item.CELLAR_KEY)
                Env.Bathroom.KEY_ON_FLOOR = False
                print("You pick up the key from the floor.")
            else:
                print("There is nothing on the floor.")
            return True
    else:
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
        elif look_around("bathroom"):
            print("The same bathroom from when you were standing up.")
            print("Are you going to POOP or what?")
            return True
        elif look("floor"):
            if Env.Bathroom.KEY_ON_FLOOR:
                print("There is a KEY on the floor.\nYou can't reach it from here.")
                return True
            else:
                print("There is nothing on the floor.")
                return True

    return False


@register_room(Room.KITCHEN, GameText.RoomDescriptions.kitchen)
def kitchen():
    if go(("bedroom", Room.BEDROOM), ("vendor", Room.VENDOR), ("monetizor", Room.MONETIZOR), (["outside", "out"], Room.OUTSIDE)):
        return True
    else:
        if look_around("kitchen"):
            print("This is definitely a kitchen.")
            print("There is a vendor.")
            print("There is also a monetizor.")
            print("The trash can is there if you want to THROW AWAY anything.")
            return True
        elif look("floor"):
            print("There is nothing on the floor.")
            return True
        elif check_command(["look", "go", "use"], "trash") or check_command("throw", "away", "trash"):
            Player.change_room(Room.TRASH_CAN)
            return True
    return False


@register_room(Room.VENDOR, GameText.RoomDescriptions.vendor)
def vendor():

    def buy(name, item):
        Player.take_credits(10)
        Player.give_item(item)
        print("You buy a %s." % name)

    def check_for_illegal_currency():
        if Player.HAS_ILLEGAL_CURRENCY:
            print("The vendor booms in a loud voice:")
            print("ILLEGAL CURRENCY DETECTED. PREPARE TO BE TAKEN INTO CUSTODY.")
            print("...")
            print("Suddenly two robot officers appear and arrest you.")
            print("You shouldn't have used that contraband CHARM!")
            Env.Universal.ILLEGAL_CURRENCY_DISCOVERED = True
            return True
        return False

    if Player.credits >= 10:
        if check_command("buy", "burrito"):
            buy("burrito", Item.BURRITO)
            check_for_illegal_currency()
            return True
        elif check_command("buy", "banana"):
            buy("banana", Item.BANANA)
            check_for_illegal_currency()
            return True
        elif check_command("buy", "soda"):
            buy("soda", Item.SODA)
            check_for_illegal_currency()
            return True
    elif check_command("buy"):
        print("You cannot afford anything.")
        return True

    if look("vendor"):
        print("There is a sticker on the vendor which reads:")
        print("Remember: Illegal Currency is Illegal.")
        return True
    if check_command("leave") or check_command("go", "kitchen"):
        Player.change_room(Room.KITCHEN)
        return True
    elif look_around("vendor"):
        print("BURRITO, BANANA, or SODA?")
        return True

    return False


@register_room(Room.MONETIZOR, GameText.RoomDescriptions.monetizor)
def monetizor():
    if look_around("monetizor"):
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


@register_room(Room.TRASH_CAN, GameText.RoomDescriptions.trash_can)
def trash_can():

    def check_trash_is_full():
        if Env.trash_is_full() and not Env.Kitchen.TRASH_TAKEN:
            print("The trash is full. Better TAKE it out.")

    if check_command("leave") or check_command("go", "kitchen"):
        Player.change_room(Room.KITCHEN)
        return True
    elif look("trash"):
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

    if Item.BURRITO_WRAPPER in Player.inventory:
        if check_command("toss", "wrapper") or check_command("throw", "away", "wrapper"):
            Player.take_item(Item.BURRITO_WRAPPER)
            Env.Kitchen.WRAPPER_IN_TRASH = True
            print("You throw away the burrito wrapper.")
            check_trash_is_full()
            return True
    if Item.BANANA_PEEL in Player.inventory:
        if check_command("toss", "peel") or check_command("throw", "away", "peel"):
            Player.take_item(Item.BANANA_PEEL)
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


@register_room(Room.OUTSIDE, GameText.RoomDescriptions.outside)
def outside():
    if go((["inside", "in", "kitchen"], Room.KITCHEN)):
        return True
    else:
        if look_around("outside"):
            print("Ah, to be outside.")
            print("The trash bin is on your left.")
            if Env.Outside.TRASH_IN_BIN:
                print("The trash is in the bin.")
            print("The CELLAR is on your right.")
            return True
        elif look(["floor", "ground"]):
            print("There is nothing on the ground.")
            return True
        elif check_command("go", "cellar") or check_command("go", "to", "cellar"):
            if Env.Outside.CELLAR_DOOR_LOCKED:
                if Item.CELLAR_KEY in Player.inventory:
                    Env.Outside.CELLAR_DOOR_LOCKED = False
                    print("You unlock the door and go down into the cellar.")
                    Player.change_room(Room.CELLAR)
                else:
                    print("You try to open the cellar door but it is locked.")
            else:
                print("You go down into the cellar.")
                Player.change_room(Room.CELLAR)
            return True

        if Item.TRASH in Player.inventory:
            if check_command("toss", "trash") or check_command("throw", "away", "trash"):
                Player.take_item(Item.TRASH)
                Env.Outside.TRASH_IN_BIN = True
                print("You throw away the trash in the bin. Chores done!")
                return True

        if Item.CELLAR_KEY in Player.inventory:
            if check_command("use", "key") or check_command("unlock", "cellar") and Env.Outside.CELLAR_DOOR_LOCKED:
                Env.Outside.CELLAR_DOOR_LOCKED = False
                print("You unlock the cellar door with the key.")
                return True

    return False


@register_room(Room.CELLAR, GameText.RoomDescriptions.cellar)
def cellar():
    if go((["upstairs", "outside"], Room.OUTSIDE)):
        return True
    else:
        if look_around("cellar"):
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
            elif Env.Universal.ILLEGAL_CURRENCY_DISCOVERED:
                print("YOU HAVE LOST THE GAME.")
                exit(0)

            break


print("Game Complete! Congratulations!")
