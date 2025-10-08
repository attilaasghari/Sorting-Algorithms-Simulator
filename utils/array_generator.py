# utils/array_generator.py
import numpy as np

def generate_array(size, array_type="random"):
    """
    Generate an array of given size and type.
    
    Parameters:
        size (int): Number of elements.
        array_type (str): One of 'random', 'ascending', 'descending', 'nearly_sorted'.
    
    Returns:
        np.ndarray: Generated array.
    """
    if array_type == "random":
        return np.random.randint(1, 1000, size)
    elif array_type == "ascending":
        return np.arange(1, size + 1)
    elif array_type == "descending":
        return np.arange(size, 0, -1)
    elif array_type == "nearly_sorted":
        arr = np.arange(1, size + 1)
        # Swap ~5% of adjacent pairs to create near-sortedness
        num_swaps = max(1, size // 20)
        for _ in range(num_swaps):
            i = np.random.randint(0, size - 1)
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
        return arr
    else:
        # Fallback to random
        return np.random.uniform(1, 1000, size).astype(int)