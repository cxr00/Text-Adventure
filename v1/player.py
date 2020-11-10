from v1.enums import Room, Charm, Item
import shelve
import os


def check_for_save_folder(fs=""):
    if not os.path.exists("../saves"):
        os.mkdir("../saves")
    if not os.path.exists("saves/" + fs):
        os.mkdir("saves/" + fs)


def join_file_string(fs):
    return "_".join(fs) if isinstance(fs, list) else fs


def view_save_files():
    check_for_save_folder()
    l = os.listdir("../saves/")
    out = []
    for each in l:
        name = " ".join(each.split("_"))
        if name not in out and name != "temp001":
            out.append(name)
    print("SAVE FILES:")
    for each in out:
        print(each)


class Player:

    # Player variables
    credits = 0
    inventory = []
    charms = []
    location = Room.BEDROOM
    previous_loc = None

    # Poop conditions
    EATEN_BURRITO = False
    EATEN_BANANA = False
    DRANK_SODA = False
    NEEDS_TO_POOP = False
    HAS_POOPED = False

    HAS_ILLEGAL_CURRENCY = False

    DEBUG = True

    @staticmethod
    def reset():
        # Player variables
        Player.credits = 0
        Player.inventory = []
        Player.charms = []
        Player.location = Room.BEDROOM
        Player.previous_loc = None

        # Poop conditions
        Player.EATEN_BURRITO = False
        Player.EATEN_BANANA = False
        Player.DRANK_SODA = False
        Player.NEEDS_TO_POOP = False
        Player.HAS_POOPED = False

        Player.HAS_ILLEGAL_CURRENCY = False

        Player.DEBUG = True

        print("You have been reset.")

    @staticmethod
    def save_game(file_string):
        check_for_save_folder()
        file_string = join_file_string(file_string)
        check_for_save_folder(file_string)

        with shelve.open("saves/" + file_string + "/player") as db:
            db["credits"] = Player.credits
            db["inventory"] = [i.value for i in Player.inventory]
            db["charms"] = [c.value for c in Player.charms]
            db["location"] = Player.location.value

            db["eaten burrito"] = Player.EATEN_BURRITO
            db["eaten banana"] = Player.EATEN_BANANA
            db["drank soda"] = Player.DRANK_SODA
            db["needs to poop"] = Player.NEEDS_TO_POOP
            db["has pooped"] = Player.HAS_POOPED

            db["has illegal currency"] = Player.HAS_ILLEGAL_CURRENCY

            db["test state"] = Player.DEBUG

    @staticmethod
    def load_game(file_string):
        check_for_save_folder()
        file_string = join_file_string(file_string)
        check_for_save_folder(file_string)

        if os.path.exists("saves/" + file_string + "/player.dat"):
            with shelve.open("saves/" + file_string + "/player") as db:
                Player.credits = int(db["credits"])

                inventory = db["inventory"]
                Player.inventory = [Item.get(i) for i in inventory]

                charms = db["charms"]
                Player.charms = [Charm.get(c) for c in charms]

                Player.location = Room.get(db["location"])
                Player.EATEN_BURRITO = bool(db["eaten burrito"])
                Player.EATEN_BANANA = bool(db["eaten banana"])
                Player.DRANK_SODA = bool(db["drank soda"])
                Player.NEEDS_TO_POOP = bool(db["needs to poop"])
                Player.HAS_POOPED = bool(db["has pooped"])

                Player.HAS_ILLEGAL_CURRENCY = bool(db["has illegal currency"])

                Player.DEBUG = bool(db["test state"])
            return True
        else:
            print("Save file %s does not exist." % file_string)
            return False

    @staticmethod
    def needs_to_poop():
        # Determines whether the player needs to use the toilet
        Player.NEEDS_TO_POOP = Player.EATEN_BURRITO and Player.EATEN_BANANA and Player.DRANK_SODA
        return Player.NEEDS_TO_POOP

    @staticmethod
    def change_room(new_room):
        Player.previous_loc, Player.location = Player.location, new_room

    @staticmethod
    def give_item(item):
        # Add an item to the inventory
        Player.inventory.append(item)

    @staticmethod
    def take_item(item):
        # Remove an item from the inventory
        Player.inventory.pop(Player.inventory.index(item))

    @staticmethod
    def give_charm(charm):
        # Add a charm to your possession
        Player.charms.append(charm)

    @staticmethod
    def take_charm(charm):
        # Remove a charm from your possession
        Player.charms.pop(Player.charms.index(charm))

    @staticmethod
    def give_credits(amount):
        # Add an amount of credits to your possession
        Player.credits += amount

    @staticmethod
    def take_credits(amount):
        # Take an amount of credits from your possession
        Player.credits -= amount

    @staticmethod
    def has_item(item):
        if isinstance(item, list):
            for e in item:
                if e in Player.inventory:
                    return True
            return False
        return item in Player.inventory

    @staticmethod
    def has_charm(charm):
        if isinstance(charm, list):
            for e in charm:
                if e in Player.charms:
                    return True
            return False
        return charm in Player.charms
