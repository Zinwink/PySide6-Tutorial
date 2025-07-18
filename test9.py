import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, 
    QPushButton, QLabel, QSizeGrip,QVBoxLayout
)
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QCursor


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #333; color: white;")
        
        # 创建布局和控件
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        
        self.title_label = QLabel("自定义标题栏")
        self.title_label.setStyleSheet("font-weight: bold;")
        
        # 最小化、最大化/还原、关闭按钮
        self.min_btn = QPushButton("-")
        self.max_btn = QPushButton("□")
        self.close_btn = QPushButton("×")
        
        # 设置按钮样式
        btn_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
                padding: 0 8px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton#close_btn:hover {
                background-color: #f00;
            }
        """
        self.min_btn.setStyleSheet(btn_style)
        self.max_btn.setStyleSheet(btn_style)
        self.close_btn.setStyleSheet(btn_style)
        self.close_btn.setObjectName("close_btn")
        
        # 添加控件到布局
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)
        
        # 连接按钮信号
        self.min_btn.clicked.connect(self.parent.showMinimized)
        self.max_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.parent.close)
        
        # 拖动窗口相关变量
        self.dragging = False
        self.offset = QPoint()
    
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent.showMaximized()
            self.max_btn.setText("▣")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint() - self.parent.pos()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.parent.move(event.globalPosition().toPoint() - self.offset)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
        event.accept()


class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义标题栏窗口")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setMinimumSize(400, 300)
        
        # 创建自定义标题栏
        self.title_bar = CustomTitleBar(self)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 添加标题栏和内容区域
        main_layout.addWidget(self.title_bar)
        
        # 添加一个示例内容标签
        content_label = QLabel("这里是窗口内容区域")
        content_label.setAlignment(Qt.AlignCenter)
        content_label.setStyleSheet("font-size: 24px; padding: 20px;")
        main_layout.addWidget(content_label, 1)
        
        # 添加大小调整手柄
        self.size_grip = QSizeGrip(self)
        self.size_grip.setFixedSize(16, 16)
        self.size_grip.setStyleSheet("background-color: #555;")
        
        # 边缘拖动调整大小
        self.setMouseTracking(True)
        self._padding = 5
        self._resize_direction = None
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.size_grip.move(self.width() - 16, self.height() - 16)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._resize_direction:
            self._resize_start_pos = event.globalPosition().toPoint()
            self._resize_start_geometry = self.geometry()
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if hasattr(self, '_resize_start_pos'):
            # 处理调整大小
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            new_geometry = self._resize_start_geometry
            
            if 'left' in self._resize_direction:
                new_geometry.setLeft(new_geometry.left() + delta.x())
            if 'right' in self._resize_direction:
                new_geometry.setRight(new_geometry.right() + delta.x())
            if 'top' in self._resize_direction:
                new_geometry.setTop(new_geometry.top() + delta.y())
            if 'bottom' in self._resize_direction:
                new_geometry.setBottom(new_geometry.bottom() + delta.y())
            
            if new_geometry.width() >= self.minimumWidth() and new_geometry.height() >= self.minimumHeight():
                self.setGeometry(new_geometry)
        else:
            # 检测鼠标是否在边缘区域
            pos = event.position().toPoint()
            rect = self.rect()
            self._resize_direction = None
            
            if pos.x() <= self._padding:
                if pos.y() <= self._padding:
                    self.setCursor(Qt.SizeFDiagCursor)
                    self._resize_direction = ['left', 'top']
                elif pos.y() >= rect.height() - self._padding:
                    self.setCursor(Qt.SizeBDiagCursor)
                    self._resize_direction = ['left', 'bottom']
                else:
                    self.setCursor(Qt.SizeHorCursor)
                    self._resize_direction = ['left']
            elif pos.x() >= rect.width() - self._padding:
                if pos.y() <= self._padding:
                    self.setCursor(Qt.SizeBDiagCursor)
                    self._resize_direction = ['right', 'top']
                elif pos.y() >= rect.height() - self._padding:
                    self.setCursor(Qt.SizeFDiagCursor)
                    self._resize_direction = ['right', 'bottom']
                else:
                    self.setCursor(Qt.SizeHorCursor)
                    self._resize_direction = ['right']
            elif pos.y() <= self._padding:
                self.setCursor(Qt.SizeVerCursor)
                self._resize_direction = ['top']
            elif pos.y() >= rect.height() - self._padding:
                self.setCursor(Qt.SizeVerCursor)
                self._resize_direction = ['bottom']
            else:
                self.setCursor(Qt.ArrowCursor)
            
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if hasattr(self, '_resize_start_pos'):
            del self._resize_start_pos
            del self._resize_start_geometry
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())