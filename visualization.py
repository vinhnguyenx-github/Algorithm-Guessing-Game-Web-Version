# visualization.py
import pygame
import numpy as np
import random
from Algorithm.bubbleSort import BubbleSort
from Algorithm.insertionSort import InsertionSort
from config import *

class Visualization:
    def __init__(self, width, height, num_points=50):
        self.width = width
        self.height = height
        self.num_points = num_points

        # Layout
        self.PADDING_TOP = 50
        self.PADDING_LEFT = 10
        self.PADDING_RIGHT = 10
        self.PADDING_MIDDLE = 10
        self.BOTTOM_AREA = 60
        self.BAR_BOTTOM_PADDING = 10
        self.BAR_SPACING = 1

        # Colors
        self.COLOR_DEFAULT = (0, 200, 70)    # dim green (unsorted)
        self.COLOR_ACTIVE  = (255, 80, 0)    # orange/red (highlight swapping)
        self.COLOR_SORTED  = (0, 255, 180)   # cyan/teal (sorted, glowing)
        self.COLOR_LINE    = (0, 255, 0)     # bright neon green (lines)

        self.algorithms = {1: BubbleSort, 2: InsertionSort}

        # progressive finalize counters (right->left)
        self.finish_left = 0
        self.finish_right = 0
        self.FINISH_RATE = 1  # bars per frame

        self.reset()

    def reset(self, num_points=None):
        if num_points is not None:
            self.num_points = num_points

        max_value = self.height - self.PADDING_TOP - self.BOTTOM_AREA
        data = np.random.randint(1, max_value, size=self.num_points).tolist()

        left_id, right_id = random.sample(algorithm_ID, 2)
        self.sorter_left = self.algorithms[left_id](list(data))
        self.sorter_right = self.algorithms[right_id](list(data))

        self.finish_left = 0
        self.finish_right = 0

    def step(self):
        if not self.sorter_left.is_done():
            self.sorter_left.step()
        else:
            self.finish_left = min(len(self.sorter_left.get_data()),
                                   self.finish_left + self.FINISH_RATE)

        if not self.sorter_right.is_done():
            self.sorter_right.step()
        else:
            self.finish_right = min(len(self.sorter_right.get_data()),
                                    self.finish_right + self.FINISH_RATE)

    def draw_array(self, screen, sorter, finish_progress, x_start, x_end, height):
        data = sorter.get_data()
        n = len(data)
        if n == 0:
            return

        available_width = (x_end - x_start)
        bar_width = available_width / n
        max_val = max(data)

        line_y = height - self.BOTTOM_AREA
        play_height = (line_y - self.BAR_BOTTOM_PADDING) - self.PADDING_TOP

        for i, val in enumerate(data):
            bar_height = (val / max_val) * play_height
            x = x_start + i * bar_width
            y = (line_y - self.BAR_BOTTOM_PADDING) - bar_height
            rect_w = max(1, bar_width - self.BAR_SPACING)

            # color logic
            if sorter.is_done():
                # progressively color from rightmost to leftmost
                color = (self.COLOR_SORTED if i >= n - finish_progress
                         else self.COLOR_DEFAULT)
            else:
                state = sorter.states[i] if i < len(sorter.states) else 0
                color = self.COLOR_ACTIVE if state == 1 else (
                        self.COLOR_SORTED if state == 2 else self.COLOR_DEFAULT)

            pygame.draw.rect(screen, color, (x, y, rect_w, bar_height))

    def draw(self, screen):
        mid_x = self.width // 2
        line_y = self.height - self.BOTTOM_AREA

        # Left
        self.draw_array(screen, self.sorter_left, self.finish_left,
                        self.PADDING_LEFT, mid_x - self.PADDING_MIDDLE, self.height)
        # Right
        self.draw_array(screen, self.sorter_right, self.finish_right,
                        mid_x + self.PADDING_MIDDLE, self.width - self.PADDING_RIGHT, self.height)

        # Lines
        pygame.draw.line(screen, self.COLOR_LINE, (mid_x, 0), (mid_x, line_y), 3)
        pygame.draw.line(screen, self.COLOR_LINE, (0, line_y), (self.width, line_y), 3)