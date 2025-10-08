# sorting/cocktail_sort.py
import time
from .base_sorter import BaseSorter

class CocktailSort(BaseSorter):
    """
    Cocktail Sort (Bidirectional Bubble Sort)
    
    Steps:
    1. Bubble largest unsorted element to the right (like Bubble Sort)
    2. Bubble smallest unsorted element to the left
    3. Shrink the unsorted range from both ends
    4. Repeat until no swaps occur
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Cocktail Sort (Bidirectional Bubble)")

        if n <= 1:
            self.record_step(arr, "Array has 0 or 1 element. Already sorted!")
            self.end_time = time.time()
            return arr

        start = 0
        end = n - 1
        swapped = True

        pass_num = 0

        while swapped and start < end:
            swapped = False
            pass_num += 1

            # Forward pass (left to right) - bubble max to end
            self.record_step(
                arr,
                f"Pass {pass_num}a: Forward pass [{start}:{end+1}]",
                {'comparing': list(range(start, end + 1))}
            )

            for i in range(start, end):
                self.record_step(
                    arr,
                    f"Comparing {arr[i]} and {arr[i+1]}",
                    {'comparing': [i, i+1]}
                )
                if self.compare(arr[i], arr[i+1]):
                    self.swap(arr, i, i+1)
                    swapped = True
                    self.record_step(
                        arr,
                        f"Swapped {arr[i]} and {arr[i+1]}",
                        {'swapping': [i, i+1]}
                    )

            if not swapped:
                break

            end -= 1
            self.record_step(
                arr,
                f"Pass {pass_num}a complete. Largest element {arr[end+1]} is sorted.",
                {'sorted': list(range(end + 1, n))}
            )

            # Backward pass (right to left) - bubble min to start
            self.record_step(
                arr,
                f"Pass {pass_num}b: Backward pass [{start}:{end+1}]",
                {'comparing': list(range(start, end + 1))}
            )

            for i in range(end, start, -1):
                self.record_step(
                    arr,
                    f"Comparing {arr[i-1]} and {arr[i]}",
                    {'comparing': [i-1, i]}
                )
                if self.compare(arr[i-1], arr[i]):
                    self.swap(arr, i-1, i)
                    swapped = True
                    self.record_step(
                        arr,
                        f"Swapped {arr[i-1]} and {arr[i]}",
                        {'swapping': [i-1, i]}
                    )

            start += 1
            self.record_step(
                arr,
                f"Pass {pass_num}b complete. Smallest element {arr[start-1]} is sorted.",
                {'sorted': list(range(0, start)) + list(range(end + 1, n))}
            )

        self.end_time = time.time()
        self.record_step(arr, "Cocktail Sort completed!")
        return arr