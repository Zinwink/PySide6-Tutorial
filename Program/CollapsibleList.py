from PySide6 import QtWidgets

from PySide6 import QtCore, QtGui, QtWidgets

class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        # 初始为未选中状态 unchecked 当按下该按钮时 之前
        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        """
        QScrollArea 的 maximumHeight 控制的是什么？
        QScrollArea 是一个容器，它内部的内容是通过 setLayout() 或 setWidget() 设置的。
        如果内部内容的高度超过了 QScrollArea 的 maximumHeight，它就会自动出现垂直滚动条。
        所以，maximumHeight 决定了在不出现滚动条的情况下，最多能显示多少内容。

        为什么 sizePolicy=Fixed 还能改变高度？
        Fixed 部件大小固定为sizeHint()返回的值，不能拉伸或收缩
        sizePolicy=Fixed 表示控件不会根据父布局自动调整高度。
        但你仍然可以通过代码显式设置控件的高度（比如通过 setMaximumHeight() 或 setFixedSize() 等方法）。
        所以，动画通过 setMaximumHeight(...) 改变了它的最大高度，而 sizePolicy=Fixed 不会阻止这个行为，只是阻止了它自动扩展。

        """
        self.content_area = QtWidgets.QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    # @QtCore.pyqtSlot()
    def on_pressed(self):
        # 按钮按下 并 释放后 状态变为checked
        # 初始化为unckecked状态 且 Right导向
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow
        )
        # Forward表示 开始值（startValue）播放到结束值（endValue）
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()-1):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            # 同时改变 最小 最大 Height
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        # 对于存放项目的内容 设置最大高度
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


if __name__ == "__main__":
    import sys
    import random

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QMainWindow()
    w.setCentralWidget(QtWidgets.QWidget())
    dock = QtWidgets.QDockWidget("Collapsible Demo")
    w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
    scroll = QtWidgets.QScrollArea()
    dock.setWidget(scroll)
    content = QtWidgets.QWidget()
    scroll.setWidget(content)
    scroll.setWidgetResizable(True)
    vlay = QtWidgets.QVBoxLayout(content)
    for i in range(10):
        box = CollapsibleBox("Collapsible Box Header-{}".format(i))
        vlay.addWidget(box)
        lay = QtWidgets.QVBoxLayout()
        for j in range(8):
            # label = QtWidgets.QLabel("{}".format(j))
            btn = QtWidgets.QPushButton(f"btn-{j}")
            color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
            btn.setStyleSheet(
                "background-color: rgba(25, 118, 210,50%); color : white; border-radius: 3px; "
            )
            # label.setAlignment(QtCore.Qt.AlignCenter)
            lay.addWidget(btn)

        box.setContentLayout(lay)
    vlay.addStretch()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())