from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, 
    QApplication, QMainWindow, QTabWidget, QHBoxLayout,QButtonGroup
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

class LeftMenu(QWidget):

    def __init__(self, tab_widget):
        super().__init__()
        self.tab_widget = tab_widget
        self.buttons = []  # 存储所有按钮
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(3)
        layout.setContentsMargins(0,0,0,0)
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)  # 关键：启用互斥
        # 动态生成按钮
        for i in range(self.tab_widget.count()):
            btn = QPushButton(self.tab_widget.tabText(i))
            btn.setProperty("tab_index", i)  # 存储按钮对应的 Tab 索引
            btn.setCheckable(True)          # 使按钮可选中（类似 RadioButton）
            btn.clicked.connect(self.on_button_clicked)
            self.button_group.addButton(btn)
            self.buttons.append(btn)
            layout.addWidget(btn)
        
        layout.addStretch()

        # 初始选中第一个按钮
        if self.buttons:
            self.buttons[0].setChecked(True)

    def on_button_clicked(self):
        # 获取被点击按钮的 Tab 索引
        sender = self.sender()
        tab_index = sender.property("tab_index")
        # 切换 Tab 页面
        self.tab_widget.setCurrentIndex(tab_index)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Left Menu with Sync Tabs")
        self.setGeometry(100, 100, 800, 600)

        # 主布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 右侧 TabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(QWidget(), "Home")
        self.tab_widget.addTab(QWidget(), "Settings")
        self.tab_widget.addTab(QWidget(), "Help")
        self.tab_widget.tabBar().setVisible(False)  # 隐藏 TabBar

        # 左侧菜单
        self.left_menu = LeftMenu(self.tab_widget)
        self.left_menu.setContentsMargins(5,2,0,2)
        self.left_menu.setFixedHeight(self.height())
        # self.left_menu.setStyleSheet(
        #     """
        #         background-color:#000000;
        #         border-radius:8px;
        #     """
        # )
        # 布局比例：左侧 1 份宽度，右侧 4 份宽度
        main_layout.addWidget(self.left_menu, stretch=1)
        main_layout.addWidget(self.tab_widget, stretch=4)

        # 设置样式
        self.set_style()

        self.setCentralWidget(central_widget)

    def set_style(self):
        # 全局样式表
        self.setStyleSheet("""
            /* 左侧菜单按钮 */
            LeftMenu {
                background-color: #2c3e50;
                border-radius: 12px;
            }
            QPushButton {
                padding: 12px 16px;
                text-align: left;
                border: none;
                background: #f5f5f5;
                color: #333;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
            QPushButton:checked {
                background: #1976D2;
                color: white;
                font-weight: bold;
            }

            /* 右侧 Tab 页面 */
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
            }
        """)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()