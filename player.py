#!/usr/bin/env python3

import graphics

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.defense = 5
        self.gold = 0
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100

    def move(self, dx, dy, dungeon):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the move is valid
        if 0 <= new_x < graphics.MAP_WIDTH and 0 <= new_y < graphics.MAP_HEIGHT:
            if dungeon[new_y][new_x] != 1:  # 1 represents walls
                self.x = new_x
                self.y = new_y
                return True
        return False

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount):
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_level += 50
        self.max_health += 20
        self.health = self.max_health
        self.attack += 3
        self.defense += 2