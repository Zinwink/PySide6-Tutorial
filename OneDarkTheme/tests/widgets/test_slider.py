import APPEND_PATH
import sys
from PySide6.QtWidgets import QWidget,QApplication,QVBoxLayout
from gui.widgets.py_slider.py_slider import PySlider
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.slider1 = PySlider(margin=2)
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider2 = PySlider()
        self.slider2.setOrientation(Qt.Vertical)
        layout = QVBoxLayout(self)
        layout.addWidget(self.slider1)
        layout.addWidget(self.slider2)

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()