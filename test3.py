from PySide6.QtWidgets import QTextEdit, QApplication
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor

app = QApplication([])

text_edit = QTextEdit()
text_edit.setPlainText("NAME: John Doe\nID: 12345\nDepartment: Engineering\nManager NAME: Jane Smith")

# 设置高亮格式
highlight_format = QTextCharFormat()
highlight_format.setBackground(QColor('yellow'))

document = text_edit.document()
cursor = QTextCursor(document)

# 查找并高亮所有 'NAME'
while True:
    cursor = document.find('NAME', cursor)
    if cursor.isNull():
        break
    # 高亮找到的文本
    cursor.mergeCharFormat(highlight_format)

text_edit.show()
app.exec()