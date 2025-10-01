import pygame
from visualization import Visualization
from config import *

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Visualization uses the full height, but it will respect BOTTOM_AREA internally
        self.visualization = Visualization(width, height)

    def handle_event(self, event):
        # Future: add controls for pausing, skipping, etc.
        pass

    def draw(self, screen):
        screen.fill(BLACK)

        # Step and draw sorting visualization
        self.visualization.step()
        self.visualization.draw(screen)

        # Define bottom line position (reserved UI area below it)
        line_y = self.height - BOTTOM_AREA

        # Bottom line
        pygame.draw.line(
            screen, LIGHT_GREEN,
            (0, line_y),
            (self.width, line_y), 2
        )

        # Middle line (stop at bottom line instead of full height)
        mid_x = self.width // 2
        pygame.draw.line(
            screen, LIGHT_GREEN,
            (mid_x, 0),
            (mid_x, line_y), 2
        )