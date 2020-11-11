from enum import Enum


class Room(Enum):

    AT_MACHINE = 0
    AT_WORKBENCH = 1
    AT_COMPUTER = 2

    QUIT_GAME = 3

    NULL = 99

    @staticmethod
    def get(n):
        for room in Room:
            if room.value == n:
                return room
        return Room.NULL


class Computer:
    data = {
        "psu": False,
        "motherboard": False,
        "processor": False,
        "graphics card": False,
        "hard drive": False,
        "solid state drive": False,
        "ram": False
    }

    @staticmethod
    def is_fixed():
        return all(Computer.data.values())

    @staticmethod
    def reset():
        for each in Computer.data:
            Computer.data[each] = False
