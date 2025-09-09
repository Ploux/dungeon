#!/usr/bin/env python3

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
MAP_WIDTH = 25
MAP_HEIGHT = 18
MESSAGE_WINDOW_HEIGHT = 120  # Height of the message window
GAME_AREA_HEIGHT = SCREEN_HEIGHT - MESSAGE_WINDOW_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)
DARKER_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 200, 255)
PURPLE = (100, 0, 100)
LIGHT_RED = (200, 50, 50)
DARK_RED = (150, 0, 0)
DARK_GREEN = (0, 200, 0)
DARKER_RED = (50, 0, 0)
DARK_BLUE = (0, 0, 50)
LIGHT_YELLOW = (255, 255, 200)
MEDIUM_GRAY = (80, 80, 80)
VERY_DARK_GRAY = (40, 40, 40)
DARKER_YELLOW = (150, 150, 0)

PLAYER_COLOR = GREEN
ENEMY_COLOR = RED
TREASURE_COLOR = YELLOW
WALL_COLOR = DARK_GRAY
FLOOR_COLOR = DARKER_GRAY
TEXT_COLOR = WHITE
BACKGROUND_COLOR = BLACK

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon")
clock = pygame.time.Clock()

class MessageWindow:
    def __init__(self):
        self.messages = []
        self.font = pygame.font.SysFont(None, 20)
        self.max_messages = 50  # Keep last 50 messages
        self.scroll_offset = 0

    def add_message(self, text):
        self.messages.append(text)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        # Auto-scroll to bottom when new message arrives
        self.scroll_to_bottom()

    def scroll_up(self):
        max_scroll = max(0, len(self.messages) - self.get_visible_lines())
        self.scroll_offset = min(self.scroll_offset + 1, max_scroll)

    def scroll_down(self):
        self.scroll_offset = max(0, self.scroll_offset - 1)

    def scroll_to_bottom(self):
        self.scroll_offset = 0

    def get_visible_lines(self):
        return (MESSAGE_WINDOW_HEIGHT - 10) // self.font.get_height()

    def draw(self, screen):
        # Draw message window background
        window_rect = pygame.Rect(0, GAME_AREA_HEIGHT, SCREEN_WIDTH, MESSAGE_WINDOW_HEIGHT)
        pygame.draw.rect(screen, BLACK, window_rect)
        pygame.draw.rect(screen, WHITE, window_rect, 2)

        if not self.messages:
            return

        visible_lines = self.get_visible_lines()
        start_index = max(0, len(self.messages) - visible_lines - self.scroll_offset)
        end_index = len(self.messages) - self.scroll_offset

        y_offset = GAME_AREA_HEIGHT + 5
        for i in range(start_index, end_index):
            if i >= 0 and i < len(self.messages):
                text_surface = self.font.render(self.messages[i], True, LIGHT_GRAY)
                screen.blit(text_surface, (5, y_offset))
                y_offset += self.font.get_height()

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
        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
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
            self.color = LIGHT_RED
        elif enemy_type == "orc":
            self.health = 60
            self.attack = 15
            self.defense = 5
            self.exp_reward = 50
            self.color = DARK_RED
        elif enemy_type == "dragon":
            self.health = 120
            self.attack = 25
            self.defense = 10
            self.exp_reward = 100
            self.color = PURPLE

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage

class Treasure:
    def __init__(self, x, y, treasure_type):
        self.x = x
        self.y = y
        self.type = treasure_type
        if treasure_type == "gold":
            self.value = random.randint(10, 50)
            self.color = YELLOW
        elif treasure_type == "health":
            self.value = random.randint(20, 50)
            self.color = RED
        elif treasure_type == "sword":
            self.value = random.randint(5, 15)
            self.color = LIGHT_GRAY

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

