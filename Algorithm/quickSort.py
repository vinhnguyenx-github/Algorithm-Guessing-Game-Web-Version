import pygame
from Algorithm.sorting import SortingAlgorithm

class QuickSort(SortingAlgorithm):
    def __init__(self, data):
        super().__init__(data)
        self.n = len(self.data)

        # internal state
        self.quick_tasks = None
        self.quick_in_progress = None

        # optional: if you want delays, set them here (ms). 
        # You can set to 0 for instant steps.
        self.delay_compare = 0
        self.delay_swap = 0
        self.next_step_time = 0

    def step(self):
        if self.done:
            return

        now = pygame.time.get_ticks()
        if now < self.next_step_time:
            return

        # initialize stack of tasks (ranges)
        if self.quick_tasks is None:
            self.quick_tasks = [(0, self.n - 1)]
            self.quick_in_progress = None

        # finished?
        if not self.quick_tasks and self.quick_in_progress is None:
            self.states = [2] * self.n
            self.done = True
            return

        # start a new partition if none active
        if self.quick_in_progress is None:
            low, high = self.quick_tasks.pop()
            if low >= high:
                if 0 <= low < self.n:
                    self.states[low] = 2
                return
            pivot = high
            i = low - 1
            j = low
            self.quick_in_progress = [low, high, pivot, i, j]

        low, high, pivot, i, j = self.quick_in_progress

        # highlight pivot and current element
        self.states = [0] * self.n
        if 0 <= pivot < self.n:
            self.states[pivot] = 1
        if low <= j < self.n:
            self.states[j] = 1

        # still scanning?
        if j <= high - 1:
            if self.data[j] <= self.data[pivot]:
                i += 1
                # swap into place
                self.data[i], self.data[j] = self.data[j], self.data[i]
                self.next_step_time = now + self.delay_swap
            else:
                self.next_step_time = now + self.delay_compare
            j += 1
            self.quick_in_progress = [low, high, pivot, i, j]
            return
        else:
            # put pivot in final position
            pivot_final = i + 1
            self.data[pivot_final], self.data[pivot] = self.data[pivot], self.data[pivot_final]

            # mark pivot_final as sorted
            if 0 <= pivot_final < self.n:
                self.states[pivot_final] = 2

            # push subranges onto stack
            if pivot_final + 1 < high:
                self.quick_tasks.append((pivot_final + 1, high))
            if low < pivot_final - 1:
                self.quick_tasks.append((low, pivot_final - 1))

            # done with partition
            self.quick_in_progress = None
            self.next_step_time = now + self.delay_swap

            # final check
            if not self.quick_tasks:
                self.states = [2] * self.n
                self.done = True