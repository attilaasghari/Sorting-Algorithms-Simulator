# sorting/selection_sort.py
import time
from .base_sorter import BaseSorter

class SelectionSort(BaseSorter):
    """
    Selection Sort Algorithm
    
    Steps:
    1. Find the minimum element in the unsorted portion
    2. Swap it with the first unsorted element
    3. Move the boundary of sorted/unsorted one position right
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Selection Sort")

        for i in range(n):
            # Assume the first unsorted element is the minimum
            min_idx = i
            
            # Highlight the current position being filled
            self.record_step(
                arr,
                f"Finding minimum in unsorted subarray [{i}:{n}]",
                {'comparing': [i], 'sorted': list(range(i))}
            )

            # Search for the actual minimum in the unsorted part
            for j in range(i + 1, n):
                self.record_step(
                    arr,
                    f"Comparing {arr[j]} with current min {arr[min_idx]}",
                    {'comparing': [min_idx, j], 'sorted': list(range(i))}
                )
                if self.compare(arr[min_idx], arr[j]):
                    min_idx = j
                    self.record_step(
                        arr,
                        f"New minimum found: {arr[min_idx]}",
                        {'comparing': [min_idx], 'sorted': list(range(i))}
                    )

            # Swap the found minimum with the first unsorted element
            if min_idx != i:
                self.swap(arr, i, min_idx)
                self.record_step(
                    arr,
                    f"Swapped {arr[i]} and {arr[min_idx]}. Position {i} is now sorted.",
                    {'swapping': [i, min_idx], 'sorted': list(range(i + 1))}
                )
            else:
                self.record_step(
                    arr,
                    f"{arr[i]} is already in correct position.",
                    {'sorted': list(range(i + 1))}
                )

        self.end_time = time.time()
        self.record_step(arr, "Selection Sort completed!")
        return arr