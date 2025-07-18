from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class RoundedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景（可选）
        
        # 设置圆角样式
        self.setStyleSheet("""
            QMainWindow {
                background: #2c3e50;  /* 背景色 */
                border-radius: 15px;  /* 圆角半径 */
            }
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
        """)

        # 添加一个按钮测试
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        button = QPushButton("关闭窗口")
        button.clicked.connect(self.close)
        layout.addWidget(button)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = RoundedWindow()
    window.resize(400, 300)
    window.show()
    app.exec()