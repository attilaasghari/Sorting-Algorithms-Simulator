# sorting/insertion_sort.py
import time
from .base_sorter import BaseSorter

class InsertionSort(BaseSorter):
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Insertion Sort")

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            # Highlight the element being inserted and the sorted portion
            self.record_step(
                arr,
                f"Inserting {key} into sorted subarray [0:{i}]",
                {'comparing': [i], 'sorted': list(range(i))}
            )

            # Move elements greater than key one position ahead
            while j >= 0:
                self.record_step(
                    arr,
                    f"Comparing {key} with {arr[j]}",
                    {'comparing': [j, i]}
                )
                if self.compare(arr[j], key):
                    arr[j + 1] = arr[j]
                    self.swaps += 1  # Treat shift as a swap for metric consistency
                    j -= 1
                    self.record_step(
                        arr,
                        f"Shifted {arr[j + 1]} right",
                        {'swapping': [j + 1, j + 2] if j + 2 < n else [j + 1]}
                    )
                else:
                    break

            arr[j + 1] = key
            self.record_step(
                arr,
                f"Inserted {key} at position {j + 1}",
                {'sorted': list(range(i + 1))}
            )

        self.end_time = time.time()
        self.record_step(arr, "Insertion Sort completed!")
        return arr