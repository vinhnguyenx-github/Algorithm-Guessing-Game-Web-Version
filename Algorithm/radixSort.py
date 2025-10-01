import pygame
from Algorithm.sorting import SortingAlgorithm
import math

class RadixSort(SortingAlgorithm):
    def __init__(self, data):
        super().__init__(data)
        self.n = len(self.data)

        # figure out max digits
        self.max_digits = 0 if self.n == 0 else int(math.log10(max(self.data))) + 1

        # internal state
        self.current_digit = 0        # which digit we are processing
        self.bucket_phase = True      # True = distributing into buckets, False = rebuilding
        self.index = 0                # current index in array/bucket
        self.buckets = [[] for _ in range(10)]

        # delay control
        self.delay_swap = 0
        self.next_step_time = 0

    def step(self):
        if self.done:
            return

        now = pygame.time.get_ticks()
        if now < self.next_step_time:
            return

        # if finished
        if self.current_digit >= self.max_digits:
            self.states = [2] * self.n
            self.done = True
            return

        self.states = [0] * self.n

        # bucket distribution phase
        if self.bucket_phase:
            if self.index < self.n:
                val = self.data[self.index]
                digit = (val // (10 ** self.current_digit)) % 10
                self.buckets[digit].append(val)
                # highlight the current element
                self.states[self.index] = 1
                self.index += 1
            else:
                # switch to rebuild phase
                self.bucket_phase = False
                self.index = 0
            self.next_step_time = now + self.delay_swap
            return

        # rebuild phase
        else:
            flat = []
            for b in self.buckets:
                flat.extend(b)

            if self.index < len(flat):
                self.data[self.index] = flat[self.index]
                self.states[self.index] = 1
                self.index += 1
            else:
                # reset for next digit
                self.current_digit += 1
                self.bucket_phase = True
                self.index = 0
                self.buckets = [[] for _ in range(10)]

            self.next_step_time = now + self.delay_swap
            return