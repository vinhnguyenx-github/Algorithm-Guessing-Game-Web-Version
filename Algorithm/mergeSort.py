import pygame
from Algorithm.sorting import SortingAlgorithm

class MergeSort(SortingAlgorithm):
    def __init__(self, data):
        super().__init__(data)
        self.n = len(self.data)

        # internal state for bottom-up merge sort
        self.merge_tasks = []
        self.merge_buffer = None
        self.merge_inited = False

        # delays (set to 0 for instant steps)
        self.delay_swap = 0
        self.next_step_time = 0

    def step(self):
        if self.done:
            return

        now = pygame.time.get_ticks()
        if now < self.next_step_time:
            return

        # generate merge tasks (bottom-up)
        if not self.merge_inited:
            size = 1
            while size < self.n:
                for left in range(0, self.n, 2*size):
                    mid = min(left + size - 1, self.n - 1)
                    right = min(left + 2*size - 1, self.n - 1)
                    if mid < right:
                        self.merge_tasks.append((left, mid, right))
                size *= 2
            self.merge_inited = True

        # if no jobs -> finished
        if not self.merge_tasks:
            self.states = [2] * self.n
            self.done = True
            return

        # init buffer for current merge job
        if self.merge_buffer is None:
            l, m, r = self.merge_tasks[0]
            self.merge_buffer = (l, m, r, l, m+1, [])

        # unpack state
        l, m, r, i, j, merged = self.merge_buffer

        # reset states
        self.states = [0] * self.n

        # comparison
        if i <= m and (j > r or self.data[i] <= self.data[j]):
            merged.append(self.data[i])
            self.states[i] = 1
            i += 1
        elif j <= r:
            merged.append(self.data[j])
            self.states[j] = 1
            j += 1

        # if block finished, write merged array back
        if i > m and j > r:
            for k, val in enumerate(merged):
                self.data[l + k] = val
            self.merge_tasks.pop(0)
            self.merge_buffer = None
        else:
            self.merge_buffer = (l, m, r, i, j, merged)

        self.next_step_time = now + self.delay_swap