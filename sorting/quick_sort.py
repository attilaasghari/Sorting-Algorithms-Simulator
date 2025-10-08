# sorting/quick_sort.py
import time
from .base_sorter import BaseSorter

class QuickSort(BaseSorter):
    """
    Quick Sort Algorithm (Iterative Implementation with Stack)
    
    Steps:
    1. Choose a 'pivot' element from the array
    2. Partition the array so elements < pivot are on left, > on right
    3. Recursively sort the sub-arrays (simulated with a stack)
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Quick Sort (Iterative)")

        # Stack stores (low, high) indices of subarrays to sort
        stack = [(0, n - 1)]
        sorted_ranges = []  # Track fully sorted ranges for highlighting

        while stack:
            low, high = stack.pop()
            if low < high:
                # Highlight current partition range
                self.record_step(
                    arr,
                    f"Partitioning subarray [{low}:{high+1}]",
                    {'comparing': list(range(low, high + 1))}
                )

                # Partition and get pivot index
                pivot_idx = self._partition(arr, low, high)

                self.record_step(
                    arr,
                    f"Pivot {arr[pivot_idx]} placed at index {pivot_idx}",
                    {'swapping': [pivot_idx], 'comparing': list(range(low, high + 1))}
                )

                # After partition, pivot is in final position
                sorted_ranges.append(pivot_idx)

                # Push right subarray, then left (stack is LIFO)
                stack.append((pivot_idx + 1, high))
                stack.append((low, pivot_idx - 1))

                # Highlight sorted pivot
                self.record_step(
                    arr,
                    f"Subarray [{low}:{high+1}] partitioned. Pivot {arr[pivot_idx]} is sorted.",
                    {'sorted': sorted_ranges.copy()}
                )

        self.end_time = time.time()
        self.record_step(arr, "Quick Sort completed!")
        return arr

    def _partition(self, arr, low, high):
        """Lomuto partition scheme: pivot is last element"""
        pivot = arr[high]
        i = low - 1  # Index of smaller element

        for j in range(low, high):
            # Highlight current comparison
            self.record_step(
                arr,
                f"Comparing {arr[j]} with pivot {pivot}",
                {'comparing': [j, high]}
            )
            
            if not self.compare(arr[j], pivot):  # arr[j] <= pivot
                i += 1
                if i != j:
                    self.swap(arr, i, j)
                    self.record_step(
                        arr,
                        f"Swapped {arr[i]} and {arr[j]}",
                        {'swapping': [i, j]}
                    )

        # Place pivot in correct position
        if i + 1 != high:
            self.swap(arr, i + 1, high)
        return i + 1