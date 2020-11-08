from microgames.ratfighter.enums import Menu
from random import randint
import shelve


class Player:

    # Player health, measures how alive they are
    MAX_HEALTH = 5
    CURRENT_HEALTH = 5

    # Max damage potential
    WEAPON = 2

    # Max defense potential
    ARMOR = 0

    # Max loot potential
    ACCESSORY = 2

    # In-game currency in your possession
    CREDITS = 1

    # Points which determine main game reward
    POINTS = 0

    # Player's current menu
    MENU = Menu.START

    @staticmethod
    def save_game():
        with shelve.open("saves/ratfighter") as db:
            db["max health"] = Player.MAX_HEALTH
            db["current health"] = Player.CURRENT_HEALTH

            db["weapon"] = Player.WEAPON
            db["armor"] = Player.ARMOR
            db["accessory"] = Player.ACCESSORY

            db["credits"] = Player.CREDITS
            db["points"] = Player.POINTS

            db["menu"] = Player.MENU.value

    @staticmethod
    def load_game():
        with shelve.open("saves/ratfighter") as db:
            Player.MAX_HEALTH = db["max health"]
            Player.CURRENT_HEALTH = db["current health"]

            Player.WEAPON = db["weapon"]
            Player.ARMOR = db["armor"]
            Player.ACCESSORY = db["accessory"]

            Player.CREDITS = db["credits"]
            Player.POINTS = db["points"]

    @staticmethod
    def reset():
        Player.MAX_HEALTH = 5
        Player.CURRENT_HEALTH = 5
        Player.WEAPON = 2
        Player.ARMOR = 0
        Player.ACCESSORY = 2
        Player.CREDITS = 1
        Player.MENU = Menu.START

    @staticmethod
    def change_menu(menu: Menu):
        Player.MENU = menu

    @staticmethod
    def get_stats():
        out = "HEALTH: %s / %s\n" % (str(Player.CURRENT_HEALTH),str(Player.MAX_HEALTH))
        out += "WEAPON: %s\n" % str(Player.WEAPON)
        out += "ARMOR: %s\n" % str(Player.ARMOR)
        out += "ACCESSORY: %s\n" % str(Player.ACCESSORY)
        out += "CREDITS: %s\n" % str(Player.CREDITS)
        out += "POINTS: %s" % str(Player.POINTS)
        return out

    @staticmethod
    def heal():
        Player.CURRENT_HEALTH = Player.MAX_HEALTH

    @staticmethod
    def get_credit_reward(base_amount):
        out = randint(1, Player.ACCESSORY) + base_amount
        Player.CREDITS += out
        return out

