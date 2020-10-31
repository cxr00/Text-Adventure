from enums import Room


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
    DRANK_PEPSI = False
    NEEDS_TO_POOP = False
    HAS_POOPED = False

    HAS_ILLEGAL_CURRENCY = False

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
        Player.DRANK_PEPSI = False
        Player.NEEDS_TO_POOP = False
        Player.HAS_POOPED = False

        Player.HAS_ILLEGAL_CURRENCY = False

        print("You have been reset.")

    @staticmethod
    def needs_to_poop():
        # Determines whether the player needs to use the toilet
        Player.NEEDS_TO_POOP = Player.EATEN_BURRITO and Player.EATEN_BANANA and Player.DRANK_PEPSI
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
        Player.credits += amount

    @staticmethod
    def take_credits(amount):
        Player.credits -= amount
