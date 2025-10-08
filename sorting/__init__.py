# sorting/__init__.py
from .base_sorter import BaseSorter

class PlaceholderSorter(BaseSorter):
    def sort(self):
        arr = self.original_array.copy()
        self.record_step(arr, "This algorithm is not implemented yet.")
        return arr

# Import all implemented sorters
from .bubble_sort import BubbleSort
from .insertion_sort import InsertionSort
from .selection_sort import SelectionSort
from .merge_sort import MergeSort
from .quick_sort import QuickSort
from .heap_sort import HeapSort
from .counting_sort import CountingSort
from .radix_sort import RadixSort
from .bucket_sort import BucketSort
from .cocktail_sort import CocktailSort
from .comb_sort import CombSort
from .pigeonhole_sort import PigeonholeSort
from .bogo_sort import BogoSort
from .shell_sort import ShellSort
from .introsort import IntroSort

# Map algorithm names to classes
SORTER_MAP = {
    "Bubble Sort": BubbleSort,
    "Insertion Sort": InsertionSort,
    "Selection Sort": SelectionSort,
    "Merge Sort": MergeSort,
    "Quick Sort": QuickSort,
    "Heap Sort": HeapSort,
    "Shell Sort": ShellSort, 
    "Counting Sort": CountingSort,
    "Radix Sort": RadixSort,
    "Bucket Sort": BucketSort,
    "Cocktail Sort": CocktailSort,
    "Comb Sort": CombSort,
    "Pigeonhole Sort": PigeonholeSort,
    "IntroSort": IntroSort,  
    "Bogo Sort": BogoSort,
    
    # Add more as you implement them
}

# Fill unimplemented algorithms with placeholder
ALL_ALGORITHMS = [
    "Bubble Sort", "Insertion Sort", "Selection Sort",
    "Merge Sort", "Quick Sort", "Heap Sort", "Shell Sort",
    "Counting Sort", "Radix Sort", "Bucket Sort", "Pigeonhole Sort",
    "Cocktail Sort", "Comb Sort", "IntroSort", "Bogo Sort"
]

for algo in ALL_ALGORITHMS:
    if algo not in SORTER_MAP:
        SORTER_MAP[algo] = PlaceholderSorter

def get_sorter(name, array):
    """Factory function to get a sorter instance by name."""
    cls = SORTER_MAP.get(name)
    if not cls:
        raise ValueError(f"Unknown algorithm: {name}")
    return cls(array)