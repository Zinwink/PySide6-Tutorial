import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

"""
QSplitter 允许用户通过拖动子控件的边界来控制子控件的大小,并提供了一个处理拖曳子
控件的控制器
QSplitter 中,各子控件默认是横向布局的,可以使用 Qt.Vertical 进行垂直布局

可以使用
setSizes()函数来设置所有小部件的大小,使用 sizes()函数返回用户设置的尺寸。也可以分
别使用 saveState()函数和 restoreState()函数保存和恢复小部件的大小状态。
如果使用 hide()函数隐藏一个小部件,那么它的空间将分配给其他控件。当再次使用 show()函数显示这个小部件时,它将被恢复。

addWidget()将小控件添加到 QSplitter 管理器的布局中
indexOf()返回小控件在 QSplitter 管理器中的索引
insertWidget()根据指定的索引将一个控件插入 QSplitter 管理器中
setOrientation()设置布局方向:Qt.Horizontal,水平方向;Qt.Vertical,垂直方向
setSizes()设置控件的初始大小
count()返回小控件在 QSplitter 管理器中的数量
saveState()保存拆分器布局的状态
restoreState()将拆分器的布局恢复到指定的状态。如果状态恢复则返回 True,否则返回 False
"""

class SplitterExample(QWidget):
    def __init__(self):
        super(SplitterExample, self).__init__()
        self.setting = {} #保存Splitter状态

        layout = QVBoxLayout(self)
        self.setWindowTitle("QSplitter布局管理例子")

        self.splitter1 = QSplitter()
        self.lineEidt = QLineEdit("lineEdit")
        self.splitter1.addWidget(self.lineEidt)
        self.splitter1.addWidget(QLabel("Label"))
        buttonShow = QPushButton("显/隐lineEdit")
        buttonShow.setCheckable(True)
        buttonShow.toggle()
        buttonShow.clicked.connect(lambda: self.buttonShowClick(buttonShow))
        self.splitter1.addWidget(buttonShow)
        layout.addWidget(self.splitter1)

        fram1 = QFrame()
        fram1.setFrameShape(QFrame.StyledPanel)
        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(fram1)
        self.splitter2.addWidget(QTextEdit())
        self.splitter2.setSizes([50, 100])
        layout.addWidget(self.splitter2)

        self.splitter3 = QSplitter(Qt.Horizontal)
        self.splitter3.addWidget(QListView())
        self.splitter3.addWidget(QTreeView())
        self.splitter3.addWidget(QTextEdit())
        # 是用于设置分割器（QSplitter）中各子部件初始大小
        # 50, 100, 150
        self.splitter3.setSizes([50, 100, 150])
        layout.addWidget(self.splitter3)

        buttonSave = QPushButton("SaveState")
        buttonSave.clicked.connect(self.saveSetting)
        buttonRestore = QPushButton('restoreState')
        buttonRestore.clicked.connect(self.restoreSetting)
        layout.addWidget(buttonSave)
        layout.addWidget(buttonRestore)

        self.setLayout(layout)

    def saveSetting(self):
        # 保存Splitter的状态
        self.setting.update({"splitter1":self.splitter1.saveState()})
        self.setting.update({"splitter2": self.splitter2.saveState()})
        self.setting.update({"splitter3": self.splitter3.saveState()})

    def restoreSetting(self):
        # 恢复状态
        self.splitter1.restoreState(self.setting["splitter1"])
        self.splitter2.restoreState(self.setting["splitter2"])
        self.splitter3.restoreState(self.setting["splitter3"])

    def buttonShowClick(self, button):
        if button.isChecked():
            self.lineEidt.show()
        else:
            self.lineEidt.hide()

if __name__=="__main__":
    app = QApplication(sys.argv)
    demo = SplitterExample()
    demo.show()
    demo.saveSetting()
    sys.exit(app.exec())