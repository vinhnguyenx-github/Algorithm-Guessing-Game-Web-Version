import pygame
import numpy as np
import random

from Algorithm.bubbleSort import BubbleSort
from Algorithm.insertionSort import InsertionSort
from Algorithm.quickSort import QuickSort
from Algorithm.mergeSort import MergeSort
from Algorithm.radixSort import RadixSort
from Algorithm.selectionSort import SelectionSort
from Algorithm.bogoSort import BogoSort

from config import *

class Visualization:
    def __init__(self, width, height, num_points=50):
        self.width = width
        self.height = height
        self.num_points = num_points

        # Layout
        self.PADDING_TOP = 70
        self.PADDING_LEFT = 10
        self.PADDING_RIGHT = 10
        self.PADDING_MIDDLE = 10
        self.BOTTOM_AREA = 60
        self.BAR_BOTTOM_PADDING = 10
        self.BAR_SPACING = 1

        # Colors
        self.COLOR_DEFAULT = (0, 200, 70)   # unsorted
        self.COLOR_ACTIVE  = (255, 80, 0)   # comparing/swapping
        self.COLOR_SORTED  = (0, 255, 180)  # sorted (teal glow)
        self.COLOR_LINE    = (0, 255, 0)    # neon green

        # Fonts
        self.font = pygame.font.SysFont("consolas", 24, bold=True)

        # Algorithms dictionary
        self.algorithms = {
            1: BubbleSort,
            2: InsertionSort,
            3: QuickSort,
            4: MergeSort,
            5: RadixSort,
            6: SelectionSort,
            7: BogoSort
        }

        # Track algorithm names
        self.left_algo_name = ""
        self.right_algo_name = ""

        # finishing wave progress
        self.finish_left = 0
        self.finish_right = 0
        self.FINISH_RATE = 1  # how many bars turn per frame

        self.reset()

    def reset(self, num_points=None):
        if num_points is not None:
            self.num_points = num_points

        max_value = self.height - self.PADDING_TOP - self.BOTTOM_AREA
        data = np.random.randint(1, max_value, size=self.num_points).tolist()

        # Pick 2 algorithms randomly (no duplicates)
        left_id, right_id = random.sample(list(self.algorithms.keys()), 2)
        self.sorter_left = self.algorithms[left_id](list(data))
        self.sorter_right = self.algorithms[right_id](list(data))

        self.left_algo_name = self.algorithms[left_id].__name__
        self.right_algo_name = self.algorithms[right_id].__name__

        self.finish_left = 0
        self.finish_right = 0

    def step(self):
        # Left sorter
        if not self.sorter_left.is_done():
            self.sorter_left.step()
        else:
            self.finish_left = min(self.finish_left + self.FINISH_RATE, len(self.sorter_left.data))

        # Right sorter
        if not self.sorter_right.is_done():
            self.sorter_right.step()
        else:
            self.finish_right = min(self.finish_right + self.FINISH_RATE, len(self.sorter_right.data))

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
            rect_width = max(1, bar_width - self.BAR_SPACING)

            # Pick color
            if sorter.is_done():
                # progressively turn bars to sorted color
                if i < finish_progress:
                    color = self.COLOR_SORTED
                else:
                    color = self.COLOR_DEFAULT
            else:
                state = sorter.states[i]
                if state == 0:
                    color = self.COLOR_DEFAULT
                elif state == 1:
                    color = self.COLOR_ACTIVE
                else:
                    color = self.COLOR_SORTED

            pygame.draw.rect(screen, color, (x, y, rect_width, bar_height))

    def draw(self, screen):
        mid_x = self.width // 2
        line_y = self.height - self.BOTTOM_AREA

        # Left visualization
        self.draw_array(screen, self.sorter_left, self.finish_left,
                        self.PADDING_LEFT, mid_x - self.PADDING_MIDDLE, self.height)

        # Right visualization
        self.draw_array(screen, self.sorter_right, self.finish_right,
                        mid_x + self.PADDING_MIDDLE, self.width - self.PADDING_RIGHT, self.height)

        # Algo names above
        left_text = self.font.render(self.left_algo_name, True, self.COLOR_LINE)
        right_text = self.font.render(self.right_algo_name, True, self.COLOR_LINE)
        screen.blit(left_text, left_text.get_rect(center=(mid_x // 2, 25)))
        screen.blit(right_text, right_text.get_rect(center=(mid_x + (self.width - mid_x) // 2, 25)))

        # Lines
        pygame.draw.line(screen, self.COLOR_LINE, (mid_x, 0), (mid_x, line_y), 3)
        pygame.draw.line(screen, self.COLOR_LINE, (0, line_y), (self.width, line_y), 3)