# sorting/shell_sort.py
import time
from .base_sorter import BaseSorter

class ShellSort(BaseSorter):
    """
    Shell Sort Algorithm (Using Knuth's sequence: 1, 4, 13, 40, ...)
    
    Steps:
    1. Start with a large gap (h)
    2. Perform gapped insertion sort for this gap
    3. Reduce gap and repeat until gap = 1
    4. Final pass is standard Insertion Sort
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Shell Sort (Knuth's sequence)")

        if n <= 1:
            self.record_step(arr, "Array has 0 or 1 element. Already sorted!")
            self.end_time = time.time()
            return arr

        # Generate Knuth's sequence: h = 3*h + 1
        gap = 1
        while gap < n // 3:
            gap = gap * 3 + 1

        pass_num = 0

        while gap >= 1:
            pass_num += 1
            self.record_step(
                arr,
                f"Pass {pass_num}: Gap = {gap}",
                {'comparing': list(range(n))}
            )

            # Gapped insertion sort
            for i in range(gap, n):
                key = arr[i]
                j = i
                # Highlight current element being inserted
                self.record_step(
                    arr,
                    f"Inserting {key} with gap {gap}",
                    {'comparing': [i]}
                )

                while j >= gap and self.compare(arr[j - gap], key):
                    arr[j] = arr[j - gap]
                    j -= gap
                    self.swaps += 1
                    self.record_step(
                        arr,
                        f"Shifted {arr[j]} right by gap {gap}",
                        {'swapping': [j, j + gap]}
                    )

                arr[j] = key
                self.swaps += 1

            gap //= 3

        self.end_time = time.time()
        self.record_step(arr, "Shell Sort completed!")
        return arr