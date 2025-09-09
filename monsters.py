#!/usr/bin/env python3

import graphics

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.type = enemy_type
        if enemy_type == "goblin":
            self.health = 30
            self.attack = 8
            self.defense = 2
            self.exp_reward = 25
            self.color = graphics.LIGHT_RED
        elif enemy_type == "orc":
            self.health = 60
            self.attack = 15
            self.defense = 5
            self.exp_reward = 50
            self.color = graphics.DARK_RED
        elif enemy_type == "dragon":
            self.health = 120
            self.attack = 25
            self.defense = 10
            self.exp_reward = 100
            self.color = graphics.PURPLE

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage