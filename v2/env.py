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
        "ratfighter":
            {
                "max health": 5,
                "current health": 5,
                "weapon": 2,
                "armor": 0,
                "accessory": 2,
                "credits": 1,
                "points": 0
            },
        "games":
            {
                "ratfighter": True,
                "thriftech": False
            },
        "bedroom":
            {
                "bed made": False,
                "room tidied": False
            },
        "bathroom":
            {
                "thriftech": True
            },
        "kitchen":
            {

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
