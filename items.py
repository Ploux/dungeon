#!/usr/bin/env python3

import random
import graphics

class Treasure:
    def __init__(self, x, y, treasure_type):
        self.x = x
        self.y = y
        self.type = treasure_type
        if treasure_type == "gold":
            self.value = random.randint(10, 50)
            self.color = graphics.YELLOW
        elif treasure_type == "health":
            self.value = random.randint(20, 50)
            self.color = graphics.RED
        elif treasure_type == "sword":
            self.value = random.randint(5, 15)
            self.color = graphics.LIGHT_GRAY