def draw_tile(screen, x, y, tile_type):
    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    if tile_type == 1:  # Wall
        pygame.draw.rect(screen, WALL_COLOR, rect)
        pygame.draw.rect(screen, MEDIUM_GRAY, rect, 1)
    else:  # Floor
        pygame.draw.rect(screen, FLOOR_COLOR, rect)
        pygame.draw.rect(screen, VERY_DARK_GRAY, rect, 1)

def draw_player(screen, player):
    rect = pygame.Rect(player.x * TILE_SIZE, player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, rect)
    pygame.draw.rect(screen, DARK_GREEN, rect, 2)

    # Draw a simple face
    pygame.draw.circle(screen, BLACK, (rect.centerx - 5, rect.centery - 5), 3)
    pygame.draw.circle(screen, BLACK, (rect.centerx + 5, rect.centery - 5), 3)
    pygame.draw.arc(screen, BLACK, (rect.centerx - 8, rect.centery, 16, 10), 0, 3.14, 2)

def draw_enemy(screen, enemy):
    rect = pygame.Rect(enemy.x * TILE_SIZE, enemy.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, enemy.color, rect)
    pygame.draw.rect(screen, DARKER_RED, rect, 2)

    # Draw a simple face
    pygame.draw.circle(screen, WHITE, (rect.centerx - 5, rect.centery - 5), 3)
    pygame.draw.circle(screen, WHITE, (rect.centerx + 5, rect.centery - 5), 3)
    pygame.draw.arc(screen, WHITE, (rect.centerx - 8, rect.centery, 16, 10), 0, 3.14, 2)

def draw_treasure(screen, treasure):
    rect = pygame.Rect(treasure.x * TILE_SIZE, treasure.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, treasure.color, rect)
    pygame.draw.rect(screen, DARKER_YELLOW, rect, 2)

    # Draw a simple treasure symbol
    pygame.draw.circle(screen, LIGHT_YELLOW, rect.center, 8)

def draw_ui(screen, player, dungeon):
    # Draw health bar
    pygame.draw.rect(screen, DARKER_RED, (10, 10, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, 200 * (player.health / player.max_health), 20))
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2)

    # Draw gold
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Gold: {player.gold}", True, TEXT_COLOR)
    screen.blit(text, (10, 40))

    # Draw level
    text = font.render(f"Level: {player.level}", True, TEXT_COLOR)
    screen.blit(text, (10, 70))

    # Draw exp
    pygame.draw.rect(screen, DARK_BLUE, (10, 100, 200, 10))
    pygame.draw.rect(screen, BLUE, (10, 100, 200 * (player.exp / player.exp_to_level), 10))
    pygame.draw.rect(screen, WHITE, (10, 100, 200, 10), 1)

