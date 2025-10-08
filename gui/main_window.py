# gui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QPushButton, QSlider, QLabel,
    QComboBox, QSpinBox, QTextEdit, QGroupBox, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from gui.visualization_widget import VisualizationWidget
from sorting import get_sorter
from utils.array_generator import generate_array
import numpy as np
import re

class SortingSimulatorMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorting Algorithm Simulator v1.0")
        self.resize(1200, 800)

        self.array = np.array([])
        self.sorter = None
        self.is_sorting = False
        self.paused = False
        self.step_index = 0

        self.init_ui()
        self.reset_array()
        self.apply_academic_theme()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        self.simulator_tab = self.create_simulator_tab()
        self.algorithms_tab = self.create_algorithms_tab()
        self.performance_tab = self.create_performance_tab()
        self.about_tab = self.create_about_tab()

        self.tabs.addTab(self.simulator_tab, "Simulator")
        self.tabs.addTab(self.algorithms_tab, "Algorithms")
        self.tabs.addTab(self.performance_tab, "Performance")
        self.tabs.addTab(self.about_tab, "About")

        main_layout.addWidget(self.tabs)

        self.timer = QTimer()
        self.timer.timeout.connect(self.run_step)

    def create_simulator_tab(self):
        # Main splitter: controls on left, visualization on right
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Controls (reduced width)
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setContentsMargins(8, 8, 8, 8)
        controls_layout.setSpacing(6)

        # Array configuration
        array_group = QGroupBox("Array")
        array_layout = QVBoxLayout()
        array_layout.setSpacing(4)
        
        # Size
        size_layout = QHBoxLayout()
        size_layout.setSpacing(4)
        size_layout.addWidget(QLabel("Size:"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(5, 1000)
        self.size_spin.setValue(50)
        self.size_spin.valueChanged.connect(self.reset_array)
        self.size_spin.setFixedWidth(80)
        size_layout.addWidget(self.size_spin)
        array_layout.addLayout(size_layout)
        
        # Type
        type_layout = QHBoxLayout()
        type_layout.setSpacing(4)
        type_layout.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Random", "Ascending", "Descending", "Nearly Sorted", "Custom"])
        self.type_combo.currentTextChanged.connect(self.toggle_custom_input)
        self.type_combo.currentTextChanged.connect(self.reset_array)
        type_layout.addWidget(self.type_combo)
        array_layout.addLayout(type_layout)
        
        array_group.setLayout(array_layout)
        controls_layout.addWidget(array_group)

        # Custom array input
        self.custom_array_input = QTextEdit()
        self.custom_array_input.setPlaceholderText("5,2,8,1")
        self.custom_array_input.setMaximumHeight(50)
        self.custom_array_input.hide()
        self.custom_array_input.setFixedHeight(50)
        controls_layout.addWidget(self.custom_array_input)

        # CSV button
        self.csv_btn = QPushButton("Import CSV")
        self.csv_btn.setFixedHeight(28)
        self.csv_btn.clicked.connect(self.import_csv)
        controls_layout.addWidget(self.csv_btn)

        # Algorithm selection
        algo_group = QGroupBox("Algorithm")
        algo_layout = QVBoxLayout()
        algo_layout.setContentsMargins(4, 4, 4, 4)
        self.algo_combo = QComboBox()
        self.algo_combo.addItems([
            "Bubble Sort", "Insertion Sort", "Selection Sort",
            "Merge Sort", "Quick Sort", "Heap Sort", "Shell Sort",
            "Counting Sort", "Radix Sort", "Bucket Sort", "Pigeonhole Sort",
            "Cocktail Sort", "Comb Sort", "IntroSort", "Bogo Sort"
        ])
        algo_layout.addWidget(self.algo_combo)
        algo_group.setLayout(algo_layout)
        controls_layout.addWidget(algo_group)

        # Speed control
        speed_group = QGroupBox("Speed")
        speed_layout = QVBoxLayout()
        speed_layout.setContentsMargins(4, 4, 4, 4)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        speed_layout.addWidget(self.speed_slider)
        speed_group.setLayout(speed_layout)
        controls_layout.addWidget(speed_group)

        # Control buttons - 2 column layout
        buttons_group = QGroupBox("Controls")
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(6)
        buttons_layout.setContentsMargins(6, 6, 6, 6)
        
        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.step_forward_btn = QPushButton("Step ▶")
        self.step_backward_btn = QPushButton("Step ◀")
        self.reset_btn = QPushButton("Reset")
        
        self.start_btn.clicked.connect(self.start_sorting)
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.reset_btn.clicked.connect(self.reset_all)
        self.step_forward_btn.clicked.connect(self.step_forward)
        self.step_backward_btn.clicked.connect(self.step_backward)
        
        # 2-column layout: start-pause, step forward-backward, reset centered
        buttons_layout.addWidget(self.start_btn, 0, 0)
        buttons_layout.addWidget(self.pause_btn, 0, 1)
        buttons_layout.addWidget(self.step_forward_btn, 1, 0)
        buttons_layout.addWidget(self.step_backward_btn, 1, 1)
        buttons_layout.addWidget(self.reset_btn, 2, 0, 1, 2)  # Spans both columns
        
        buttons_group.setLayout(buttons_layout)
        controls_layout.addWidget(buttons_group)

        controls_layout.addStretch()

        # Right panel: Visualization
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        self.vis_widget = VisualizationWidget()
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        self.explanation_text.setMaximumHeight(70)
        
        right_layout.addWidget(self.vis_widget)
        right_layout.addWidget(self.explanation_text)

        # Add widgets to splitter
        splitter.addWidget(controls_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([220, 980])  # Controls: 220px, Visualization: rest

        return splitter

    def create_algorithms_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Show ALL algorithms info
        all_algorithms_info = self.get_all_algorithms_info()
        
        self.algorithm_info = QTextEdit()
        self.algorithm_info.setReadOnly(True)
        self.algorithm_info.setHtml(all_algorithms_info)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.algorithm_info)
        
        layout.addWidget(QLabel("All Implemented Algorithms:"))
        layout.addWidget(scroll)
        return widget

    def get_all_algorithms_info(self):
        """Return HTML content for ALL algorithms"""
        algorithms = [
            ("Bubble Sort", "Basic Comparison Sort", "O(n²)", "O(1)", "Yes",
             "Repeatedly compares adjacent elements and swaps them if in wrong order."),
            ("Insertion Sort", "Basic Comparison Sort", "O(n²)", "O(1)", "Yes",
             "Builds sorted array one element at a time by inserting each element in correct position."),
            ("Selection Sort", "Basic Comparison Sort", "O(n²)", "O(1)", "No",
             "Selects minimum element from unsorted portion and swaps it to front."),
            ("Merge Sort", "Efficient Divide & Conquer", "O(n log n)", "O(n)", "Yes",
             "Divides array in half, recursively sorts, then merges sorted halves."),
            ("Quick Sort", "Efficient Divide & Conquer", "O(n log n) avg", "O(log n)", "No",
             "Partitions array around pivot, then recursively sorts sub-arrays."),
            ("Heap Sort", "Efficient Comparison Sort", "O(n log n)", "O(1)", "No",
             "Converts array to max heap, then repeatedly extracts maximum element."),
            ("Shell Sort", "Efficient Comparison Sort", "O(n log²n)", "O(1)", "No",
             "Generalization of insertion sort using gap sequences to move elements farther."),
            ("Counting Sort", "Non-Comparison Sort", "O(n + k)", "O(k)", "Yes",
             "Counts occurrences of each element, then reconstructs sorted array."),
            ("Radix Sort", "Non-Comparison Sort", "O(d·n)", "O(n + k)", "Yes",
             "Sorts numbers digit by digit using counting sort as subroutine."),
            ("Bucket Sort", "Non-Comparison Sort", "O(n) avg", "O(n)", "Yes",
             "Distributes elements into buckets, sorts each bucket, then concatenates."),
            ("Pigeonhole Sort", "Non-Comparison Sort", "O(n + k)", "O(n + k)", "Yes",
             "Places elements into pigeonholes based on value, then empties holes in order."),
            ("Cocktail Sort", "Basic Comparison Sort", "O(n²)", "O(1)", "Yes",
             "Bidirectional bubble sort that bubbles in both directions alternately."),
            ("Comb Sort", "Efficient Comparison Sort", "O(n log n) avg", "O(1)", "No",
             "Improvement over bubble sort using shrinking gap (factor 1.3)."),
            ("IntroSort", "Hybrid Advanced Sort", "O(n log n)", "O(log n)", "No",
             "Hybrid: starts with quicksort, switches to heapsort if depth limit exceeded."),
            ("Bogo Sort", "Joke/Randomized Sort", "O(n × n!)", "O(1)", "No",
             "Randomly shuffles until array happens to be sorted. Never use in practice!")
        ]
        
        html = "<h2>All Implemented Sorting Algorithms</h2>\n"
        html += "<style>table { border-collapse: collapse; width: 100%; } "
        html += "th, td { border: 1px solid #bdc3c7; padding: 8px; text-align: left; } "
        html += "th { background-color: #ecf0f1; font-weight: bold; } "
        html += "tr:nth-child(even) { background-color: #f8f9fa; }</style>\n"
        html += "<table>\n"
        html += "<thead>\n"
        html += "<tr>\n"
        html += "<th>Algorithm</th>\n"
        html += "<th>Category</th>\n"
        html += "<th>Time Complexity</th>\n"
        html += "<th>Space</th>\n"
        html += "<th>Stable</th>\n"
        html += "<th>Description</th>\n"
        html += "</tr>\n"
        html += "</thead>\n"
        html += "<tbody>\n"
        
        for name, category, time_comp, space, stable, desc in algorithms:
            html += "<tr>\n"
            html += f"<td><strong>{name}</strong></td>\n"
            html += f"<td>{category}</td>\n"
            html += f"<td>{time_comp}</td>\n"
            html += f"<td>{space}</td>\n"
            html += f"<td>{stable}</td>\n"
            html += f"<td>{desc}</td>\n"
            html += "</tr>\n"
        
        html += "</tbody>\n"
        html += "</table>\n"
        html += "<p><em>Note: Time complexity shows worst/average case unless specified.</em></p>"
        
        return html

    def create_performance_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        layout.addWidget(QLabel("Performance Metrics:"))
        layout.addWidget(self.metrics_text)
        return widget

    def create_about_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_content = """
<h2>Sorting Algorithm Simulator v1.0</h2>
<p>An educational desktop tool to visualize and compare sorting algorithms.</p>
<h3>Developer</h3>
<ul>
<li>Name: Attila Asghari</li>
<li>Website: <a href="https://ata.vitren.ir" style="color: blue;">https://ata.vitren.ir</a></li>
<li>Email: attilaasghari@gmail.com</li>
<li>GitHub: <a href="https://github.com/attilaasghari/Sorting-Algorithms-Simulator" style="color: blue;">https://github.com/attilaasghari/Sorting-Algorithms-Simulator</a></li>
<li>Software Website: <a href="https://ata.vitren.ir/projects/sas/" style="color: blue;">https://ata.vitren.ir/projects/sas/</a></li>
</ul>
<h3>Usage Instructions</h3>
<ol>
<li>Select array size and type.</li>
<li>Choose a sorting algorithm.</li>
<li>Click 'Start' to begin visualization.</li>
<li>Use 'Step' buttons to move manually.</li>
<li>Check 'Performance' tab for metrics.</li>
</ol>
<h3>Algorithms Included</h3>
<p><b>Basic:</b> Bubble, Insertion, Selection<br>
<b>Efficient:</b> Merge, Quick, Heap, Shell<br>
<b>Non-Comparison:</b> Counting, Radix, Bucket, Pigeonhole<br>
<b>Hybrid/Advanced:</b> IntroSort, Cocktail, Comb, Bogo</p>
"""
        about_text.setHtml(about_content)
        layout.addWidget(about_text)
        return widget

    def toggle_custom_input(self, text):
        if text == "Custom":
            self.custom_array_input.show()
            self.size_spin.setEnabled(False)
        else:
            self.custom_array_input.hide()
            self.size_spin.setEnabled(True)

    def import_csv(self):
        from PyQt6.QtWidgets import QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    line = f.readline().strip()
                numbers = re.split(r'[,\s]+', line)
                numbers = [x for x in numbers if x]
                self.array = np.array([float(x) for x in numbers])
                self.type_combo.setCurrentText("Custom")
                self.custom_array_input.setPlainText(','.join(map(str, self.array.astype(int))))
                self.vis_widget.update_array(self.array)
                self.explanation_text.setPlainText(f"Loaded {len(self.array)} values from {file_name}")
            except Exception as e:
                self.explanation_text.setPlainText(f"CSV Error: {e}")

    def reset_array(self):
        array_type = self.type_combo.currentText().lower().replace(" ", "_")
        
        if array_type == "custom":
            text = self.custom_array_input.toPlainText().strip()
            if not text:
                self.array = generate_array(10, "random")
            else:
                try:
                    numbers = re.split(r'[,\s]+', text)
                    numbers = [x for x in numbers if x]
                    self.array = np.array([float(x) for x in numbers])
                    if len(self.array) == 0:
                        self.array = generate_array(10, "random")
                except Exception as e:
                    self.array = generate_array(10, "random")
                    self.explanation_text.setPlainText(f"Invalid input: {e}. Using random array.")
        else:
            size = self.size_spin.value()
            self.array = generate_array(size, array_type)
        
        self.vis_widget.update_array(self.array)
        self.explanation_text.clear()
        self.metrics_text.clear()

    def reset_all(self):
        self.timer.stop()
        self.is_sorting = False
        self.paused = False
        self.step_index = 0
        self.sorter = None
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.reset_array()

    def start_sorting(self):
        if self.is_sorting:
            return
        algo_name = self.algo_combo.currentText()
        self.sorter = get_sorter(algo_name, self.array.copy())
        self.sorter.sort()
        self.is_sorting = True
        self.paused = False
        self.step_index = 0
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.pause_btn.setText("Pause")
        self.run_step()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.setText("Resume" if self.paused else "Pause")
        if not self.paused and self.is_sorting:
            self.run_step()

    def step_forward(self):
        if not self.sorter or not self.sorter.steps:
            return
        self.timer.stop()
        if self.step_index < len(self.sorter.steps):
            step = self.sorter.steps[self.step_index]
            self.vis_widget.update_array(step['array'], step.get('highlights', {}))
            self.explanation_text.setPlainText(step.get('explanation', ''))
            self.update_metrics_for_step(self.step_index)
            self.step_index += 1

    def step_backward(self):
        if not self.sorter or not self.sorter.steps or self.step_index <= 0:
            return
        self.timer.stop()
        self.step_index -= 1
        state = self.sorter.get_state_at(self.step_index)
        self.vis_widget.update_array(state['array'], state.get('highlights', {}))
        self.explanation_text.setPlainText(state.get('explanation', ''))
        self.update_metrics_for_step(self.step_index)

    def run_step(self):
        if not self.is_sorting or self.paused:
            return

        if self.step_index >= len(self.sorter.steps):
            self.sorting_finished()
            return

        step = self.sorter.steps[self.step_index]
        self.vis_widget.update_array(step['array'], step.get('highlights', {}))
        self.explanation_text.setPlainText(step.get('explanation', ''))
        self.update_metrics_for_step(self.step_index)

        self.step_index += 1

        if self.step_index < len(self.sorter.steps):
            delay = max(10, 200 - self.speed_slider.value() * 2)
            self.timer.start(delay)
        else:
            self.sorting_finished()

    def update_metrics_for_step(self, step_index):
        if not self.sorter:
            return
        total_comparisons = self.sorter.comparisons
        total_swaps = self.sorter.swaps
        total_time = self.sorter.get_metrics()['time']

        total_steps = len(self.sorter.steps)
        if total_steps == 0:
            progress = 1.0
        else:
            progress = min(1.0, step_index / total_steps)

        current_comparisons = int(total_comparisons * progress)
        current_swaps = int(total_swaps * progress)
        current_time = total_time * progress

        text = (
            f"Comparisons: {current_comparisons}\n"
            f"Swaps: {current_swaps}\n"
            f"Time: {current_time:.4f} seconds (estimated)"
        )
        self.metrics_text.setPlainText(text)

    def sorting_finished(self):
        self.timer.stop()
        self.is_sorting = False
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.explanation_text.append("\n✅ Sorting completed!")

    def apply_academic_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #ffffff;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
                color: #2c3e50;
                font-size: 10pt;
            }
            QGroupBox {
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
                padding-bottom: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-height: 26px;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QSlider::groove:horizontal {
                height: 5px;
                background: #ecf0f1;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 1px solid #2980b9;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
                background: #f8f9fa;
                font-size: 9pt;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                top: -1px;
            }
            QTabBar::tab {
                background: #ecf0f1;
                padding: 6px 12px;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 10pt;
            }
            QTabBar::tab:selected {
                background: white;
                font-weight: bold;
            }
            QComboBox, QSpinBox {
                padding: 3px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                min-height: 22px;
                font-size: 9pt;
            }
            QLabel {
                padding: 1px;
                font-size: 9pt;
            }
            QScrollArea {
                border: none;
            }
        """)