# sorting/bubble_sort.py
import time
from .base_sorter import BaseSorter

class BubbleSort(BaseSorter):
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Bubble Sort")

        for i in range(n):
            swapped = False
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # Highlight the pair being compared
                self.record_step(
                    arr,
                    f"Comparing {arr[j]} and {arr[j+1]}",
                    {'comparing': [j, j+1]}
                )
                if self.compare(arr[j], arr[j+1]):
                    self.swap(arr, j, j+1)
                    swapped = True
                    self.record_step(
                        arr,
                        f"Swapped {arr[j]} and {arr[j+1]}",
                        {'swapping': [j, j+1]}
                    )
            # Mark the last i+1 elements as sorted
            sorted_indices = list(range(n - i, n))
            self.record_step(
                arr,
                f"Pass {i+1} complete. Largest {i+1} elements are sorted.",
                {'sorted': sorted_indices}
            )
            if not swapped:
                break

        self.end_time = time.time()
        self.record_step(arr, "Bubble Sort completed!")
        return arr