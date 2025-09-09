#!/usr/bin/env python3

import pygame

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

def draw_game_over(screen):
    font = pygame.font.SysFont(None, 72)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, GAME_AREA_HEIGHT//2))
    screen.blit(text, text_rect)

    font = pygame.font.SysFont(None, 36)
    text = font.render("Press R to restart", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, GAME_AREA_HEIGHT//2 + 60))
    screen.blit(text, text_rect)