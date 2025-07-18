
"""
QMimeData 用于描述可以存储在剪贴板中并且可以通过拖放机制传输的信息。
QMimeData 不是一个 QWidget 控件
QMimeData 对象通常由 QDrag 对象或 QClipboard 对象创建,并作为数据传输通道提
供给 QDrag 对象或 QClipboard 对象。
"""

import sys
from PySide6.QtWidgets import QPushButton, QWidget, QLineEdit, QApplication, QLabel,QVBoxLayout
from PySide6.QtCore import QByteArray, QMimeData

# 该按钮可以接受拖拽的文本文件进入
class ButtonQMime(QPushButton):
    def __init__(self, title, parent):
        super(ButtonQMime, self).__init__(title, parent)
        # 启用控件的拖放接收功能，这是实现拖放功能的关键第一步
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        # 鼠标拖拽进入控件， 按照mimeData指定该控件是否拖拽
        '''
        检查拖动的数据是否包含纯文本格式 (text/plain)
        如果是，调用 e.accept() 表示接受此拖动操作
        否则，调用 e.ignore() 表示忽略此拖动操作
        '''
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()
        
    def dropEvent(self, event):
        # 拖拽后鼠标释放事件
        self.setText(event.mimeData().text())

# 该按钮接受拖拽进入的内容，并按照自定义MimeData修改按钮文本
class ButtonMyQMime(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.mime = QMimeData()
        qb = QByteArray(bytes('abcd1234',encoding='utf8'))
        self.mime.setData('my_minetype',qb)
    
    def dragEnterEvent(self, event):
        if self.mime.hasFormat('my_mimetype'):
            event.accept() # 接受 向父组件传播
        else:
            event.ignore() # 忽略
    
    def dropEvent(self, event):
        self.setText('自定义format结果为:'+self.mime.data('my_mimetype').data().decode('utf8'))

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel('拖拽到窗口显示拖拽format信息',self)
        layout.addWidget(self.label)

        edit = QLineEdit("我可以被拖拽，你可以用我拖拽，也可以拖拽文件到窗口", self)
        edit.setMinimumWidth(350)
        edit.setDragEnabled(True)
        layout.addWidget(edit)

        button = ButtonQMime('拖拽到此按钮，修改按钮text',self)
        layout.addWidget(button)

        button2 = ButtonMyQMime("拖拽到此按钮，显示自定义format", self)
        layout.addWidget(button2)

        self.setWindowTitle("QMimeData案例：通过拖拽传输数据")
        self.setGeometry(300, 300, 300, 150)
        self.show()
    
    # 接受拖拽文件， 识别路径和内容 并显示
    def dragEnterEvent(self, event):
        _str = ''
        mime = event.mimeData()

        # 识别拖拽文件
        if mime.hasUrls():
            path_list = mime.urls()
            _str = '\n'.join(a.path() for a in path_list)
            _str = '拖拽的文件路径为:\n' + _str + '\n\n'
        
        # 识别拖拽的文字
        if mime.hasText():
            _str = _str +"拖拽的文字内容为:\n"+mime.text()+"\n\n"
        
        # 显示一些格式信息
        format_list = mime.formats()
        self.label.setText(_str+"拖拽的formats为:\n"+'\n'.join(format_list))

if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())