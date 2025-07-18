import APPEND_PATH
import sys
from PySide6.QtWidgets import QWidget,QApplication,QVBoxLayout,QToolButton
from PySide6.QtGui import QIcon
from gui.widgets.py_icon_button.py_icon_button import PyIconButton
from gui.core.functions import Functions
import os
os.chdir(os.path.dirname(__file__))

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        btn1 = QToolButton()
        btn1.setIcon(QIcon("../../gui/images/svg_icons/icon_close.svg"))
        btn1.setStyleSheet(
        '''
        QToolButton {
            background-color: #99CCCC;    /* 默认背景色 */
            border: none;
            border-radius: 5px;
            padding: 5px;
            color: #ff0000;  /* 红色 */
        }
        QToolButton:hover {
            background-color: #FFCC99;    /* 悬停颜色 */
            color: #ff0000;  /* 红色 */
        }
        QToolButton:pressed {
            background-color: #FF6666;    /* 按下颜色 */
            color: #ff0000;  /* 红色 */
        }
        '''
        )

        # btn2 = PyIconButton(icon_color=Functions.set_svg_icon("icon_busy.svg"),parent=None,app_parent=self,tooltip_text="button ok")
        layout.addWidget(btn1)
        # layout.addWidget(btn2)
    

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()

