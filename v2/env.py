from enum import Enum
import json
import os


class Room(Enum):
    BEDROOM = "bedroom"
    BATHROOM = "bathroom"
    KITCHEN = "kitchen"

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
                "current room": "bedroom",
                "previous room": None
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
                        "storio": True
                    },
                "completed":
                    {
                        "ratfighter": False,
                        "thriftech": False,
                        "stox": False,
                        "vocabuloid": False,
                        "growlike": False,
                        "storio": False
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
        for each in save_games:
            print(each)
