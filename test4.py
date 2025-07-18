from PySide6.QtWidgets import (QApplication, QMainWindow, QFrame, 
                              QPushButton, QVBoxLayout, QWidget, 
                              QButtonGroup, QHBoxLayout,QLabel)
from PySide6.QtCore import (QPropertyAnimation, QEasingCurve, 
                           Qt, QSize, Property)
from PySide6.QtGui import QIcon
import sys
import os
os.chdir(os.path.dirname(__file__))

class AnimatedButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(parent)
        self._icon_size = QSize(20, 20)
        self._text = text
        self._icon = icon
        
        self.setup_ui()
        
    def setup_ui(self):
        self.setCheckable(True)
        self.setIcon(self._icon)
        self.setText(self._text)
        self.setToolTip(self._text)
        self.setIconSize(self._icon_size)
        
        # # 使用水平布局来保持图标位置稳定
        # self.layout = QHBoxLayout(self)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # # self.layout.setSpacing(8)
        
        # self.icon_label = QLabel()
        # self.icon_label.setPixmap(self._icon.pixmap(self._icon_size))
        # self.layout.addWidget(self.icon_label)
        
        # self.text_label = QLabel(self._text)
        # self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # self.layout.addWidget(self.text_label)
        # self.text_label.hide()  # 初始隐藏文字
        
    def setTextVisible(self, visible):
        self.text_label.setVisible(visible)
        self.setFixedWidth(200 if visible else 60)
        
    textVisible = Property(bool, lambda self: self.text_label.isVisible(), setTextVisible)

class AnimatedSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
        # 动画参数
        self.collapsed_width = 40
        self.expanded_width = 200
        self.animation_duration = 300
        
        # 初始状态
        self.setFixedWidth(self.collapsed_width)
        self.is_expanded = False
        
        # 设置样式
        self.setStyleSheet("""
            /* 侧边栏基础样式 */
            AnimatedSidebar {
                background-color: #2c3e50;
                border-radius: 12px;
                border: none;
            }
            
            /* 按钮通用样式 */
            QPushButton {
                background-color: transparent;
                color: #ecf0f1;
                text-align: left;
                padding: 0;
                border-radius: 6px;
                border: none;
                margin: 2px 4px;
                font-size: 14px;
                min-width: 40px;
            }
            
            /* 按钮悬停状态 */
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            /* 按钮按下状态 */
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
            
            /* 按钮选中状态 */
            QPushButton:checked {
                background-color: #3498db;
                color: white;
            }
            
            /* 切换按钮特殊样式 */
            #toggleButton {
                background-color: #34495e;
                border-radius: 20px;
                padding: 8px;
            }
            
            #toggleButton:hover {
                background-color: #3d566e;
            }
            
            /* 标签样式 */
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
            }
            
            QPushButton:checked QLabel {
                color: white;
            }
        """)
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 12, 0, 12)
        self.layout.setSpacing(1)
        
        # 创建按钮组实现单选效果
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        # 添加几个示例按钮
        self.buttons = [
            self.add_button("文件", QIcon("./OneDarkTheme/gui/images/svg_icons/icon_file.svg"), True),
            self.add_button("编辑", QIcon("./OneDarkTheme/gui/images/svg_icons/icon_busy.svg")),
            self.add_button("视图", QIcon("./OneDarkTheme/gui/images/svg_icons/icon_folder.svg")),
            self.add_button("帮助", QIcon("./OneDarkTheme/gui/images/svg_icons/icon_home.svg"))
        ]
        
        # 添加展开/收起按钮
        self.toggle_button = QPushButton()
        self.toggle_button.setObjectName("toggleButton")
        self.toggle_button.setIcon(QIcon.fromTheme("arrow-right"))
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.clicked.connect(self.toggle_animation)
        self.layout.addStretch()
        self.layout.addWidget(self.toggle_button, 0, Qt.AlignLeft)
        
    def add_button(self, text, icon, checked=False):
        """创建自定义动画按钮"""
        btn = AnimatedButton(text, icon)
        btn.setFixedHeight(50)
        # btn.setFixedWidth(self.width())
        btn.setChecked(checked)
        
        # 连接按钮点击信号
        btn.clicked.connect(lambda: self.on_button_clicked(btn))
        
        self.layout.addWidget(btn)
        self.button_group.addButton(btn)
        return btn
        
    def on_button_clicked(self, button):
        """处理按钮点击事件"""
        # 确保只有一个按钮能被选中
        for btn in self.buttons:
            btn.setChecked(btn == button)
        
    def toggle_animation(self):
        """切换展开/收起状态"""
        self.is_expanded = not self.is_expanded
        
        # 当点击展开/收起按钮时，取消所有按钮的选中状态
        self.button_group.setExclusive(False)
        for btn in self.buttons:
            btn.setChecked(False)
        self.button_group.setExclusive(True)
        
        # 创建宽度动画
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(self.animation_duration)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        if self.is_expanded:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self.expanded_width)
            self.toggle_button.setIcon(QIcon.fromTheme("arrow-left"))
        else:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self.collapsed_width)
            self.toggle_button.setIcon(QIcon.fromTheme("arrow-right"))
            
        # 动画过程中动态调整按钮文本显示
        self.animation.valueChanged.connect(self.update_button_text_visibility)
        self.animation.start()
        
    def update_button_text_visibility(self, width):
        """根据当前宽度更新按钮文本的显示状态"""
        # 计算动画进度 (0.0-1.0)
        progress = (width - self.collapsed_width) / (self.expanded_width - self.collapsed_width)
        
        for btn in self.buttons:
            # 当进度超过50%时显示文字，否则隐藏
            btn.setTextVisible(progress > 0.5)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("优化动画侧边栏")
        self.resize(900, 600)
        
        # 主布局
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(5, 0, 0, 0)
        # layout.setSpacing(0)
        
        # 添加动画侧边栏
        self.sidebar = AnimatedSidebar(self)
        layout.addWidget(self.sidebar)
        
        # 添加主内容区域
        content = QFrame()
        content.setStyleSheet("background-color: #f5f6fa;")
        layout.addWidget(content, 1)
        
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()