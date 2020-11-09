from enums import *
from player import Player, view_save_files
from env import Env
from words import Words, GameText

from microgames.ratfighter.game import run_ratfighter_21xx
from microgames.thriftech.game import run_thriftech

ROOMS = {}
DESC = {}

end = False
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


def go(*loc):
    """
    Changes room based on given loc as long as the command starts with 'go' or 'go to'
    :param loc: The possible locations to travel and their associated commands
    """
    if check_cmd("go"):
        n = 2 if cmd[1] == "to" else 1
        for e in loc:
            # Synonym engine
            # Returns True if there is at least one match
            if isinstance(e[0], list):
                if cmd[n] in e[0]:
                    Player.change_room(e[1])
                    return True
            elif cmd[n] == e[0]:
                Player.change_room(e[1])
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


# All commands associated with items in the player's inventory
def inventory_check():

    def check_need_to_poop():
        if Player.needs_to_poop():
            print("Your tummy gurgles. Probably need a bathroom.")

    if Player.has_item(Item.WIDGET):
        if look("widget"):
            print("It is a widget. Fascinating. You can PROCESS this.")
            return True
        elif check_cmd("process", "widget"):
            Player.give_credits(8)
            Player.take_item(Item.WIDGET)
            Player.HAS_ILLEGAL_CURRENCY = True
            print("You process the widget. You earn 8 credits!")
            return True

    if Player.has_item(Item.BURRITO):
        if look("burrito"):
            print("A burrito from the vendor.")
            return True
        elif check_cmd("eat", "burrito"):
            Player.take_item(Item.BURRITO)
            Player.EATEN_BURRITO = True
            print("You eat the burrito. Scrumptch!")
            Player.give_item(Item.BURRITO_WRAPPER)
            print("You are left with the burrito WRAPPER.")
            check_need_to_poop()
            return True

    if Player.has_item(Item.SODA):
        if look("soda"):
            print("A pepsi from the vendor.")
            return True
        elif check_cmd("drink", "soda"):
            Player.take_item(Item.SODA)
            Player.DRANK_SODA = True
            print("You drink the soda. Scrumptch!")
            Player.give_item(Item.SODA_CAN)
            print("You are left with the soda CAN.")
            check_need_to_poop()
            return True

    if Player.has_item([Item.BANANA, Item.PEELED_BANANA]):
        if look("banana"):
            print("A banana from the vendor.")
            if Player.has_item(Item.BANANA):
                print("I need to PEEL it.")
            return True
        elif check_cmd("eat", "banana"):
            if Player.has_item(Item.PEELED_BANANA):
                Player.take_item(Item.PEELED_BANANA)
                Player.EATEN_BANANA = True
                print("You eat the banana. Scrumptch!")
                check_need_to_poop()
                return True
            elif Player.has_item(Item.BANANA):
                print("You need to PEEL it first.")
                return True
        elif check_cmd("peel", "banana"):
            Player.take_item(Item.BANANA)
            Player.give_item(Item.PEELED_BANANA)
            Player.give_item(Item.BANANA_PEEL)
            print("You peel the banana.")
            print("You are left with a peeled banana and a banana peel.")
            return True

    return False


# All commands associated with the charms in the player's possession
def charm_check():
    if Player.has_charm(Charm.GENERATE):
        if check_cmd("generate"):
            if not Player.has_item(Item.WIDGET):
                Player.give_item(Item.WIDGET)
                print("You generate a widget.")
            else:
                print("You already have a widget in your possession.")
            return True

    return False


