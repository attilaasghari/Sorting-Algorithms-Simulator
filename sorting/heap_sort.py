# sorting/heap_sort.py
import time
from .base_sorter import BaseSorter

class HeapSort(BaseSorter):
    """
    Heap Sort Algorithm
    
    Steps:
    1. Build a max heap from the input data
    2. At this point, the largest item is at the root
    3. Replace it with the last item, reduce heap size by one
    4. Heapify the root
    5. Repeat while heap size > 1
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Heap Sort")

        # Build max heap (rearrange array)
        self.record_step(arr, "Building max heap...")
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i, heap_size=n)

        self.record_step(arr, "Max heap built. Starting extraction...")

        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            # Move current root to end
            if arr[0] != arr[i]:
                self.swap(arr, 0, i)
                self.record_step(
                    arr,
                    f"Moved max {arr[i]} to position {i}",
                    {'swapping': [0, i], 'sorted': list(range(i, n))}
                )
            else:
                self.record_step(
                    arr,
                    f"{arr[i]} is already in correct position.",
                    {'sorted': list(range(i, n))}
                )

            # Call heapify on the reduced heap
            self._heapify(arr, i, 0, heap_size=i)

        self.end_time = time.time()
        self.record_step(arr, "Heap Sort completed!")
        return arr

    def _heapify(self, arr, n, i, heap_size=None):
        """
        Heapify a subtree rooted at index i.
        n is the size of the heap.
        """
        if heap_size is None:
            heap_size = n

        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Highlight the subtree being heapified
        indices = [i]
        if left < heap_size:
            indices.append(left)
        if right < heap_size:
            indices.append(right)
        
        self.record_step(
            arr,
            f"Heapifying subtree rooted at {i} (value {arr[i]})",
            {'comparing': indices}
        )

        # Check if left child exists and is greater than root
        if left < heap_size:
            if self.compare(arr[largest], arr[left]):
                largest = left

        # Check if right child exists and is greater than largest so far
        if right < heap_size:
            if self.compare(arr[largest], arr[right]):
                largest = right

        # If largest is not root, swap and continue heapifying
        if largest != i:
            self.swap(arr, i, largest)
            self.record_step(
                arr,
                f"Swapped {arr[i]} and {arr[largest]} in heap",
                {'swapping': [i, largest], 'comparing': indices}
            )
            # Recursively heapify the affected sub-tree
            self._heapify(arr, heap_size, largest, heap_size)
        else:
            self.record_step(
                arr,
                f"Subtree rooted at {i} is already a max heap",
                {'comparing': indices}
            )