import APPEND_PATH
import sys
from PySide6.QtWidgets import QWidget,QApplication,QVBoxLayout,QToolButton,QFrame
from PySide6.QtGui import QIcon
from gui.widgets.py_left_menu.py_left_menu import PyLeftMenu
from gui.core.functions import Functions
import os
os.chdir(os.path.dirname(__file__))

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        frame = QFrame()
        frame.setMaximumSize(300, 400)
        frame.setMinimumSize(90, 400)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        menu = PyLeftMenu(frame,self)
        frame_layout.addWidget(menu)
        layout.addWidget(frame)
    

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()

