import APPEND_PATH
import sys
from PySide6.QtWidgets import QWidget,QApplication,QVBoxLayout
from gui.widgets.py_grips.py_grips import PyGrips

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.top_grips = PyGrips(self,"top")
        self.left_grips = PyGrips(self,"left")
        self.right_grips = PyGrips(self,"right")
        self.bottom_grips = PyGrips(self,"bottom")

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
