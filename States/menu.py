import pygame
from Assets.button import Button
from config import *



pygame.font.init()
font_large = pygame.font.SysFont("couriernew", 60, bold=True)

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Start = green filled, Config = border only
        self.start_btn = Button("START", width // 2 - 100, height // 2, 200, 60, filled=True)
        self.config_btn = Button("CONFIG", width // 2 - 100, height // 2 + 100, 200, 60, filled=False)

    def handle_event(self, event):
        if self.start_btn.is_clicked(event):
            return "game"
        elif self.config_btn.is_clicked(event):
            return "option"   # ✅ go to option state now
        return None

    def draw(self, screen):
        screen.fill(BLACK)
        header = font_large.render("ALGORITHM GUESSING GAME", True, LIGHT_GREEN)
        header_rect = header.get_rect(center=(self.width // 2, self.height // 4))
        screen.blit(header, header_rect)

        self.start_btn.draw(screen)
        self.config_btn.draw(screen)