# Additional utility commands
def misc_check():
    if check_cmd("credits") or look("credits") or check_cmd("check", "credits"):
        print("You have %s credits." % Player.credits)
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

    # META COMMANDS
    elif check_cmd("reset"):
        Player.reset()
        Env.reset()
        return True
    elif check_cmd("save"):
        Player.save_game(cmd[1:])
        Env.save_game(cmd[1:])
        print("You have saved the game \"%s\"." % " ".join(cmd[1:]))
        return True
    elif check_cmd("load"):
        Player.save_game("temp001")
        if Player.load_game(cmd[1:]):
            Env.save_game("temp001")
            if Env.load_game(cmd[1:]):
                print("You have loaded the save game \"%s\"." % " ".join(cmd[1:]))
            else:
                Env.load_game("temp001")
                print("Failed to load ENV of save game \"%s\"." % " ".join(cmd[1:]))
        else:
            Player.load_game("temp001")
            print("Failed to load PLAYER of save game \"%s\"." % " ".join(cmd[1:]))
        return True
    elif check_cmd(["view", "look"], ["save", "saves"]):
        view_save_files()
        return True
    elif check_cmd(["quit", "exit"]):
        really_quit = input("Are you sure you want to quit? (y/n)\n>>> ")
        if really_quit[0] == "y":
            exit(0)
        else:
            return True
    # Whatever I need to speed up testing
    elif check_cmd("debug") and Player.DEBUG:
        Player.change_room(Room.CELLAR)
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
            elif not f():
                print("I don't understand \"%s\"." % " ".join(cmd))

        return wrapper

    # registers the room's associated function for dictionary traversal
    def register_function(f):
        ROOMS[room] = universal_check(f)

    return register_function


@register_room(Room.BEDROOM, GameText.RoomDescriptions.bedroom)
def bedroom():
    if go(
        ("bathroom", Room.BATHROOM),
        ("kitchen", Room.KITCHEN)
    ):
        return True
    else:
        if look_around("bedroom"):
            print("It is your bedroom.")
            print("The door to your bathroom is open.")
            print("The door to your kitchen is also open.")
            print("You could PLAY RATFIGHTER.")
            return True
        elif look("floor"):
            print("There is nothing on the floor.")
            return True
        elif check_cmd("play", "ratfighter"):
            Env.RatFighter.POINTS = run_ratfighter_21xx(Env.RatFighter.POINTS)
            if Env.RatFighter.POINTS >= 50 and not Env.RatFighter.DISPENSED_CHARM:
                Player.give_charm(Charm.DECANTIFY)
                Env.RatFighter.DISPENSED_CHARM = True
                print("You are rewarded with DECANTIFY.")
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
                print("There is a KEY on the floor.")
            return True
        elif look("floor"):
            if Env.Bathroom.KEY_ON_FLOOR:
                print("There is a KEY on the floor.")
            else:
                print("There is nothing on the floor.")
            return True
        elif check_cmd("sit", "toilet"):
            Env.Bathroom.SITTING_ON_TOILET = True
            print("You sit on the toilet.")
            return True
        elif check_cmd(Words.TAKE, "key"):
            if Env.Bathroom.KEY_ON_FLOOR:
                Player.give_item(Item.CELLAR_KEY)
                Env.Bathroom.KEY_ON_FLOOR = False
                print("You pick up the key from the floor.")
            else:
                print("There is nothing on the floor.")
            return True
    else:
        if check_cmd(["poop", "shit"]) or check_cmd("take", ["dump", "shit"]):
            if Player.NEEDS_TO_POOP:
                Player.NEEDS_TO_POOP = False
                Player.HAS_POOPED = True
                print("Ah, sweet relief!")
            else:
                print("You don't need to do that right now.")
            return True
        elif check_cmd("stand"):
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
            else:
                print("There is nothing on the floor.")
            return True

    return False


@register_room(Room.KITCHEN, GameText.RoomDescriptions.kitchen)
def kitchen():
    if go(
          ("bedroom", Room.BEDROOM),
          ("vendor", Room.VENDOR),
          ("monetizor", Room.MONETIZOR),
          (["outside", "out"], Room.OUTSIDE),
          ("trash", Room.TRASH_CAN)
    ):
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
        elif check_cmd(["look", "use"], "trash") or check_cmd("throw", "away", "trash"):
            Player.change_room(Room.TRASH_CAN)
            return True

    return False


