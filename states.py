
class Env:

    class Universal:
        ILLEGAL_CURRENCY_DISCOVERED = False
        SUPER_ILLEGAL_ITEM_DISCOVERED = False

        @staticmethod
        def reset():
            Env.Universal.ILLEGAL_CURRENCY_DISCOVERED = False
            Env.Universal.SUPER_ILLEGAL_ITEM_DISCOVERED = False

    class Bedroom:
        pass

    class Bathroom:
        SITTING_ON_TOILET = False
        KEY_ON_FLOOR = True

        @staticmethod
        def reset():
            Env.Bathroom.SITTING_ON_TOILET = False
            Env.Bathroom.KEY_ON_FLOOR = True

    class Kitchen:
        WRAPPER_IN_TRASH = False
        PEEL_IN_TRASH = False
        CAN_IN_TRASH = False
        TRASH_FULL = False
        TRASH_TAKEN = False

        @staticmethod
        def reset():
            Env.Kitchen.WRAPPER_IN_TRASH = False
            Env.Kitchen.PEEL_IN_TRASH = False
            Env.Kitchen.CAN_IN_TRASH = False
            Env.Kitchen.TRASH_FULL = False
            Env.Kitchen.TRASH_TAKEN = False

    class Outside:
        TRASH_IN_BIN = False
        CELLAR_DOOR_LOCKED = True

        @staticmethod
        def reset():
            Env.Outside.TRASH_IN_BIN = False
            Env.Outside.CELLAR_DOOR_LOCKED = True

    class Cellar:
        CHARM_ON_TABLE = True

        @staticmethod
        def reset():
            Env.Cellar.CHARM_ON_TABLE = True

    @staticmethod
    def trash_is_full():
        Env.Kitchen.TRASH_FULL = Env.Kitchen.WRAPPER_IN_TRASH and Env.Kitchen.PEEL_IN_TRASH and Env.Kitchen.CAN_IN_TRASH
        return Env.Kitchen.TRASH_FULL

    @staticmethod
    def reset():
        Env.Universal.reset()
        Env.Bathroom.reset()
        Env.Kitchen.reset()
        Env.Outside.reset()
        Env.Cellar.reset()
