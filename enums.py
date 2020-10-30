from enum import IntEnum


class Room(IntEnum):
    BEDROOM = 0
    BATHROOM = 1
    KITCHEN = 2
    VENDOR = 3
    MONETIZOR = 4
    TRASH_CAN = 5
    OUTSIDE = 6
    CELLAR = 7


class Item(IntEnum):
    WIDGET = 0

    BURRITO = 1
    BANANA = 2
    SODA = 3

    WRAPPER = 4
    PEEL = 5
    SODA_CAN = 6
    TRASH = 7

    KEY = 8


class Charm(IntEnum):
    GENERATE = 0
