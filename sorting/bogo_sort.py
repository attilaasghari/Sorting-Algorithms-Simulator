# sorting/bogo_sort.py
import time
import random
from .base_sorter import BaseSorter

class BogoSort(BaseSorter):
    """
    Bogo Sort (Stupid Sort, Monkey Sort, Permutation Sort)
    
    Steps:
    1. Check if array is sorted
    2. If not, randomly shuffle the array
    3. Repeat until sorted
    
    ⚠️ WARNING: This algorithm has O(n!) average time complexity.
    Only use for arrays with n <= 8!
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Bogo Sort (Random Shuffle Until Sorted)")

        if n <= 1:
            self.record_step(arr, "Array has 0 or 1 element. Already sorted!")
            self.end_time = time.time()
            return arr

        if n > 8:
            self.record_step(
                arr,
                "⚠️ Bogo Sort is EXTREMELY SLOW for n > 8!\n"
                "Consider using a real sorting algorithm instead."
            )

        attempts = 0
        max_attempts = 10000  # Safety limit to avoid infinite loop

        while not self._is_sorted(arr):
            attempts += 1
            if attempts > max_attempts:
                self.record_step(
                    arr,
                    f"⚠️ Gave up after {max_attempts} attempts! Array may never sort randomly."
                )
                break

            # Randomly shuffle
            random.shuffle(arr)
            self.swaps += n  # Count as n swaps (full shuffle)
            
            if attempts % 100 == 0 or attempts <= 10:
                self.record_step(
                    arr,
                    f"Attempt {attempts}: Random shuffle",
                    {'comparing': list(range(n))}
                )

        self.end_time = time.time()
        if self._is_sorted(arr):
            self.record_step(arr, f"Bogo Sort completed in {attempts} attempts! 🎉")
        else:
            self.record_step(arr, "Bogo Sort failed to sort within attempt limit.")
        return arr

    def _is_sorted(self, arr):
        """Check if array is sorted in non-decreasing order"""
        for i in range(len(arr) - 1):
            self.comparisons += 1
            if self.compare(arr[i], arr[i + 1]):
                return False
        return True