@register_room(Room.VENDOR, GameText.RoomDescriptions.vendor)
def vendor():

    # def check_for_illegal_currency():
    #     if Player.HAS_ILLEGAL_CURRENCY:
    #         print("The vendor booms in a loud voice:")
    #         print("ILLEGAL CURRENCY DETECTED. PREPARE TO BE TAKEN INTO CUSTODY.")
    #         print("...")
    #         print("Suddenly two robot officers appear and arrest you.")
    #         print("You shouldn't have used that contraband CHARM!")
    #         Env.Universal.ILLEGAL_CURRENCY_DISCOVERED = True
    #         return True
    #     return False

    def buy(item):
        if Player.credits >= 10:
            Player.take_credits(10)
            Player.give_item(item)
            print("You buy a %s." % item.value)
        else:
            print("You cannot afford the %s." % item.value)
        return True

    if check_cmd("buy", "burrito"):
        return buy(Item.BURRITO)
    elif check_cmd("buy", "banana"):
        return buy(Item.BANANA)
    elif check_cmd("buy", "soda"):
        return buy(Item.SODA)

    if look_around("vendor"):
        print("There is a sticker on the vendor which reads:")
        print("Remember: Illegal Currency is Illegal.")
        print("The vendor contains: BURRITO, BANANA, and SODA.")
        return True
    if check_cmd("leave") or check_cmd("go", "kitchen"):
        Player.change_room(Room.KITCHEN)
        return True

    return False


@register_room(Room.MONETIZOR, GameText.RoomDescriptions.monetizor)
def monetizor():

    if go(("kitchen", Room.KITCHEN)):
        return True
    elif look_around("monetizor"):
        print("There is a sticker on the side of the monetizor which reads:")
        print("INSERT contraband for a credit reward.")
        return True
    elif check_cmd("leave"):
        Player.change_room(Room.KITCHEN)
        return True

    if Player.has_charm(Charm.GENERATE):
        if check_cmd(Words.INSERT, ["charm", "generate"]):
            Player.give_credits(50)
            Player.take_charm(Charm.GENERATE)
            print("You put the generate charm into the monetizor.")
            print("It whirs and spits out 50 credits. Sweet!")
            Player.change_room(Room.KITCHEN)
            return True

    if Player.has_item(Item.WIDGET):
        if check_cmd(Words.INSERT, "widget"):
            Player.give_credits(5)
            Player.take_item(Item.WIDGET)
            print("You put the widget into the monetizor.")
            print("It whirs and spits out 5 credits. Not bad.")
            return True

    return False


@register_room(Room.TRASH_CAN, GameText.RoomDescriptions.trash_can)
def trash_can():

    def check_trash_is_full():
        if Env.trash_is_full() and not Env.Kitchen.TRASH_TAKEN:
            print("The trash is full. Better TAKE it out.")

    if go(("kitchen", Room.KITCHEN)):
        return True
    elif check_cmd("leave"):
        Player.change_room(Room.KITCHEN)
        return True
    elif look_around("trash"):
        if Env.trash_is_full():
            if Env.Kitchen.TRASH_TAKEN:
                print("The trash can is empty.")
            else:
                print("The trash can is full.")
        else:
            print("There's still a bit of room in the trash can.")
        return True
    elif check_cmd(Words.TAKE, "trash") and Env.trash_is_full() and not Env.Kitchen.TRASH_TAKEN:
        Player.give_item(Item.TRASH)
        Env.Kitchen.TRASH_TAKEN = True
        print("You take the TRASH bag out of the can.")
        print("The garbage bin is OUTSIDE.")
        Player.change_room(Room.KITCHEN)
        return True

    if Item.BURRITO_WRAPPER in Player.inventory:
        if check_cmd("toss", "wrapper") or check_cmd("throw", "away", "wrapper"):
            Player.take_item(Item.BURRITO_WRAPPER)
            Env.Kitchen.WRAPPER_IN_TRASH = True
            print("You throw away the burrito wrapper.")
            check_trash_is_full()
            return True
    if Item.BANANA_PEEL in Player.inventory:
        if check_cmd("toss", "peel") or check_cmd("throw", "away", "peel"):
            Player.take_item(Item.BANANA_PEEL)
            Env.Kitchen.PEEL_IN_TRASH = True
            print("You throw away the banana peel.")
            check_trash_is_full()
            return True
    if Item.SODA_CAN in Player.inventory:
        if check_cmd("toss", "can") or check_cmd("throw", "away", "can"):
            Player.take_item(Item.SODA_CAN)
            Env.Kitchen.CAN_IN_TRASH = True
            print("You throw away the soda can.")
            check_trash_is_full()
            return True

    return False


