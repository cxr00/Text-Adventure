from enum import Enum


class Menu(Enum):

    START = "start"
    ACTION = "action"
    SHOP = "shop"
    FIGHT = "fight"
    BATTLE = "battle"

    NULL = "null"

    @staticmethod
    def get(s):
        for menu in Menu:
            if menu.value == s:
                return menu
        return Menu.NULL
