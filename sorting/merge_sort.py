# sorting/merge_sort.py
import time
from .base_sorter import BaseSorter

class MergeSort(BaseSorter):
    """
    Merge Sort Algorithm (Iterative Bottom-Up Implementation)
    
    Steps:
    1. Treat each element as a sorted list of size 1
    2. Repeatedly merge adjacent sublists to produce new sorted sublists
    3. Continue until there is only one sublist remaining
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Merge Sort (Bottom-Up)")

        # Make a copy to work on
        working_arr = arr.copy()
        temp_arr = [0] * n  # Temporary array for merging

        size = 1
        while size < n:
            left = 0
            while left < n - 1:
                mid = min(left + size - 1, n - 1)
                right = min(left + size * 2 - 1, n - 1)

                # Only merge if right > mid (i.e., second subarray exists)
                if mid < right:
                    self.record_step(
                        working_arr,
                        f"Merging subarrays [{left}:{mid+1}] and [{mid+1}:{right+1}]",
                        {'comparing': list(range(left, right + 1))}
                    )

                    # Perform the merge
                    self._merge(working_arr, temp_arr, left, mid, right)

                    self.record_step(
                        working_arr,
                        f"Merged into sorted subarray [{left}:{right+1}]",
                        {'sorted': list(range(left, right + 1))}
                    )

                left += size * 2

            size *= 2

        self.end_time = time.time()
        self.record_step(working_arr, "Merge Sort completed!")
        return working_arr

    def _merge(self, arr, temp, left, mid, right):
        """Merge two sorted subarrays arr[left..mid] and arr[mid+1..right]"""
        i = left      # Starting index for left subarray
        j = mid + 1   # Starting index for right subarray
        k = left      # Starting index to be sorted

        # Copy data to temp array
        for idx in range(left, right + 1):
            temp[idx] = arr[idx]

        # Merge the temp arrays back into arr[left..right]
        while i <= mid and j <= right:
            if not self.compare(temp[i], temp[j]):  # temp[i] <= temp[j]
                arr[k] = temp[i]
                i += 1
            else:
                arr[k] = temp[j]
                j += 1
            k += 1
            self.swaps += 1  # Count as assignment/move

        # Copy remaining elements of left subarray, if any
        while i <= mid:
            arr[k] = temp[i]
            i += 1
            k += 1
            self.swaps += 1

        # Copy remaining elements of right subarray, if any
        while j <= right:
            arr[k] = temp[j]
            j += 1
            k += 1
            self.swaps += 1