from enum import Enum, auto


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


# The set of items which may appear in the player's inventory
class Item(Enum):
    WIDGET = "widget"

    BURRITO = "burrito"
    BURRITO_WRAPPER = "burrito wrapper"

    BANANA = "banana"
    PEELED_BANANA = "peeled banana"
    BANANA_PEEL = "banana peel"

    SODA = "soda"
    SODA_CAN = "soda can"

    TRASH = "trash"

    CELLAR_KEY = "cellar key"


# The set of charms which may appear in the player's charm box
class Charm(Enum):
    GENERATE = "generate"
