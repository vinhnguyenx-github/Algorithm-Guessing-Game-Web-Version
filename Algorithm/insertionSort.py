from Algorithm.sorting import SortingAlgorithm

class InsertionSort(SortingAlgorithm):
    def __init__(self, data):
        super().__init__(data)
        self.i = 1
        self.j = 0
        self.ins_inited = True
        self.n = len(self.data)

    def step(self):
        if self.done:
            return

        # Done condition
        if self.i >= self.n:
            self.states = [2] * self.n
            self.done = True
            return

        # Reset states for highlight
        self.states = [0] * self.n

        # If this pair is in order or j out of range, move to next i
        if self.j < 0 or self.data[self.j] <= self.data[self.j + 1]:
            self.i += 1
            if self.i >= self.n:
                self.states = [2] * self.n
                self.done = True
                return
            self.j = self.i - 1
            return

        # Otherwise, swap adjacent pair (like bubble animation)
        a, b = self.j, self.j + 1
        self.states[a] = self.states[b] = 1
        self.data[a], self.data[b] = self.data[b], self.data[a]
        self.j -= 1