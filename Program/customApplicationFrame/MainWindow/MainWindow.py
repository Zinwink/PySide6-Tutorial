from title_bar import TitleBar
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QApplication,QMainWindow,QFrame
from PySide6.QtCore import Qt
from grips import *
import sys

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景（必须选）
        self.centralWidget = QFrame()
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(8,8,8,8)
        self.central_layout.addWidget(self.centralWidget)
        self.centralWidget.setStyleSheet(
            """
            background-color : #CCCCCC;
            border-radius: 8px
            """
        )
        self.resize(900,500)
        self.setMinimumSize(900,500)
        self.title_bar = TitleBar(self)
        self.title_bar.setFixedHeight(50)
        self.title_bar.set_title("windows")
        layout = QVBoxLayout(self.centralWidget)
        layout.setContentsMargins(0,0,0,0)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(2,1,2,0)
        title_layout.addWidget(self.title_bar)
        layout.addLayout(title_layout)
        widget = QWidget()
        layout.addWidget(widget)
        self.left_grip = GripsLeft(self,True)
        self.right_grip = GripsRight(self,True)
        self.top_grip = GripsTop(self,True)
        self.bottom_grip = GripsBottom(self, True)
        self.top_right_grip = GripsTopRight(self, True)
        self.bottom_left_grip = GripsBottomLeft(self, True)
        self.bottom_right_grip = GripsBottomRight(self,True)
        # layout.addStretch()
        # self.title_bar.s

    def resizeEvent(self, event):
        self.left_grip.setGeometry(5, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
        self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
        self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
        self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
        self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
        self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
    
    # def resizeEvent(self, event):
    #     self.title_bar.setGeometry()
    
    # def 

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()