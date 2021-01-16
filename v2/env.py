from enum import Enum
import json
import os


class Room(Enum):
    BEDROOM = "bedroom"
    BATHROOM = "bathroom"
    KITCHEN = "kitchen"
    CHAMBER = "chamber"

    NULL = "null"

    @staticmethod
    def get(s):
        for room in Room:
            if room.value == s:
                return room
        return Room.NULL


class Env:
    data = {
        "player":
            {
                "location": "chamber",
                "previous location": None
            },
        "games":
            {
                "owned":
                    {
                        "ratfighter": True,
                        "thriftech": True,
                        "stox": True,
                        "vocabuloid": True,
                        "growlike": True,
                        "storio": True,
                        "farmageddon": True
                    },
                "completed":
                    {
                        "ratfighter": False,
                        "thriftech": False,
                        "stox": False,
                        "vocabuloid": False,
                        "growlike": False,
                        "storio": False,
                        "farmageddon": False
                    }
            },
        "ratfighter": None,
        "thriftech": None,
        "stox": None,
        "vocabuloid":
            {
                "best time": 0
            },
        "storio": None,
        "farmageddon": None,
        "bedroom":
            {
                "bed made": False,
                "room tidied": False
            },
        "bathroom":
            {
                "thriftech": False
            }
    }

    @staticmethod
    def save(file_name):
        if not os.path.exists("saves"):
            os.mkdir("saves")
        with open("saves/%s_env.json" % "_".join(file_name), "w+") as fp:
            json.dump(Env.data, fp)
        return True

    @staticmethod
    def load(file_name):
        if not os.path.exists("saves"):
            os.mkdir("saves")
        try:
            with open("saves/%s_env.json" % "_".join(file_name), "r+") as fp:
                Env.data = json.load(fp)
        except FileNotFoundError:
            return False
        return True

    @staticmethod
    def show_saves():
        save_games = []
        if not os.path.exists("saves"):
            os.mkdir("saves")
        for each in os.listdir("saves"):
            name = " ".join(each.split("_")[:-1])
            if name not in save_games:
                save_games.append(name)
        if len(save_games) == 0:
            print("You have no save games.")
        else:
            for each in save_games:
                print(each)

    @staticmethod
    def change_room(new_room):
        Env.data["player"]["previous location"] = Env.data["player"]["location"]
        Env.data["player"]["location"] = new_room.value
