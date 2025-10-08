# sorting/comb_sort.py
import time
from .base_sorter import BaseSorter

class CombSort(BaseSorter):
    """
    Comb Sort Algorithm
    
    Steps:
    1. Initialize gap as array length
    2. Set shrink factor (typically 1.3)
    3. While gap > 1 or swaps occurred:
        a. Update gap = floor(gap / shrink_factor)
        b. If gap < 1, set gap = 1
        c. Compare and swap elements gap apart
        d. Record if any swaps occurred
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Comb Sort")

        if n <= 1:
            self.record_step(arr, "Array has 0 or 1 element. Already sorted!")
            self.end_time = time.time()
            return arr

        gap = n
        shrink = 1.3
        swapped = True

        pass_num = 0

        while gap > 1 or swapped:
            # Update gap
            gap = int(gap / shrink)
            if gap < 1:
                gap = 1

            swapped = False
            pass_num += 1

            self.record_step(
                arr,
                f"Pass {pass_num}: Gap = {gap}",
                {'comparing': list(range(n - gap))}
            )

            # Compare elements gap apart
            for i in range(n - gap):
                self.record_step(
                    arr,
                    f"Comparing {arr[i]} and {arr[i + gap]} (gap={gap})",
                    {'comparing': [i, i + gap]}
                )
                if self.compare(arr[i], arr[i + gap]):
                    self.swap(arr, i, i + gap)
                    swapped = True
                    self.record_step(
                        arr,
                        f"Swapped {arr[i]} and {arr[i + gap]}",
                        {'swapping': [i, i + gap]}
                    )

            if gap == 1 and not swapped:
                self.record_step(
                    arr,
                    "No swaps with gap=1. Array is sorted."
                )

        self.end_time = time.time()
        self.record_step(arr, "Comb Sort completed!")
        return arr