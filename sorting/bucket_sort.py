# sorting/bucket_sort.py
import time
from .base_sorter import BaseSorter

class BucketSort(BaseSorter):
    """
    Bucket Sort Algorithm
    
    Steps:
    1. Create n empty buckets
    2. Put array elements in different buckets based on value
    3. Sort individual buckets (using Insertion Sort)
    4. Concatenate all buckets into sorted array
    """
    def sort(self):
        arr = self.original_array.copy()
        n = len(arr)
        self.start_time = time.time()

        self.record_step(arr, "Start Bucket Sort")

        if n <= 1:
            self.record_step(arr, "Array has 0 or 1 element. Already sorted!")
            self.end_time = time.time()
            return arr

        # Handle any range by normalizing to [0, 1)
        min_val = min(arr)
        max_val = max(arr)
        range_val = max_val - min_val if max_val != min_val else 1

        self.record_step(
            arr,
            f"Input range: [{min_val:.2f}, {max_val:.2f}] → Normalizing to [0, 1)"
        )

        # Create n empty buckets
        buckets = [[] for _ in range(n)]
        self.record_step(arr, f"Created {n} empty buckets")

        # Distribute input array values into buckets
        for i, value in enumerate(arr):
            # Normalize value to [0, 1)
            normalized = (value - min_val) / range_val
            # Avoid index = n when value == max_val
            bucket_index = min(int(normalized * n), n - 1)
            buckets[bucket_index].append(value)
            
            self.record_step(
                arr,
                f"Distributed {value:.2f} into bucket {bucket_index}",
                {'comparing': [i]}
            )

        # Show bucket distribution
        bucket_summary = [f"Bucket {i}: {len(b)} items" for i, b in enumerate(buckets) if b]
        self.record_step(
            arr,
            "Bucket distribution:\n" + "\n".join(bucket_summary)
        )

        # Sort individual buckets and concatenate
        sorted_arr = []
        for i, bucket in enumerate(buckets):
            if bucket:
                self.record_step(
                    sorted_arr + bucket + [x for b in buckets[i+1:] for x in b],
                    f"Sorting bucket {i} with {len(bucket)} elements",
                    {'comparing': list(range(len(sorted_arr), len(sorted_arr) + len(bucket)))}
                )
                
                # Sort bucket using Insertion Sort logic (in-place)
                bucket_sorted = self._insertion_sort_bucket(bucket)
                sorted_arr.extend(bucket_sorted)
                
                self.record_step(
                    sorted_arr + [x for b in buckets[i+1:] for x in b],
                    f"Bucket {i} sorted: {bucket_sorted}",
                    {'sorted': list(range(len(sorted_arr) - len(bucket_sorted), len(sorted_arr)))}
                )
            else:
                self.record_step(
                    sorted_arr + [x for b in buckets[i+1:] for x in b],
                    f"Bucket {i} is empty"
                )

        self.end_time = time.time()
        self.record_step(sorted_arr, "Bucket Sort completed!")
        return sorted_arr

    def _insertion_sort_bucket(self, bucket):
        """Simple insertion sort for a single bucket"""
        arr = bucket.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and self.compare(arr[j], key):
                arr[j + 1] = arr[j]
                j -= 1
                self.swaps += 1
            arr[j + 1] = key
            self.swaps += 1
        return arr