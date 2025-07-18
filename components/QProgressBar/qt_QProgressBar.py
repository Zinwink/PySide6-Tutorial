import sys
import time
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                             QProgressBar, QPushButton, 
                             QVBoxLayout, QWidget)

# Worker 类 - 执行耗时任务
class Worker(QObject):
    progress_updated = Signal(int)  # 进度更新信号 (0-100)
    finished = Signal()             # 任务完成信号

    @Slot()
    def do_work(self):
        """模拟耗时任务"""
        for i in range(1, 101):
            time.sleep(0.1)  # 模拟耗时操作
            self.progress_updated.emit(i)  # 发送进度信号
        self.finished.emit()  # 发送完成信号

# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThread + moveToThread 示例")
        self.setup_ui()

    def setup_ui(self):
        # 创建控件
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        
        self.button = QPushButton("开始任务")
        self.button.clicked.connect(self.start_task)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_task(self):
        """启动线程和任务"""
        self.button.setEnabled(False)  # 禁用按钮，防止重复点击
        
        # 创建线程和worker
        self.thread = QThread()
        self.worker = Worker()

        # 将worker移动到新线程
        self.worker.moveToThread(self.thread)

        # 连接信号和槽
        self.thread.started.connect(self.worker.do_work)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # 启动线程
        self.thread.start()

    def update_progress(self, value):
        """更新进度条 (在主线程执行)"""
        self.progress_bar.setValue(value)

    def task_finished(self):
        """任务完成后的清理工作"""
        self.button.setEnabled(True)  # 重新启用按钮
        print("任务完成!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())