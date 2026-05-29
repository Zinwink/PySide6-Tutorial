from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, 
    QApplication, QMainWindow, QTabWidget, QHBoxLayout,QFrame
)
from PySide6.QtCore import Qt, Signal,QSize
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath,QIcon

class LeftMenu(QFrame):
    tab_changed = Signal(int)

    def __init__(self, tab_widget):
        super().__init__()
        self.tab_widget = tab_widget
        self.buttons = []
        self.setup_ui()
        self.tab_widget.currentChanged.connect(self.emit_tab_changed)
        # QWidget默认透明， 不启用该属性， Qss设置背景和圆角无效 可以使用QFrame
        # self.setAttribute(Qt.WA_StyledBackground)  # 关键：启用 QSS 背景绘制

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 20, 10, 20)  # 增加内边距

        for i in range(self.tab_widget.count()):
            btn = QPushButton(self.tab_widget.tabText(i))
            btn.setIcon(QIcon("../OneDarkTheme/gui/images/svg_icons/icon_heart.svg"))
            # btn.setIconSize(QSize(24, 24))
            btn.setProperty("tab_index", i)
            btn.setCheckable(True)
            btn.clicked.connect(self.on_button_clicked)
            self.buttons.append(btn)
            layout.addWidget(btn)

        if self.buttons:
            self.buttons[0].setChecked(True)

        # 设置菜单背景样式
        self.setStyleSheet("""
            LeftMenu {
                background: #FFFFFF;
                border-radius: 12px;
            }
            QPushButton {
                padding: 12px 16px;
                text-align: left;
                border: none;
                background: transparent;
                color: #333;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #F0F0F0;
            }
            QPushButton:checked {
                background: #1976D2;
                color: white;
                font-weight: bold;
            }
        """)

    # def paintEvent(self, event):
    #     """ 绘制圆角背景和阴影 """
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)

    #     # 绘制圆角矩形背景
    #     path = QPainterPath()
    #     path.addRoundedRect(self.rect(), 12, 12)  # 圆角半径12px
    #     painter.fillPath(path, QColor("#FFFFFF"))

    #     # 绘制阴影（可选）
    #     painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
    #     painter.drawPath(path)

    def on_button_clicked(self):
        sender = self.sender()
        tab_index = sender.property("tab_index")
        self.tab_widget.setCurrentIndex(tab_index)

    def emit_tab_changed(self, index):
        self.tab_changed.emit(index)

    def update_button_state(self, index):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stylish Left Menu")
        self.setGeometry(100, 100, 900, 600)

        # 主布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 窗口边距
        main_layout.setSpacing(20)

        # 左侧菜单（带圆角背景）
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(QWidget(), "Home")
        self.tab_widget.addTab(QWidget(), "Settings")
        self.tab_widget.addTab(QWidget(), "Help")
        self.tab_widget.tabBar().setVisible(False)

        self.left_menu = LeftMenu(self.tab_widget)
        self.left_menu.tab_changed.connect(self.left_menu.update_button_state)

        # 右侧内容区域样式
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background: #FFFFFF;
            }
        """)

        # 布局比例：左侧1份，右侧3份
        main_layout.addWidget(self.left_menu, stretch=1)
        main_layout.addWidget(self.tab_widget, stretch=3)

        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()