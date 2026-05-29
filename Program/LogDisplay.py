import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QTextEdit, QPushButton, QHBoxLayout, QComboBox
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QTextCharFormat, QColor

class LogDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日志显示栏")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        layout.addWidget(self.log_text)
        
        # 创建控制按钮区域
        control_layout = QHBoxLayout()
        
        # 日志级别选择
        self.log_level = QComboBox()
        self.log_level.addItems(["INFO", "WARNING", "ERROR", "DEBUG"])
        control_layout.addWidget(self.log_level)
        
        # 添加测试日志按钮
        test_button = QPushButton("添加测试日志")
        test_button.clicked.connect(self.add_test_log)
        control_layout.addWidget(test_button)
        
        # 清空日志按钮
        clear_button = QPushButton("清空日志")
        clear_button.clicked.connect(self.clear_logs)
        control_layout.addWidget(clear_button)
        
        layout.addLayout(control_layout)
        
        # 初始化日志级别颜色
        self.init_log_level_colors()
        
    def init_log_level_colors(self):
        """初始化不同日志级别的颜色"""
        self.log_colors = {
            "INFO": QColor(0, 0, 0),       # 黑色
            "WARNING": QColor(255, 165, 0), # 橙色
            "ERROR": QColor(255, 0, 0),     # 红色
            "DEBUG": QColor(0, 0, 255)      # 蓝色
        }
    
    def add_log(self, message, level="INFO"):
        """添加日志到显示区域"""
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # 获取对应级别的颜色
        color = self.log_colors.get(level, QColor(0, 0, 0))
        
        # 创建文本格式并设置颜色
        format = QTextCharFormat()
        format.setForeground(color)
        
        # 将文本添加到显示区域
        self.log_text.setCurrentCharFormat(format)
        self.log_text.append(log_entry)
        
        # 自动滚动到底部
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def add_test_log(self):
        """添加测试日志"""
        level = self.log_level.currentText()
        self.add_log(f"这是一条{level}级别的测试日志", level)
    
    def clear_logs(self):
        """清空所有日志"""
        self.log_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogDisplay()
    window.show()
    sys.exit(app.exec())