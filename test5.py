from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QHBoxLayout,QVBoxLayout, QPushButton, QLabel)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # 保存父窗口引用
        self.setFixedHeight(30)  # 设置标题栏高度
        
        # 创建布局和控件
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        
        # 标题图标和文本
        self.icon = QLabel()
        self.icon.setPixmap(QIcon(":/icons/app_icon.png").pixmap(20, 20))
        self.title = QLabel("我的应用程序")
        self.title.setStyleSheet("font-weight: bold;")
        
        # 添加空白区域使标题居中
        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addStretch()
        
        # 窗口控制按钮
        self.min_btn = QPushButton("—")
        self.max_btn = QPushButton("□")
        self.close_btn = QPushButton("×")
        
        # 设置按钮样式
        btn_style = """
            QPushButton {
                border: none;
                padding: 2px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e5e5e5;
            }
            QPushButton#close_btn:hover {
                background-color: #e81123;
                color: white;
            }
        """
        self.min_btn.setStyleSheet(btn_style)
        self.max_btn.setStyleSheet(btn_style)
        self.close_btn.setStyleSheet(btn_style)
        self.close_btn.setObjectName("close_btn")
        
        # 连接按钮信号
        self.min_btn.clicked.connect(self.parent.showMinimized)
        self.max_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.parent.close)
        
        # 添加按钮到布局
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)
    
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent.showMaximized()
            self.max_btn.setText("❐")
    
    # 以下方法用于实现窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.drag_start_position = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if not self.parent.isMaximized() and hasattr(self.parent, 'drag_start_position'):
            if event.buttons() & Qt.LeftButton:
                delta = event.globalPosition().toPoint() - self.parent.drag_start_position
                self.parent.move(self.parent.pos() + delta)
                self.parent.drag_start_position = event.globalPosition().toPoint()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # 创建主窗口内容
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 添加自定义标题栏
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # 添加内容区域
        content = QWidget()
        content.setStyleSheet("background-color: white;")
        main_layout.addWidget(content)
        
        # 窗口大小
        self.resize(800, 600)
        
        # 窗口阴影效果
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                border-radius: 4px;
            }
        """)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()