# sorting/counting_sort.py
import time
from .base_sorter import BaseSorter

class CountingSort(BaseSorter):
    """
    Counting Sort Algorithm
    
    Steps:
    1. Find the maximum value to determine range
    2. Create a count array to store frequency of each element
    3. Modify count array to store cumulative counts
    4. Build output array by placing elements at correct positions
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Counting Sort")

        if n == 0:
            self.record_step(arr, "Empty array. Sorting complete!")
            self.end_time = time.time()
            return arr

        # Only works for non-negative integers
        min_val = int(min(arr))
        max_val = int(max(arr))
        
        if min_val < 0:
            self.record_step(
                arr,
                f"⚠️ Counting Sort requires non-negative integers. Found min={min_val}."
            )
            # Shift all values to be non-negative
            shift = -min_val
            arr = [x + shift for x in arr]
            min_val = 0
            max_val = int(max(arr))
            self.record_step(
                arr,
                f"Shifted all values by +{shift} to make them non-negative."
            )

        k = max_val - min_val + 1  # Range of input
        self.record_step(
            arr,
            f"Input range: [{min_val}, {max_val}] → k = {k}"
        )

        # Step 1: Count frequencies
        count = [0] * k
        self.record_step(arr, "Counting frequencies of each element...")
        
        for i, num in enumerate(arr):
            idx = int(num) - min_val
            count[idx] += 1
            # Highlight current element being counted
            self.record_step(
                arr,
                f"Counted {num} (index {idx} in count array)",
                {'comparing': [i]}
            )

        self.record_step(arr, f"Frequency array: {count}")

        # Step 2: Cumulative count (positions)
        self.record_step(arr, "Computing cumulative counts (positions)...")
        for i in range(1, k):
            count[i] += count[i - 1]
            self.record_step(
                arr,
                f"Cumulative count at index {i}: {count[i]}",
                {'comparing': []}
            )

        # Step 3: Build output array (stable sort)
        output = [0] * n
        self.record_step(arr, "Building output array from back to front (for stability)...")

        for i in range(n - 1, -1, -1):
            num = int(arr[i])
            idx = num - min_val
            pos = count[idx] - 1  # Position in output
            output[pos] = num
            count[idx] -= 1
            
            self.record_step(
                output,
                f"Placed {num} at position {pos}",
                {'swapping': [pos]}
            )

        # If we shifted values earlier, shift back
        if min_val != int(min(self.original_array)):
            shift = min_val - int(min(self.original_array))
            output = [x - shift for x in output]
            self.record_step(
                output,
                f"Shifted values back by {-shift}"
            )

        self.end_time = time.time()
        self.record_step(output, "Counting Sort completed!")
        return output