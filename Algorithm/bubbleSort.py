from Algorithm.sorting import SortingAlgorithm

class BubbleSort(SortingAlgorithm):
    def __init__(self, data):
        super().__init__(data)
        self.i = 0
        self.j = 0
        self.n = len(self.data)
        self.is_swapped = False

    def step(self):
        if self.done:
            return

        # Reset states (0 = default unsorted)
        self.states = [0] * self.n

        # If finished
        if self.i >= self.n - 1:
            self.done = True
            self.states = [2] * self.n  # mark all sorted
            return

        if self.j == 0:
            self.is_swapped = False

        # Highlight the two being compared
        self.states[self.j] = 1
        self.states[self.j + 1] = 1

        # Compare neighbors
        if self.data[self.j] > self.data[self.j + 1]:
            self.data[self.j], self.data[self.j + 1] = self.data[self.j + 1], self.data[self.j]
            self.is_swapped = True

        # Move forward
        self.j += 1

        # End of pass
        if self.j >= self.n - self.i - 1:
            if not self.is_swapped:
                self.done = True
                self.states = [2] * self.n
                return
            self.j = 0
            self.i += 1