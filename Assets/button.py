import pygame
from config import *

pygame.font.init()
font_small = pygame.font.SysFont("consolas", 28)

class Button:
    def __init__(self, text, x, y, w, h, filled=False):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.filled = filled
        self.hovered = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Default style
        bg_color = DARK_GREEN if self.filled else BLACK
        border_color = GREEN
        text_color = WHITE

        # Hover effect → both buttons fill green
        if self.hovered:
            bg_color = GREEN
            text_color = WHITE  # keep contrast strong

        # Draw background and border
        pygame.draw.rect(screen, bg_color, self.rect, 0, border_radius=3)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=3)

        # Render text
        label = font_small.render(self.text, True, text_color)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False