import APPEND_PATH
import sys
from gui.widgets.py_circular_progress.py_circular_progress import PyCircularProgress
from PySide6.QtWidgets import QMainWindow,QWidget, QHBoxLayout,QApplication,QSlider,QSizePolicy

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(400,500)
        layout = QHBoxLayout()
        circleProgress = PyCircularProgress()
        # circleProgress.setFixedSize(100,100)
        circleProgress.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding)
        layout.addWidget(circleProgress)
        slider = QSlider()
        slider.setRange(0,100)
        slider.valueChanged.connect(lambda x : circleProgress.set_value(x))
        layout.addWidget(slider)
        self.setLayout(layout)
        

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()