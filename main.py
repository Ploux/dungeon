#!/usr/bin/env python3

import pygame
import sys
import graphics
from player import Player
from world import Dungeon
from message_window import MessageWindow

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((graphics.SCREEN_WIDTH, graphics.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon")
clock = pygame.time.Clock()

def main():
    # Create player
    player = Player(1, 1)

    # Create dungeon
    dungeon = Dungeon(graphics.MAP_WIDTH, graphics.MAP_HEIGHT)

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
        screen.fill(graphics.BACKGROUND_COLOR)

        # Create a surface for the game area (clipped to avoid drawing over message window)
        game_surface = pygame.Surface((graphics.SCREEN_WIDTH, graphics.GAME_AREA_HEIGHT))
        game_surface.fill(graphics.BACKGROUND_COLOR)

        # Draw dungeon
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                if y * graphics.TILE_SIZE < graphics.GAME_AREA_HEIGHT:  # Only draw if within game area
                    graphics.draw_tile(game_surface, x, y, dungeon.map[y][x])

        # Draw treasures
        for treasure in dungeon.treasures:
            if treasure.y * graphics.TILE_SIZE < graphics.GAME_AREA_HEIGHT:
                graphics.draw_treasure(game_surface, treasure)

        # Draw enemies
        for enemy in dungeon.enemies:
            if enemy.y * graphics.TILE_SIZE < graphics.GAME_AREA_HEIGHT:
                graphics.draw_enemy(game_surface, enemy)

        # Draw player
        if player.y * graphics.TILE_SIZE < graphics.GAME_AREA_HEIGHT:
            graphics.draw_player(game_surface, player)

        # Draw UI
        graphics.draw_ui(game_surface, player, dungeon)

        # Blit the game surface to the main screen
        screen.blit(game_surface, (0, 0))

        # Draw message window
        message_window.draw(screen)

        # Draw game over message
        if game_over:
            graphics.draw_game_over(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()