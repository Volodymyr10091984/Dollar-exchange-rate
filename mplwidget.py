from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


# class widget class for graphics 
class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        fig = Figure()
        self.canvas = FigureCanvasQTAgg(fig)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
