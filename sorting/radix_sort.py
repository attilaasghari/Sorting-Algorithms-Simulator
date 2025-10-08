# sorting/radix_sort.py
import time
from .base_sorter import BaseSorter
from .counting_sort import CountingSort

class RadixSort(BaseSorter):
    """
    Radix Sort Algorithm (Least Significant Digit - LSD)
    
    Steps:
    1. Find the maximum number to know number of digits
    2. Do counting sort for every digit (from least to most significant)
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Radix Sort (LSD)")

        if n == 0:
            self.record_step(arr, "Empty array. Sorting complete!")
            self.end_time = time.time()
            return arr

        # Handle negative numbers by separating and recombining
        negative = [x for x in arr if x < 0]
        positive = [x for x in arr if x >= 0]

        sorted_arr = []

        # Sort negative numbers (make positive, sort, then reverse and negate)
        if negative:
            neg_abs = [-x for x in negative]
            self.record_step(
                arr,
                f"Separating {len(negative)} negative numbers for special handling"
            )
            neg_sorted_abs = self._radix_sort_positive(neg_abs)
            neg_sorted = [-x for x in reversed(neg_sorted_abs)]  # Reverse for correct order
            sorted_arr.extend(neg_sorted)

        # Sort positive numbers
        if positive:
            pos_sorted = self._radix_sort_positive(positive)
            sorted_arr.extend(pos_sorted)

        self.end_time = time.time()
        self.record_step(sorted_arr, "Radix Sort completed!")
        return sorted_arr

    def _radix_sort_positive(self, arr):
        """Helper to sort non-negative integers using Radix Sort"""
        if not arr:
            return arr

        max_val = max(arr)
        digit_place = 1

        current_arr = arr.copy()

        while max_val // digit_place > 0:
            self.record_step(
                current_arr,
                f"Sorting by digit at place {digit_place} (units=1, tens=10, etc.)"
            )

            # Extract the current digit for each number
            digit_arr = [self._get_digit(x, digit_place) for x in current_arr]
            
            # Create a combined array for stable sorting: (digit, original_value)
            # But we'll use Counting Sort on digits while keeping original values
            current_arr = self._counting_sort_by_digit(current_arr, digit_place)
            
            self.record_step(
                current_arr,
                f"After sorting by digit {digit_place}: {current_arr}"
            )

            digit_place *= 10

        return current_arr

    def _get_digit(self, number, place):
        """Get the digit at the given place (1=units, 10=tens, etc.)"""
        return (number // place) % 10

    def _counting_sort_by_digit(self, arr, place):
        """Counting sort based on a specific digit place"""
        n = len(arr)
        if n == 0:
            return arr

        # Extract digits
        digits = [self._get_digit(x, place) for x in arr]
        max_digit = 9  # Digits are 0-9

        # Count frequencies (digits 0-9)
        count = [0] * 10
        for d in digits:
            count[d] += 1
            self.comparisons += 1  # Count as comparison

        # Cumulative count
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build output array (stable: iterate from back)
        output = [0] * n
        for i in range(n - 1, -1, -1):
            d = digits[i]
            pos = count[d] - 1
            output[pos] = arr[i]
            count[d] -= 1
            self.swaps += 1

        return output