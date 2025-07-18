from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPainterPath

class RoundedStatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)  # 状态栏高度
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)  # 边距
        self.layout.setSpacing(10)  # 控件间距

        # 添加按钮或其他控件
        self.btn_settings = QPushButton("设置")
        self.btn_help = QPushButton("帮助")
        self.label_status = QLabel("就绪")
        self.label_status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.layout.addWidget(self.btn_settings)
        self.layout.addWidget(self.btn_help)
        self.layout.addStretch()  # 将右侧控件推到最右
        self.layout.addWidget(self.label_status)

        # 样式设置（可选）
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #888;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QLabel {
                color: #333;
            }
        """)

    def paintEvent(self, event):
        """绘制圆角背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(240, 240, 240))  # 背景色

        path = QPainterPath()
        rect = self.rect()
        radius = 10  # 圆角半径
        path.addRoundedRect(rect, radius, radius)
        painter.drawPath(path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义状态栏示例")
        self.setGeometry(100, 100, 600, 400)

        # 创建自定义状态栏并添加到窗口顶部
        self.status_bar = RoundedStatusBar()
        self.setMenuWidget(self.status_bar)  # 替换默认菜单栏

        # 主窗口内容（示例）
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()