import random
from Algorithm.sorting import SortingAlgorithm

class BogoSort(SortingAlgorithm):
    def __init__(self, data):
        super().__init__(data)
        self.n = len(self.data)

    def is_sorted(self):
        for i in range(len(self.data) - 1):
            if self.data[i] > self.data[i + 1]:
                return False
        return True

    def step(self):
        if self.done:
            return

        # Reset all states
        self.states = [0] * self.n

        if self.is_sorted():
            self.done = True
            self.states = [2] * self.n  # mark all as sorted
            return

        # Shuffle randomly
        random.shuffle(self.data)

        # Highlight everything as "active"
        self.states = [1] * self.n