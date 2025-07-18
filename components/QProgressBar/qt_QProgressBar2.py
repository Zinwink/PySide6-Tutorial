import sys
import time
from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                             QProgressBar, QPushButton, 
                             QVBoxLayout, QWidget, QLabel)

class Worker(QObject):
    progress_updated = Signal(int)
    finished = Signal()
    
    @Slot()
    def do_work(self):
        """模拟耗时任务"""
        for i in range(1, 101):
            time.sleep(0.05)  # 模拟耗时操作
            self.progress_updated.emit(i)
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("美化进度条示例")
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        # 创建控件
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        
        # 修正这里：使用 Qt.AlignmentFlag 枚举
        self.status_label = QLabel("准备就绪")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 正确的居中方式
        
        self.button = QPushButton("开始处理")
        self.button.setFixedHeight(40)
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.button.clicked.connect(self.start_task)
        
    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QProgressBar {
                height: 8px;
                border-radius: 4px;
                background-color: #e0e0e0;
                text-align: center;
                padding: 2px;  /* 关键：为chunk留出圆角空间 */
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 0px;
                width: 8px;
                margin: 1px;  /* 微调位置 */
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
        """)
        
    def start_task(self):
        self.button.setEnabled(False)
        self.status_label.setText("处理中...")
        self.progress_bar.setValue(0)
        
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.do_work)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()
        
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
        if value < 30:
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #FF5722;
                }
            """)
        elif value < 70:
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #FFC107;
                }
            """)
        else:
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #4CAF50;
                }
            """)
        
    def task_finished(self):
        self.button.setEnabled(True)
        self.status_label.setText("处理完成!")
        self.progress_bar.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec())