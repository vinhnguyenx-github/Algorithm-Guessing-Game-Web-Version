import pygame
from visualization import Visualization
from Assets.button import Button
from config import *

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Visualization
        self.visualization = Visualization(width, height)

        # Game state
        self.started = False
        self.paused = False

        # Buttons in bottom UI area
        button_w, button_h = 120, 40
        btn_y = self.height - BOTTOM_AREA + (BOTTOM_AREA - button_h) // 2

        self.start_btn = Button("START", 50, btn_y, button_w, button_h, filled=True)
        self.pause_btn = Button("PAUSE", 200, btn_y, button_w, button_h, filled=True)
        self.reset_btn = Button("RESET", 350, btn_y, button_w, button_h, filled=False)

    def handle_event(self, event):
        if self.start_btn.is_clicked(event):
            self.started = True
            self.paused = False
        elif self.pause_btn.is_clicked(event) and self.started:
            self.paused = not self.paused
        elif self.reset_btn.is_clicked(event):
            self.visualization.reset()
            self.started = False
            self.paused = False
        return None

    def draw(self, screen):
        screen.fill(BLACK)

        line_y = self.height - BOTTOM_AREA
        mid_x = self.width // 2

        # Visualization only if started
        if self.started:
            if not self.paused:
                self.visualization.step()
            self.visualization.draw(screen)

        # Always show middle and bottom lines
        pygame.draw.line(screen, LIGHT_GREEN, (0, line_y), (self.width, line_y), 2)   # Bottom line
        pygame.draw.line(screen, LIGHT_GREEN, (mid_x, 0), (mid_x, line_y), 2)        # Middle line

        # Control buttons (always visible)
        self.start_btn.draw(screen)
        self.pause_btn.draw(screen)
        self.reset_btn.draw(screen)