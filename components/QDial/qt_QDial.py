import sys
from PySide6.QtCore import * 
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qt_material import apply_stylesheet

class dialDemo(QWidget):
    def __init__(self,parent=None):
        super(dialDemo, self).__init__(parent)
        self.setWindowTitle("QDial 例子")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.label = QLabel("Hello Qt for Python")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # 普通qdial
        self.dial1 = QDial()
        self.dial1.setMinimum(10)
        self.dial1.setMaximum(50)
        self.dial1.setSingleStep(3)
        # setPageStep(5)	点击空白区域/PageUp/PageDown键	快速大范围调整
        # setSingleStep(1)	键盘方向键/鼠标拖动滑块	精细微调
        self.dial1.setPageStep(5)
        self.dial1.setValue(20)
        layout.addWidget(self.dial1)

        # 开启循环
        self.dial_wrap = QDial()
        self.dial_wrap.setMinimum(5)
        self.dial_wrap.setMaximum(25)
        self.dial_wrap.setSingleStep(1)
        self.dial_wrap.setPageStep(5)
        self.dial_wrap.setValue(15)
        # 用于设置循环 刻度 100 -->0 --->100
        self.dial_wrap.setWrapping(True)
        self.dial_wrap.setMinimumHeight(100)
        layout.addWidget(self.dial_wrap)
        # 连接信号槽
        self.dial1.valueChanged.connect(lambda :self.valuechange(self.dial1))
        self.dial_wrap.valueChanged.connect(lambda :self.valuechange(self.dial_wrap))

        self.setLayout(layout)

    
    def valuechange(self, dial):
        size = dial.value()
        self.label.setText("选中大小: %d"%size)
        self.label.setFont(QFont("Arial",size))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 每次滚动鼠标滚轮​​ 将滚动 ​​2 行内容
    app.setWheelScrollLines(2)
    apply_stylesheet(app,theme="light_blue.xml")
    demo = dialDemo()
    demo.show()
    sys.exit(app.exec())