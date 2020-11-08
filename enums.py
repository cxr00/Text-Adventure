from enum import Enum


# The set of rooms and room-like states
class Room(Enum):
    BEDROOM = "bedroom"
    BATHROOM = "bathroom"

    KITCHEN = "kitchen"
    VENDOR = "vendor"
    MONETIZOR = "monetizor"
    TRASH_CAN = "trash can"

    OUTSIDE = "outside"
    CELLAR = "cellar"

    DEBUG = "debug"
    NULL = "null"

    @staticmethod
    def get(s):
        for room in Room:
            if room.value == s:
                return room
        return Room.NULL


# The set of items which may appear in the player's inventory
class Item(Enum):
    WIDGET = "widget"

    BURRITO = "burrito"
    BURRITO_WRAPPER = "burrito wrapper"

    BANANA = "banana"
    PEELED_BANANA = "banana (peeled)"
    BANANA_PEEL = "banana peel"

    SODA = "soda"
    SODA_CAN = "soda can"

    TRASH = "trash"

    CELLAR_KEY = "cellar key"

    DEBUG = "debug"
    NULL = "null"

    @staticmethod
    def get(s):
        for item in Item:
            if item.value == s:
                return item
        return Item.NULL


# The set of charms which may appear in the player's charm box
class Charm(Enum):
    GENERATE = "generate"

    DEBUG = "debug"

    NULL = "null"

    @staticmethod
    def get(s):
        for charm in Charm:
            if charm.value == s:
                return charm
        return Charm.NULL
