import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import Qt

class FormLayoutDemo(QWidget):
    def __init__(self, parent=None):
        super(FormLayoutDemo, self).__init__(parent)
        self.setWindowTitle("QFormLayout布局管理器")
        self.resize(400, 100)

        formLayout = QFormLayout()

        nameLineEdit = QLineEdit()
        emailLineEdit = QLineEdit()
        ageSpinBox = QSpinBox()
        formLayout.addRow("&Name:",nameLineEdit)
        formLayout.addRow("&Email:",emailLineEdit)
        formLayout.addRow("&Age:",ageSpinBox)

        # 模拟macStyle表单布局外观，但使用左对齐的标签
        """
        setRowWrapPolicy 控制表单行的换行策略，决定当空间不足时如何排列标签和字段
        QFormLayout.DontWrapRows：不换行，标签和字段始终在同一行（默认值）
        QFormLayout.WrapLongRows：如果空间不足，将长行换行（标签在上，字段在下）
        QFormLayout.WrapAllRows：所有行都换行显示（标签在上，字段在下）

        setFieldGrowthPolicy 控制表单字段的增长策略，决定字段如何利用额外空间
        QFormLayout.FieldsStayAtSizeHint：字段保持其 sizeHint 大小（默认值）
        QFormLayout.ExpandingFieldsGrow：有 expanding 策略的字段会扩展
        QFormLayout.AllNonFixedFieldsGrow：所有非固定大小的字段都会扩展

        setFormAlignment设置整个表单在布局中的对齐方式。
        水平方向：Qt.AlignLeft, Qt.AlignHCenter, Qt.AlignRight
        垂直方向：Qt.AlignTop, Qt.AlignVCenter, Qt.AlignBottom

        setLabelAlignment   设置表单中所有标签的对齐方式。
        Qt.AlignLeft：左对齐（默认）
        Qt.AlignRight：右对齐
        Qt.AlignHCenter：水平居中
        Qt.AlignJustify：两端对齐

        """
        formLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        formLayout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        formLayout.setLabelAlignment(Qt.AlignLeft)

        formLayout.addItem(QSpacerItem(30,30))
        formLayout.addRow(QPushButton('确认'),QPushButton('取消'))

        self.setLayout(formLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FormLayoutDemo()
    form.show()
    sys.exit(app.exec())