@register_room(Room.OUTSIDE, GameText.RoomDescriptions.outside)
def outside():
    if go((["inside", "in", "kitchen"], Room.KITCHEN), (["portal", "nether"], Room.DEBUG)):
        return True
    else:
        if look_around("outside"):
            print("Ah, to be outside.")
            print("The trash bin is on your left.")
            if Env.Outside.TRASH_IN_BIN:
                print("The trash is in the bin.")
            print("The CELLAR is on your right.")
            print("A strange PORTAL to the NETHER is also present for some reason.")
            return True
        elif look(["floor", "ground"]):
            print("There is nothing on the ground.")
            return True
        elif check_cmd("go", "cellar") or check_cmd("go", "to", "cellar"):
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
            if check_cmd("toss", "trash") or check_cmd("throw", "away", "trash"):
                Player.take_item(Item.TRASH)
                Env.Outside.TRASH_IN_BIN = True
                print("You throw away the trash in the bin. Chores done!")
                return True

        if Item.CELLAR_KEY in Player.inventory:
            if check_cmd("use", "key") or check_cmd("unlock", "cellar") and Env.Outside.CELLAR_DOOR_LOCKED:
                Env.Outside.CELLAR_DOOR_LOCKED = False
                print("You unlock the cellar door with the key.")
                return True

    return False


@register_room(Room.CELLAR, GameText.RoomDescriptions.cellar)
def cellar():
    if go((["upstairs", "outside", "out"], Room.OUTSIDE)):
        return True
    else:
        if look_around("cellar"):
            print("It's mostly empty, but there's a few pieces of old furniture.")
            print("There is a THRIFTECH entertainment module.")
            return True
        elif check_cmd("play", "thriftech"):
            Env.ThrifTech.COMPLETE = run_thriftech()
            if Env.ThrifTech.COMPLETE and not Env.ThrifTech.REWARD_GIVEN:
                Player.give_charm(Charm.GENERATE)
                Env.ThrifTech.REWARD_GIVEN = True
                print("You are rewarded with a GENERATE charm.")
            return True
        # elif check_cmd(Words.TAKE, "charm") and Env.Cellar.CHARM_ON_TABLE:
        #     Player.give_charm(Charm.GENERATE)
        #     Env.Cellar.CHARM_ON_TABLE = False
        #     print("You take the GENERATE charm from the table.")
        #     return True

    return False


@register_room(Room.DEBUG, GameText.RoomDescriptions.test_room)
def test_room():
    if go((["away", "out", "portal", "outside"], Room.OUTSIDE)):
        return True
    elif look_around(["room", "area", "nether"]):
        print("You are in a very nether-y place.")
        print("You don't know why you went through the portal to begin with.")
        if Env.Debug.PLUNGUS_DECANTIFIED:
            print("The plungus has been decantified.")
        return True
    elif look("floor"):
        print("There are windy, curly mushrooms growing all over.")
        print("You don't want to touch any of them.")
        return True
    elif check_cmd("use", "decantify"):
        if Player.has_charm(Charm.DECANTIFY) and not Env.Debug.PLUNGUS_DECANTIFIED:
            Env.Debug.PLUNGUS_DECANTIFIED = True
            print("You employ the charm's powers to decantify the plungus.")
        else:
            print("You have no such charm to use.")
        return True
    elif check_cmd("check", ["state", "plungus"]):
        if Env.Debug.PLUNGUS_DECANTIFIED:
            print("The plungus is decantified.")
        else:
            print("The plungus is NOT decantified.")
        return True


def run_game():
    global end
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
                if Env.Outside.TRASH_IN_BIN and Player.HAS_POOPED and Env.Debug.PLUNGUS_DECANTIFIED:
                    end = True

                break
    print("Game Complete! Congratulations!")


run_game()
