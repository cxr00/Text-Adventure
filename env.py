import shelve
import os


def join_file_string(fs):
    return "_".join(fs) if isinstance(fs, list) else fs


class Env:

    class Universal:
        ILLEGAL_CURRENCY_DISCOVERED = False
        SUPER_ILLEGAL_ITEM_DISCOVERED = False

        @staticmethod
        def reset():
            Env.Universal.ILLEGAL_CURRENCY_DISCOVERED = False
            Env.Universal.SUPER_ILLEGAL_ITEM_DISCOVERED = False

    class Bedroom:

        @staticmethod
        def reset():
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

    class Debug:
        PLUNGUS_DECANTIFIED = False

        @staticmethod
        def reset():
            Env.Debug.PLUNGUS_DECANTIFIED = False

    @staticmethod
    def trash_is_full():
        Env.Kitchen.TRASH_FULL = Env.Kitchen.WRAPPER_IN_TRASH and Env.Kitchen.PEEL_IN_TRASH and Env.Kitchen.CAN_IN_TRASH
        return Env.Kitchen.TRASH_FULL

    @staticmethod
    def reset():
        Env.Universal.reset()

        Env.Bedroom.reset()
        Env.Bathroom.reset()
        Env.Kitchen.reset()
        Env.Outside.reset()
        Env.Cellar.reset()

        Env.Debug.reset()

    @staticmethod
    def save_game(file_string):
        file_string = join_file_string(file_string)
        with shelve.open("saves/" + file_string + "/env") as db:
            db["univ illegal currency discovered"] = Env.Universal.ILLEGAL_CURRENCY_DISCOVERED
            db["univ super illegal item discovered"] = Env.Universal.SUPER_ILLEGAL_ITEM_DISCOVERED

            db["bathroom sitting on toilet"] = Env.Bathroom.SITTING_ON_TOILET
            db["bathroom key on floor"] = Env.Bathroom.KEY_ON_FLOOR

            db["kitchen wrapper in trash"] = Env.Kitchen.WRAPPER_IN_TRASH
            db["kitchen peel in trash"] = Env.Kitchen.PEEL_IN_TRASH
            db["kitchen can in trash"] = Env.Kitchen.CAN_IN_TRASH
            db["kitchen trash full"] = Env.Kitchen.TRASH_FULL
            db["kitchen trash taken"] = Env.Kitchen.TRASH_TAKEN

            db["cellar charm on table"] = Env.Cellar.CHARM_ON_TABLE

            db["debug plungus decantified"] = Env.Debug.PLUNGUS_DECANTIFIED

    @staticmethod
    def load_game(file_string):
        file_string = join_file_string(file_string)

        if os.path.exists("saves/" + file_string + "/env.dat"):
            with shelve.open("saves/" + file_string + "/env") as db:
                Env.Universal.ILLEGAL_CURRENCY_DISCOVERED = bool(db["univ illegal currency discovered"])
                Env.Universal.SUPER_ILLEGAL_ITEM_DISCOVERED = bool(db["univ super illegal item discovered"])

                Env.Bathroom.SITTING_ON_TOILET = bool(db["bathroom sitting on toilet"])
                Env.Bathroom.KEY_ON_FLOOR = bool(db["bathroom key on floor"])

                Env.Kitchen.WRAPPER_IN_TRASH = bool(db["kitchen wrapper in trash"])
                Env.Kitchen.PEEL_IN_TRASH = bool(db["kitchen peel in trash"])
                Env.Kitchen.CAN_IN_TRASH = bool(db["kitchen can in trash"])
                Env.Kitchen.TRASH_FULL = bool(db["kitchen trash full"])
                Env.Kitchen.TRASH_TAKEN = db["kitchen trash taken"]

                Env.Cellar.CHARM_ON_TABLE = bool(db["cellar charm on table"])

                Env.Debug.PLUNGUS_DECANTIFIED = bool(db["debug plungus decantified"])
            return True
        else:
            print("Save file %s does not exist" % "_".join(file_string))
            return False