def main():
    # Create player
    player = Player(1, 1)

    # Create dungeon
    dungeon = Dungeon(MAP_WIDTH, MAP_HEIGHT)

    # Create message window
    message_window = MessageWindow()
    message_window.add_message("Welcome to the dungeon! Use arrow keys to move. Press 'r' to restart.")

    # Game loop
    running = True
    game_over = False

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    # Handle movement and combat
                    dx, dy = 0, 0
                    if event.key == pygame.K_KP7:  # Northwest
                        dx, dy = -1, -1
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_UP:  # North
                        dx, dy = 0, -1
                    elif event.key == pygame.K_KP9:  # Northeast
                        dx, dy = 1, -1
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:  # East
                        dx, dy = 1, 0
                    elif event.key == pygame.K_KP3:  # Southeast
                        dx, dy = 1, 1
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_DOWN:  # South
                        dx, dy = 0, 1
                    elif event.key == pygame.K_KP1:  # Southwest
                        dx, dy = -1, 1
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:  # West
                        dx, dy = -1, 0
                    
                    # Check if movement would trigger combat
                    if dx != 0 or dy != 0:
                        new_x = player.x + dx
                        new_y = player.y + dy
                        
                        # Check if there's an enemy at the target position
                        enemy_at_target = None
                        for enemy in dungeon.enemies:
                            if enemy.x == new_x and enemy.y == new_y:
                                enemy_at_target = enemy
                                break
                        
                        if enemy_at_target:
                            # Combat: Player attacks enemy
                            damage = player.attack
                            actual_damage = enemy_at_target.take_damage(damage)
                            message_window.add_message(f"You hit the {enemy_at_target.type} for {actual_damage}.")
                            
                            if enemy_at_target.health <= 0:
                                # Enemy defeated - player moves into square
                                message_window.add_message(f"You have slain the {enemy_at_target.type}!")
                                player.gain_exp(enemy_at_target.exp_reward)
                                dungeon.enemies.remove(enemy_at_target)
                                player.move(dx, dy, dungeon.map)
                            else:
                                # Enemy attacks back
                                damage = enemy_at_target.attack
                                actual_damage = player.take_damage(damage)
                                message_window.add_message(f"The {enemy_at_target.type} hits you for {actual_damage}.")
                                if player.health <= 0:
                                    game_over = True
                        else:
                            # Normal movement (no enemy at target)
                            player.move(dx, dy, dungeon.map)

                # Message window scrolling
                if event.key == pygame.K_PAGEUP:
                    message_window.scroll_up()
                elif event.key == pygame.K_PAGEDOWN:
                    message_window.scroll_down()
                elif event.key == pygame.K_END:
                    message_window.scroll_to_bottom()

                if event.key == pygame.K_r:
                    # Restart game
                    player = Player(1, 1)
                    dungeon = Dungeon(MAP_WIDTH, MAP_HEIGHT)
                    message_window = MessageWindow()
                    message_window.add_message("Welcome back to the dungeon! Use arrow keys to move. Press 'r' to restart.")
                    game_over = False

        if not game_over:
            # Check for collisions with treasures
            for treasure in dungeon.treasures[:]:
                if treasure.x == player.x and treasure.y == player.y:
                    if treasure.type == "gold":
                        player.gold += treasure.value
                        message_window.add_message(f"You've found {treasure.value} gold!")
                    elif treasure.type == "health":
                        healed = player.heal(treasure.value)
                        message_window.add_message(f"You've found a health potion and healed {healed} health!")
                    elif treasure.type == "sword":
                        player.attack += treasure.value
                        message_window.add_message(f"You've found a magic sword! Attack increased by {treasure.value}!")
                    dungeon.treasures.remove(treasure)

        # Draw everything
        screen.fill(BACKGROUND_COLOR)

        # Create a surface for the game area (clipped to avoid drawing over message window)
        game_surface = pygame.Surface((SCREEN_WIDTH, GAME_AREA_HEIGHT))
        game_surface.fill(BACKGROUND_COLOR)

        # Draw dungeon
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                if y * TILE_SIZE < GAME_AREA_HEIGHT:  # Only draw if within game area
                    draw_tile(game_surface, x, y, dungeon.map[y][x])

        # Draw treasures
        for treasure in dungeon.treasures:
            if treasure.y * TILE_SIZE < GAME_AREA_HEIGHT:
                draw_treasure(game_surface, treasure)

        # Draw enemies
        for enemy in dungeon.enemies:
            if enemy.y * TILE_SIZE < GAME_AREA_HEIGHT:
                draw_enemy(game_surface, enemy)

        # Draw player
        if player.y * TILE_SIZE < GAME_AREA_HEIGHT:
            draw_player(game_surface, player)

        # Draw UI
        draw_ui(game_surface, player, dungeon)

        # Blit the game surface to the main screen
        screen.blit(game_surface, (0, 0))

        # Draw message window
        message_window.draw(screen)

        # Draw game over message
        if game_over:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, GAME_AREA_HEIGHT//2))
            screen.blit(text, text_rect)

            font = pygame.font.SysFont(None, 36)
            text = font.render("Press R to restart", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, GAME_AREA_HEIGHT//2 + 60))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
