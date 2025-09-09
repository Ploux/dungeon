#!/usr/bin/env python3

import pygame
import graphics

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
        return (graphics.MESSAGE_WINDOW_HEIGHT - 10) // self.font.get_height()

    def draw(self, screen):
        # Draw message window background
        window_rect = pygame.Rect(0, graphics.GAME_AREA_HEIGHT, graphics.SCREEN_WIDTH, graphics.MESSAGE_WINDOW_HEIGHT)
        pygame.draw.rect(screen, graphics.BLACK, window_rect)
        pygame.draw.rect(screen, graphics.WHITE, window_rect, 2)

        if not self.messages:
            return

        visible_lines = self.get_visible_lines()
        start_index = max(0, len(self.messages) - visible_lines - self.scroll_offset)
        end_index = len(self.messages) - self.scroll_offset

        y_offset = graphics.GAME_AREA_HEIGHT + 5
        for i in range(start_index, end_index):
            if i >= 0 and i < len(self.messages):
                text_surface = self.font.render(self.messages[i], True, graphics.LIGHT_GRAY)
                screen.blit(text_surface, (5, y_offset))
                y_offset += self.font.get_height()