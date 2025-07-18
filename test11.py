from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QPushButton, QHBoxLayout, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPainterPath

class RoundedStatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(10)

        # 添加控件
        self.btn_settings = QPushButton("设置")
        self.btn_help = QPushButton("帮助")
        self.label_status = QLabel("就绪")
        self.label_status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 设置为可勾选按钮（测试 :checked 状态）
        self.btn_settings.setCheckable(True)

        self.layout.addWidget(self.btn_settings)
        self.layout.addWidget(self.btn_help)
        self.layout.addStretch()
        self.layout.addWidget(self.label_status)

        # 需要设置按钮checked才能保持ckeck选中状态
        # 修正后的样式表
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #888;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background: #F0F0F0;
            }
            
            QPushButton:checked {
                background: #1976D2;
                color: white;
                font-weight: bold;
            }
            QLabel {
                color: #333;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)  # 调用父类绘制
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(240, 240, 240))
        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(rect, 10, 10)
        painter.drawPath(path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义状态栏（固定顶部）")
        self.setGeometry(100, 100, 600, 400)

        # 主容器（用于嵌套状态栏和内容）
        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)

        # 垂直布局：状态栏 + 内容
        self.vertical_layout = QVBoxLayout(self.main_container)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)  # 去除默认边距
        self.vertical_layout.setSpacing(0)

        # 1. 添加自定义状态栏到顶部
        self.status_bar = RoundedStatusBar()
        self.vertical_layout.addWidget(self.status_bar)

        # 2. 添加实际内容区域（示例：一个空白QWidget）
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: #f0f0f0;")
        self.vertical_layout.addWidget(self.content_widget)

    def resizeEvent(self, event):
        """窗口大小改变时，调整状态栏宽度"""
        self.status_bar.setFixedWidth(self.width())
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()