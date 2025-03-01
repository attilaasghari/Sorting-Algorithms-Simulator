import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

class SortingSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Sorting Algorithms Simulator")

        # Variables
        self.data = []
        self.original_data = []
        self.sorting = False
        self.current_algorithm = tk.StringVar()
        self.start_time = 0
        self.timer_var = tk.StringVar()
        self.timer_var.set("Time: 0.00s")
        self.array_size = tk.IntVar(value=30)
        self.element_count_var = tk.StringVar()
        
        # Setup UI
        self.create_widgets()
        self.generate_new_array()

    def create_widgets(self):
        # Control Frame
        control_frame = ttk.Frame(self.master)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Left Control Panel
        left_control = ttk.Frame(control_frame)
        left_control.pack(side=tk.LEFT)
        
        # Array Controls
        ttk.Label(left_control, text="Elements:").pack(side=tk.LEFT)
        size_entry = ttk.Entry(left_control, textvariable=self.array_size, width=5)
        size_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(left_control, text="Generate", command=self.generate_new_array).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_control, text="Reset Array", command=self.reset_array).pack(side=tk.LEFT, padx=5)
        
        # Right Control Panel
        right_control = ttk.Frame(control_frame)
        right_control.pack(side=tk.RIGHT)
        
        # About Button
        ttk.Button(right_control, text="About", command=self.show_about).pack(side=tk.RIGHT, padx=5)
        
        # Algorithm Selection
        algorithms = ['Bubble Sort', 'Insertion Sort', 'Selection Sort', 
                      'Merge Sort', 'Quick Sort', 'Heap Sort']
        self.algorithm_menu = ttk.Combobox(right_control, textvariable=self.current_algorithm, values=algorithms)
        self.algorithm_menu.pack(side=tk.LEFT, padx=5)
        self.algorithm_menu.current(0)
        
        # Sorting Controls
        ttk.Button(right_control, text="Start", command=self.start_sorting).pack(side=tk.LEFT, padx=5)
        ttk.Button(right_control, text="Stop", command=self.stop_sorting).pack(side=tk.LEFT, padx=5)
        
        # Info Panel
        info_frame = ttk.Frame(self.master)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(info_frame, textvariable=self.timer_var).pack(side=tk.LEFT)
        ttk.Label(info_frame, textvariable=self.element_count_var).pack(side=tk.RIGHT)
        
        # Plot Area
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Array Display
        self.array_label = ttk.Label(self.master, text="Array: []")
        self.array_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def show_about(self):
        about_window = tk.Toplevel(self.master)
        about_window.title("About Sorting Algorithms Simulator")
        about_window.geometry("400x300")
        
        about_text = """
        Sorting Algorithms Simulator v1.0
        
        Developed by: Attila Asghari
        Created: 2024
        Contact: attilaasghari@gmail.com
        Website: https://attilaasghari.github.io/
        GitHub: https://github.com/attilaasghari/Sorting-Algorithms-Simulator
        
        This software provides visualization of various sorting 
        algorithms including:
        - Bubble Sort
        - Insertion Sort
        - Selection Sort
        - Merge Sort
        - Quick Sort
        - Heap Sort
        
        Features:
        - Real-time visualization
        - Adjustable array size
        - Performance timing
        - Multiple algorithm comparison
        - Interactive controls
        
        Licensed under MIT Open Source License
        """
        
        ttk.Label(about_window, text="About", font=('Arial', 14, 'bold')).pack(pady=5)
        ttk.Label(about_window, text=about_text.strip(), justify=tk.LEFT).pack(padx=10, pady=10)
        ttk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=5)

    def generate_new_array(self):
        try:
            size = max(3, min(self.array_size.get(), 500))  # Limit between 3 and 500
            self.array_size.set(size)
        except:
            size = 30
            self.array_size.set(size)
            
        self.data = [random.randint(10, 500) for _ in range(size)]
        self.original_data = self.data.copy()
        self.element_count_var.set(f"Elements: {len(self.data)}")
        self.update_plot()
        self.update_array_display()

    def reset_array(self):
        self.data = self.original_data.copy()
        self.timer_var.set("Time: 0.00s")
        self.sorting = False
        self.update_plot()
        self.update_array_display()

    def update_plot(self, highlight=[]):
        self.ax.clear()
        self.ax.set_title("Sorting Visualization")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        colors = ['lightblue' if i not in highlight else 'red' for i in range(len(self.data))]
        self.bars = self.ax.bar(range(len(self.data)), self.data, color=colors)
        
        # Add value labels on bars
        for bar, value in zip(self.bars, self.data):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                         f'{value}',
                         ha='center', va='bottom', fontsize=8)
        
        self.canvas.draw()
        self.update_array_display()

    def update_array_display(self):
        if len(self.data) > 20:
            front = ', '.join(map(str, self.data[:10]))
            back = ', '.join(map(str, self.data[-10:]))
            text = f"[{front}, ..., {back}]"
        else:
            text = str(self.data)
        self.array_label.config(text=f"Array: {text}")

    def start_sorting(self):
        if not self.sorting and len(self.data) > 0:
            self.sorting = True
            self.start_time = time.time()
            self.timer_var.set("Time: 0.00s")
            self.update_timer()
            algorithm = self.current_algorithm.get()
            
            # Reset generator based on algorithm
            if algorithm == 'Bubble Sort':
                sort_generator = self.bubble_sort()
            elif algorithm == 'Insertion Sort':
                sort_generator = self.insertion_sort()
            elif algorithm == 'Selection Sort':
                sort_generator = self.selection_sort()
            elif algorithm == 'Merge Sort':
                sort_generator = self.merge_sort()
            elif algorithm == 'Quick Sort':
                sort_generator = self.quick_sort()
            elif algorithm == 'Heap Sort':
                sort_generator = self.heap_sort()
            
            self.animate_sort(sort_generator)

    def stop_sorting(self):
        self.sorting = False

    def update_timer(self):
        if self.sorting:
            elapsed = time.time() - self.start_time
            self.timer_var.set(f"Time: {elapsed:.2f}s")
            self.master.after(100, self.update_timer)

    def animate_sort(self, generator):
        if not self.sorting:
            return
        try:
            highlighted = next(generator)
            self.update_plot(highlighted)
            self.master.after(50, lambda: self.animate_sort(generator))
        except StopIteration:
            self.sorting = False
            self.update_plot()
            self.timer_var.set(f"Final Time: {time.time() - self.start_time:.2f}s")
            
    # Sorting Algorithms (as generators)
    def bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.data[j] > self.data[j+1]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
                    yield [j, j+1]
        yield []

    def insertion_sort(self):
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i-1
            while j >=0 and key < self.data[j] :
                self.data[j+1] = self.data[j]
                j -= 1
                yield [j+1, j]
            self.data[j+1] = key
            yield [j+1]
        yield []

    def selection_sort(self):
        for i in range(len(self.data)):
            min_idx = i
            for j in range(i+1, len(self.data)):
                if self.data[min_idx] > self.data[j]:
                    min_idx = j
                yield [i, j]
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
            yield [i, min_idx]
        yield []

    def merge_sort(self):
        def merge(low, mid, high):
            temp = []
            left = low
            right = mid + 1
            
            while left <= mid and right <= high:
                if self.data[left] <= self.data[right]:
                    temp.append(self.data[left])
                    left += 1
                else:
                    temp.append(self.data[right])
                    right += 1
                yield [left, right]
            
            while left <= mid:
                temp.append(self.data[left])
                left += 1
                yield [left]
            
            while right <= high:
                temp.append(self.data[right])
                right += 1
                yield [right]
            
            for i in range(len(temp)):
                self.data[low + i] = temp[i]
                yield [low + i]

        def helper(low, high):
            if low < high:
                mid = (low + high) // 2
                yield from helper(low, mid)
                yield from helper(mid + 1, high)
                yield from merge(low, mid, high)
        
        yield from helper(0, len(self.data)-1)
        yield []

    def quick_sort(self):
        def partition(low, high):
            pivot = self.data[high]
            i = low - 1
            for j in range(low, high):
                if self.data[j] <= pivot:
                    i += 1
                    self.data[i], self.data[j] = self.data[j], self.data[i]
                    yield [i, j]
            self.data[i+1], self.data[high] = self.data[high], self.data[i+1]
            yield [i+1, high]
            return i + 1

        def helper(low, high):
            if low < high:
                pi = yield from partition(low, high)
                yield from helper(low, pi-1)
                yield from helper(pi+1, high)
        
        yield from helper(0, len(self.data)-1)
        yield []

    def heap_sort(self):
        def heapify(n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            if l < n and self.data[i] < self.data[l]:
                largest = l
                yield [i, l]

            if r < n and self.data[largest] < self.data[r]:
                largest = r
                yield [largest, r]

            if largest != i:
                self.data[i], self.data[largest] = self.data[largest], self.data[i]
                yield [i, largest]
                yield from heapify(n, largest)

        n = len(self.data)
        for i in range(n//2 - 1, -1, -1):
            yield from heapify(n, i)
        
        for i in range(n-1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]
            yield [i, 0]
            yield from heapify(i, 0)
        yield []

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingSimulator(root)
    root.mainloop()