import shelve
import os


def join_file_string(fs):
    return "_".join(fs) if isinstance(fs, list) else fs


class Env:

    class Universal:

        @staticmethod
        def reset():
            pass

    class Bedroom:

        @staticmethod
        def reset():
            pass

    class RatFighter:
        DISPENSED_CHARM = False
        POINTS = 0

        @staticmethod
        def reset():
            Env.RatFighter.DISPENSED_CHARM = False
            Env.RatFighter.POINTS = 0

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

    class ThrifTech:
        COMPLETE = False
        REWARD_GIVEN = False

        @staticmethod
        def reset():
            Env.ThrifTech.COMPLETE = False
            Env.ThrifTech.REWARD_GIVEN = False

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
        Env.RatFighter.reset()
        Env.ThrifTech.reset()

    @staticmethod
    def save_game(file_string):
        file_string = join_file_string(file_string)
        with shelve.open("saves/" + file_string + "/env") as db:

            db["bathroom sitting on toilet"] = Env.Bathroom.SITTING_ON_TOILET
            db["bathroom key on floor"] = Env.Bathroom.KEY_ON_FLOOR

            db["kitchen wrapper in trash"] = Env.Kitchen.WRAPPER_IN_TRASH
            db["kitchen peel in trash"] = Env.Kitchen.PEEL_IN_TRASH
            db["kitchen can in trash"] = Env.Kitchen.CAN_IN_TRASH
            db["kitchen trash full"] = Env.Kitchen.TRASH_FULL
            db["kitchen trash taken"] = Env.Kitchen.TRASH_TAKEN

            db["outside trash in bin"] = Env.Outside.TRASH_IN_BIN
            db["outside cellar door locked"] = Env.Outside.CELLAR_DOOR_LOCKED

            db["cellar charm on table"] = Env.Cellar.CHARM_ON_TABLE

            db["debug plungus decantified"] = Env.Debug.PLUNGUS_DECANTIFIED

            db["ratfighter dispensed charm"] = Env.RatFighter.DISPENSED_CHARM
            db["ratfighter points"] = Env.RatFighter.POINTS

            db["thriftech complete"] = Env.ThrifTech.COMPLETE
            db["thriftech reward given"] = Env.ThrifTech.REWARD_GIVEN

    @staticmethod
    def load_game(file_string):
        file_string = join_file_string(file_string)

        if os.path.exists("saves/" + file_string + "/env.dat"):
            with shelve.open("saves/" + file_string + "/env") as db:

                Env.Bathroom.SITTING_ON_TOILET = bool(db["bathroom sitting on toilet"])
                Env.Bathroom.KEY_ON_FLOOR = bool(db["bathroom key on floor"])

                Env.Kitchen.WRAPPER_IN_TRASH = bool(db["kitchen wrapper in trash"])
                Env.Kitchen.PEEL_IN_TRASH = bool(db["kitchen peel in trash"])
                Env.Kitchen.CAN_IN_TRASH = bool(db["kitchen can in trash"])
                Env.Kitchen.TRASH_FULL = bool(db["kitchen trash full"])
                Env.Kitchen.TRASH_TAKEN = db["kitchen trash taken"]

                Env.Outside.TRASH_IN_BIN = bool(db["outside trash in bin"])
                Env.Outside.CELLAR_DOOR_LOCKED = bool(db["outside cellar door locked"])

                Env.Debug.PLUNGUS_DECANTIFIED = bool(db["debug plungus decantified"])

                Env.RatFighter.DISPENSED_CHARM = bool(db["ratfighter dispensed charm"])
                Env.RatFighter.POINTS = int(db["ratfighter points"])

                Env.ThrifTech.COMPLETE = bool(db["thriftech complete"])
                Env.ThrifTech.REWARD_GIVEN = bool(db["thriftech reward given"])
            return True
        else:
            print("Save file %s does not exist" % "_".join(file_string))
            return False
