import APPEND_PATH
import sys
from PySide6.QtWidgets import QWidget,QApplication,QVBoxLayout
from gui.widgets.py_credits_bar.py_credits import PyCredits

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(600,500)
        layout = QVBoxLayout(self)
        layout.addStretch()
        credits = PyCredits("@wink","0.1.1","#CCFFFF","Times New Roman",11,"#000000",8,7)
        credits.setFixedHeight(30)
        layout.addWidget(credits)

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
