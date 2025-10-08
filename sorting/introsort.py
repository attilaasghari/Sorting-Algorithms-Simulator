# sorting/introsort.py
import time
import math
from .base_sorter import BaseSorter

class IntroSort(BaseSorter):
    """
    IntroSort Algorithm (Hybrid: Quick + Heap + Insertion)
    
    Steps:
    1. Use Quick Sort with depth limit = 2 * floor(log2(n))
    2. If depth limit reached, switch to Heap Sort for that subarray
    3. For small subarrays (size <= 16), use Insertion Sort
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start IntroSort (Hybrid: Quick + Heap + Insertion)")

        if n <= 1:
            self.record_step(arr, "Array has 0 or 1 element. Already sorted!")
            self.end_time = time.time()
            return arr

        # Stack stores (low, high, depth)
        max_depth = 2 * int(math.floor(math.log2(n))) if n > 1 else 0
        stack = [(0, n - 1, 0)]
        sorted_ranges = []

        while stack:
            low, high, depth = stack.pop()
            size = high - low + 1

            if size <= 1:
                continue

            # Use Insertion Sort for small arrays
            if size <= 16:
                self._insertion_sort_range(arr, low, high)
                sorted_ranges.extend(range(low, high + 1))
                self.record_step(
                    arr,
                    f"Used Insertion Sort on small subarray [{low}:{high+1}]",
                    {'sorted': sorted_ranges.copy()}
                )
                continue

            # Check depth limit
            if depth > max_depth:
                self._heap_sort_range(arr, low, high)
                sorted_ranges.extend(range(low, high + 1))
                self.record_step(
                    arr,
                    f"Depth limit exceeded. Used Heap Sort on [{low}:{high+1}]",
                    {'sorted': sorted_ranges.copy()}
                )
                continue

            # Quick Sort partition
            self.record_step(
                arr,
                f"Quick Sort partition on [{low}:{high+1}] (depth {depth}/{max_depth})",
                {'comparing': list(range(low, high + 1))}
            )

            pivot_idx = self._partition(arr, low, high)
            sorted_ranges.append(pivot_idx)

            self.record_step(
                arr,
                f"Pivot {arr[pivot_idx]} placed at index {pivot_idx}",
                {'swapping': [pivot_idx], 'sorted': sorted_ranges.copy()}
            )

            # Push right then left (LIFO)
            stack.append((pivot_idx + 1, high, depth + 1))
            stack.append((low, pivot_idx - 1, depth + 1))

        self.end_time = time.time()
        self.record_step(arr, "IntroSort completed!")
        return arr

    def _insertion_sort_range(self, arr, low, high):
        """Insertion sort on subarray arr[low..high]"""
        for i in range(low + 1, high + 1):
            key = arr[i]
            j = i - 1
            while j >= low and self.compare(arr[j], key):
                arr[j + 1] = arr[j]
                j -= 1
                self.swaps += 1
            arr[j + 1] = key
            self.swaps += 1

    def _heapify_range(self, arr, low, high, i):
        """Heapify subtree rooted at i within [low, high]"""
        largest = i
        left = 2 * (i - low) + 1 + low
        right = 2 * (i - low) + 2 + low

        if left <= high and self.compare(arr[largest], arr[left]):
            largest = left
        if right <= high and self.compare(arr[largest], arr[right]):
            largest = right

        if largest != i:
            self.swap(arr, i, largest)
            self._heapify_range(arr, low, high, largest)

    def _heap_sort_range(self, arr, low, high):
        """Heap Sort on subarray arr[low..high]"""
        n = high - low + 1
        # Build heap
        for i in range(low + n // 2 - 1, low - 1, -1):
            self._heapify_range(arr, low, high, i)
        # Extract elements
        for i in range(high, low, -1):
            self.swap(arr, low, i)
            self._heapify_range(arr, low, i - 1, low)

    def _partition(self, arr, low, high):
        """Lomuto partition scheme"""
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if not self.compare(arr[j], pivot):
                i += 1
                if i != j:
                    self.swap(arr, i, j)
        if i + 1 != high:
            self.swap(arr, i + 1, high)
        return i + 1