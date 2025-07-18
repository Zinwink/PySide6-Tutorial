import APPEND_PATH
import sys
from PySide6.QtWidgets import QWidget,QApplication,QVBoxLayout
from gui.widgets.py_line_edit.py_line_edit import PyLineEdit
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.lineEdit = PyLineEdit()
        layout = QVBoxLayout(self)
        layout.addWidget(self.lineEdit)

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()