# gui/visualization_widget.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect

class VisualizationWidget(QWidget):
    """
    Widget to visualize an array as vertical bars with value labels underneath.
    Supports highlighting for comparisons, swaps, and sorted regions.
    """
    def __init__(self):
        super().__init__()
        self.array = []
        self.highlights = {}  # e.g., {'comparing': [i,j], 'swapping': [k,l], 'sorted': [m,n,...]}

    def update_array(self, array, highlights=None):
        """Update the displayed array and highlights."""
        self.array = list(array) if array is not None else []
        self.highlights = highlights or {}
        self.update()  # Triggers repaint

    def paintEvent(self, event):
        if not self.array:
            return

        painter = QPainter(self)
        width = self.width()
        height = self.height()
        n = len(self.array)
        if n == 0:
            return

        # Reserve space at the bottom for labels (30px)
        label_height = 30
        drawing_height = height - label_height
        if drawing_height <= 0:
            drawing_height = height

        # Prevent division by zero
        bar_width = max(1, width // n)
        max_val = max(self.array) if self.array else 1
        min_val = min(self.array) if self.array else 0
        value_range = max_val - min_val if max_val != min_val else 1

        # Set up font for labels
        font_size = max(6, min(14, bar_width // 2))
        font = QFont("Segoe UI", font_size, QFont.Weight.Normal)
        painter.setFont(font)
        font_metrics = QFontMetrics(font)

        for i, val in enumerate(self.array):
            x = i * bar_width
            # Normalize value to [0,1] then scale to drawing_height
            normalized = (val - min_val) / value_range
            bar_height = int(normalized * drawing_height)
            y = drawing_height - bar_height  # Start from top of drawing area

            # Determine bar color
            color = QColor(70, 130, 180)  # SteelBlue (default)
            if i in self.highlights.get('comparing', []):
                color = QColor(220, 20, 60)      # Crimson (comparing)
            elif i in self.highlights.get('swapping', []):
                color = QColor(50, 205, 50)      # LimeGreen (swapping)
            elif i in self.highlights.get('sorted', []):
                color = QColor(169, 169, 169)    # DarkGray (sorted)

            # Draw bar
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawRect(QRect(x, y, bar_width, bar_height))

            # Draw value label centered under the bar
            label = str(int(val))
            text_width = font_metrics.horizontalAdvance(label)
            text_x = x + (bar_width - text_width) // 2
            text_y = height - 8  # 8px from bottom
            painter.setPen(QPen(Qt.GlobalColor.black))
            painter.drawText(text_x, text_y, label)