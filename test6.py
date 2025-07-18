from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

app = QApplication([])

# 创建主窗口
window = QWidget()
layout = QVBoxLayout()

# 创建带图标的按钮
button1 = QPushButton()
button1.setText("保存")
button1.setIcon(QIcon("./OneDarkTheme/gui/images/svg_icons/icon_save.svg"))
button1.setIconSize(QSize(24, 24))

# 创建时直接设置
button2 = QPushButton(QIcon("./OneDarkTheme/gui/images/svg_icons/icon_folder_open.svg"), "打开", window)

# 图标在右侧的按钮
button3 = QPushButton("下载", window)
button3.setIcon(QIcon("./OneDarkTheme/gui/images/svg_icons/icon_add_user.svg"))
button3.setStyleSheet("""
    QPushButton {
        padding-right: 15px;
    }
    QPushButton::icon {
        padding-left: 1px;
    }
""")

# 添加到布局
layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(button3)

window.setLayout(layout)
window.show()
app.exec()