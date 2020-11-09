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

    PSU = False
    MOTHERBOARD = False
    PROCESSOR = False
    GRAPHICS_CARD = False
    HARD_DRIVE = False
    SOLID_STATE_DRIVE = False
    RAM = False

    @staticmethod
    def computer_is_fixed():
        return Computer.PSU\
               and Computer.MOTHERBOARD \
               and Computer.PROCESSOR \
               and Computer.GRAPHICS_CARD \
               and Computer.HARD_DRIVE \
               and Computer.SOLID_STATE_DRIVE \
               and Computer.RAM
