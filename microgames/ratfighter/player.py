from microgames.ratfighter.enums import Menu
from random import randint


class Player:
    data = {
        "max health": 5,
        "current health": 5,
        "weapon": 2,
        "armor": 0,
        "accessory": 2,
        "credits": 1,
        "points": 0
    }

    # Player's current menu
    MENU = Menu.START

    @staticmethod
    def reset():
        Player.data = {
            "max health": 5,
            "current health": 5,
            "weapon": 2,
            "armor": 0,
            "accessory": 2,
            "credits": 1,
            "points": 0
        }

        Player.MENU = Menu.START

    @staticmethod
    def change_menu(menu: Menu):
        Player.MENU = menu

    @staticmethod
    def get_stats():
        out = "HEALTH: %s / %s\n" % (str(Player.data["current health"]), str(Player.data["max health"]))
        out += "WEAPON: %s\n" % str(Player.data["weapon"])
        out += "ARMOR: %s\n" % str(Player.data["armor"])
        out += "ACCESSORY: %s\n" % str(Player.data["accessory"])
        out += "CREDITS: %s\n" % str(Player.data["credits"])
        out += "POINTS: %s" % str(Player.data["points"])
        return out

    @staticmethod
    def heal():
        Player.data["current health"] = Player.data["max health"]
