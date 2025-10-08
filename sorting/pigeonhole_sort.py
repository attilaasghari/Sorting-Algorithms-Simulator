# sorting/pigeonhole_sort.py
import time
from .base_sorter import BaseSorter

class PigeonholeSort(BaseSorter):
    """
    Pigeonhole Sort Algorithm
    
    Steps:
    1. Find min and max values to determine range
    2. Create pigeonholes (buckets) for each value in range
    3. Place each element in its corresponding pigeonhole
    4. Iterate through pigeonholes and put elements back in order
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Pigeonhole Sort")

        if n <= 1:
            self.record_step(arr, "Array has 0 or 1 element. Already sorted!")
            self.end_time = time.time()
            return arr

        min_val = int(min(arr))
        max_val = int(max(arr))
        range_val = max_val - min_val + 1

        self.record_step(
            arr,
            f"Input range: [{min_val}, {max_val}] → Range size = {range_val}, Array size = {n}"
        )

        # Check if pigeonhole sort is appropriate
        if range_val > n * 10:  # Heuristic: if range is much larger than n, warn
            self.record_step(
                arr,
                f"⚠️ Pigeonhole Sort is inefficient when range ({range_val}) >> n ({n})."
            )

        # Create pigeonholes
        pigeonholes = [[] for _ in range(range_val)]
        self.record_step(arr, f"Created {range_val} pigeonholes")

        # Place elements in pigeonholes
        for i, value in enumerate(arr):
            idx = int(value) - min_val
            pigeonholes[idx].append(value)
            self.record_step(
                arr,
                f"Placed {value} in pigeonhole {idx}",
                {'comparing': [i]}
            )

        # Reconstruct sorted array
        sorted_arr = []
        for i, hole in enumerate(pigeonholes):
            if hole:
                actual_value = min_val + i
                self.record_step(
                    sorted_arr + hole + [x for h in pigeonholes[i+1:] for x in h],
                    f"Emptying pigeonhole {i} (value {actual_value}): {hole}",
                    {'sorted': list(range(len(sorted_arr), len(sorted_arr) + len(hole)))}
                )
                sorted_arr.extend(hole)
            # else: empty pigeonhole — skip

        self.end_time = time.time()
        self.record_step(sorted_arr, "Pigeonhole Sort completed!")
        return sorted_arr