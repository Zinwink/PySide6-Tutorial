import APPEND_PATH
import sys
from PySide6.QtWidgets import QWidget,QApplication,QVBoxLayout
from gui.widgets.py_toggle.py_toggle import PyToggle
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        toggle = PyToggle()
        layout = QVBoxLayout(self)
        layout.addWidget(toggle)
        
        toggle.toggled.connect(lambda x : print(x))
        toggle.stateChanged.connect(lambda x: print(x))

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()