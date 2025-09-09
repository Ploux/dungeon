#!/usr/bin/env python3

import random
from monsters import Enemy
from items import Treasure

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for _ in range(width)] for _ in range(height)]
        self.generate_dungeon()
        self.enemies = []
        self.treasures = []
        self.generate_entities()

    def generate_dungeon(self):
        # Create a simple grid with walls around the edges
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    self.map[y][x] = 1  # Wall
                else:
                    # Randomly generate some inner walls
                    if random.random() < 0.15:
                        self.map[y][x] = 1  # Wall

        # Ensure player start position is clear
        self.map[1][1] = 0
        self.map[1][2] = 0
        self.map[2][1] = 0

    def generate_entities(self):
        # Generate enemies
        for _ in range(15):
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                if self.map[y][x] == 0:
                    enemy_type = random.choice(["goblin", "orc", "dragon"])
                    self.enemies.append(Enemy(x, y, enemy_type))
                    break

        # Generate treasures
        for _ in range(10):
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                if self.map[y][x] == 0:
                    treasure_type = random.choice(["gold", "health", "sword"])
                    self.treasures.append(Treasure(x, y, treasure_type))
                    break