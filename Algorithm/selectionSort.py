from Algorithm.sorting import SortingAlgorithm

class SelectionSort(SortingAlgorithm):
    def __init__(self, data):
        super().__init__(data)
        self.n = len(self.data)
        self.i = 0              # current index to place smallest element
        self.j = 1              # scanning index
        self.min_index = 0      # index of current minimum

    def step(self):
        if self.done:
            return

        self.states = [0] * self.n  # reset visualization states

        # finished?
        if self.i >= self.n - 1:
            self.states = [2] * self.n
            self.done = True
            return

        # highlight current scanning positions
        self.states[self.i] = 2             # everything before i is sorted
        self.states[self.min_index] = 1     # highlight current min
        if self.j < self.n:
            self.states[self.j] = 1         # highlight comparing element

        # update minimum if needed
        if self.j < self.n and self.data[self.j] < self.data[self.min_index]:
            self.min_index = self.j

        # advance scan
        self.j += 1

        # end of scan -> perform swap
        if self.j >= self.n:
            if self.min_index != self.i:
                self.data[self.i], self.data[self.min_index] = self.data[self.min_index], self.data[self.i]

            self.i += 1
            self.min_index = self.i
            self.j = self.i + 1