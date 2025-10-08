# sorting/base_sorter.py
import time
from abc import ABC, abstractmethod

class BaseSorter(ABC):
    """
    Abstract base class for all sorting algorithms.
    Ensures consistent step logging, metrics, and visualization support.
    """
    def __init__(self, array):
        self.original_array = array.copy()
        self.steps = []  # List of {'array', 'explanation', 'highlights'}
        self.comparisons = 0
        self.swaps = 0
        self.start_time = None
        self.end_time = None

    def record_step(self, array, explanation="", highlights=None):
        """Record a step for visualization and playback."""
        self.steps.append({
            'array': array.copy(),
            'explanation': explanation,
            'highlights': highlights or {}
        })

    def compare(self, a, b):
        """Record a comparison and return a > b (for ascending sort)."""
        self.comparisons += 1
        return a > b

    def swap(self, arr, i, j):
        """Swap two elements and record the swap."""
        if i != j:
            arr[i], arr[j] = arr[j], arr[i]
            self.swaps += 1

    def get_metrics(self):
        """Return current performance metrics."""
        elapsed = (self.end_time or time.time()) - (self.start_time or time.time())
        return {
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'time': elapsed
        }

    def get_state_at(self, index):
        """Get the state (array + info) at a given step index."""
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return {'array': self.original_array.copy(), 'explanation': 'Initial state'}

    @abstractmethod
    def sort(self):
        """Perform the sort and populate self.steps."""
        pass