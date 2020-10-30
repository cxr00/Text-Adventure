
class Env:

    class Bathroom:
        SITTING_ON_TOILET = False
        KEY_ON_FLOOR = True

    class Bedroom:
        pass

    class Kitchen:
        WRAPPER_IN_TRASH = False
        PEEL_IN_TRASH = False
        CAN_IN_TRASH = False
        TRASH_FULL = False
        TRASH_TAKEN = False

    class Outside:
        TRASH_IN_BIN = False
        CELLAR_DOOR_LOCKED = True

    class Cellar:
        CHARM_ON_TABLE = True

    @staticmethod
    def trash_is_full():
        Env.Kitchen.TRASH_FULL = Env.Kitchen.WRAPPER_IN_TRASH and Env.Kitchen.PEEL_IN_TRASH and Env.Kitchen.CAN_IN_TRASH
        return Env.Kitchen.TRASH_FULL

