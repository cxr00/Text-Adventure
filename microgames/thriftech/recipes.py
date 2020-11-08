

class MaterialRecipe:
    CIRCUIT_BOARD = (("glass", 2), ("plastic", 2), ("copper wire", 1))
    CABLE = (("copper wire", 3), ("plastic", 2))
    MICROCHIP = (("scrap metal", 2), ("plastic", 2), ("glass", 2))
    CAPACITOR = (("scrap metal", 2), ("copper wire", 1), ("glass", 1))
    CASING = (("scrap metal", 4), ("plastic", 2), ("glass", 1))


class ComponentRecipe:
    PSU = (("casing", 1), ("cable", 2), ("capacitor", 3))
    MOTHERBOARD = (("circuit board", 2), ("cable", 1), ("microchip", 1))
    PROCESSOR = (("microchip", 2), ("cable", 2), ("capacitor", 1))
    GRAPHICS_CARD = (("casing", 1), ("microchip", 2), ("circuit board", 1))
    HARD_DRIVE = (("casing", 1), ("circuit board", 1), ("cable", 2))
    SOLID_STATE_DRIVE = (("casing", 1), ("circuit board", 1), ("microchip", 1))
    RAM = (("microchip", 1), ("cable", 1), ("circuit board", 1))


