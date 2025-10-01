from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    """Abstract base class for all sorting algorithms."""

    def __init__(self, data):
        self.data = list(data)  # copy input
        self.states = [0] * len(self.data)  # for visualization if needed
        self.done = False

    @abstractmethod
    def step(self):
        """Perform one step of the algorithm."""
        pass

    def is_done(self):
        return self.done

    def get_data(self):
        return self.data