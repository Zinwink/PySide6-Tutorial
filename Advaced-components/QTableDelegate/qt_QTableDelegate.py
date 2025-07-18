from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import re
import sys
import datetime
import random

import os
os.chdir(os.path.dirname(__file__))

SUBJECT, NAME, SCORE, DESCRIPTION = range(4)

class Student(object):

    def __init__(self, subject, name, score=0, description=""):
        self.subject = subject
        self.name = name
        self.score = score
        self.description = description
    
    def __hash__(self):
        return super(Student, self).__hash__()

    def __lt__(self, other):
        if self.name < other.name:
            return True
        if self.subject < other.subject:
            return True
        return id(self) < id(other)
    
    def __eq__(self, other):
        if self.name == other.name:
            return True
        if self.subject == other.subject:
            return True
        return id(self) == id(other)


class StudentTableModel(QAbstractTableModel):
    def __init__(self, filename=""):
        super(StudentTableModel, self).__init__()
        self.students = []
    
    def initData(self):
        for subject in ['语文', '数学', '外语', '综合']:
            for name in ['张三', '李四', '王五', '赵六']:
                score = random.random() * 40 + 60
                if score>=80:
                    _str = f'{name}的{subject}成绩是：优秀'
                else:
                    _str = f'{name}的{subject}成绩是：良好'
                student = Student(subject, name, score, _str)
                self.students.append(student)
        self.sortBySubject()
    
    def sortByName(self):

        self.students = sorted(self.students,key=lambda x:(x.name,x.subject))
        self.endResetModel()
    
    def sortBySubject(self):
        self.students = sorted(self.students, key=lambda x: (x.subject, x.name))
        self.endResetModel()
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

    def data(self, index, role=Qt.DisplayRole):
        # 返回指定索引数据
        if not index.isValid() or not (0 <= index.row() < len(self.students)):
            return None
        student = self.students[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            # 显示数据
            if column == SUBJECT:
                return student.subject
            elif column == NAME:
                return student.name
            elif column == DESCRIPTION:
                return student.description
            elif column == SCORE:
                return "{:.2f}".format(student.score)
        elif role == Qt.TextAlignmentRole:
            # 文本对齐 返回对齐方式
            if column == SCORE:
                return int(Qt.AlignRight | Qt.AlignVCenter)
            return int(Qt.AlignLeft | Qt.AlignVCenter)
        elif role == Qt.ForegroundRole and column == SCORE:
            # 前景设置 应用与SCORE列
            if student.score < 80:
                return QColor(Qt.black)
            elif student.score < 90:
                return QColor(Qt.darkGreen)
            elif student.score < 100:
                return QColor(Qt.red)
        elif role == Qt.BackgroundRole:
            # 背景设置
            if student.subject in ("数学", "语文"):
                return QColor(250, 230, 250)
            elif student.subject in ("外语",):
                return QColor(250, 250, 230)
            elif student.subject in ("综合"):
                return QColor(230, 250, 250)
            else:
                return QColor(210, 230, 230)
        return None

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft | Qt.AlignVCenter)
            return int(Qt.AlignRight | Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == SUBJECT:
                return "科目"
            elif section == NAME:
                return "姓名"
            elif section == SCORE:
                return "分数"
            elif section == DESCRIPTION:
                return "说明"
        return int(section + 1)
    
    def rowCount(self, index=QModelIndex()):
        return len(self.students)
    
    def columnCount(self, index=QModelIndex()):
        return 4
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.students) and role==Qt.EditRole:
            student = self.students[index.row()]
            column = index.column()
            if column == SUBJECT:
                student.subject = value
            elif column == NAME:
                student.name = value
            elif column == DESCRIPTION:
                student.description = value
            elif column == SCORE:
                try:
                    student.score = int(value)
                except:
                    print('输入错误，请输入数字')
            
            # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            self.dataChanged.emit(index, index) # 发射信号， 通知界面数据改变
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.students.insert(position + row, Student("test", "test", 0,''))
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.students = (self.students[:position] + self.students[position + rows:])
        self.endRemoveRows()
        return True

class StudentTableDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(StudentTableDelegate, self).__init__(parent)
    
    def paint(self, painter, option, index):
        if index.column() == DESCRIPTION:
            text = index.model().data(index)
            if text[-2:] == "优秀":
                text = f'{text[:-2]}<font color=red><b>优秀</b></font>'
                index.model().setData(index, value=text)
            elif text[-2:] == '良好':
                text = f'{text[:-2]}<font color=green><b>良好</b></font>'
                index.model().setData(index, value=text)
            palette = QApplication.palette()
            document = QTextDocument()
            document.setDefaultFont(option.font)
            if option.state & QStyle.State_Selected:
                document.setHtml("<font color={}>{}</font>".format(
                    palette.highlightedText().color().name(), text))
                # palette.highlightedText().color().name() 获取的是当前系统或应用程序样式表中定义的 ​​高亮文本颜色​​。这个颜色通常与选中项的背景色（palette.highlight().color()）形成对比，确保选中文本的可读性 
                # 通常为白色
            else:
                document.setHtml(text)
            color = (palette.highlight().color()
                     if option.state & QStyle.State_Selected
                     else QColor(index.model().data(index, Qt.BackgroundRole)))
            painter.save()
            painter.fillRect(option.rect, color)
            painter.translate(option.rect.x(), option.rect.y())
            document.drawContents(painter)
            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)
    
    def sizeHint(self, option, index):
        #  获取字体度量信息
        fm = option.fontMetrics
        if index.column() == SCORE:
            return QSize(fm.averageCharWidth(), fm.height())
        if index.column() == DESCRIPTION:
            text = index.model().data(index)
            document = QTextDocument()
            document.setDefaultFont(option.font)
            document.setHtml(text)
            return QSize(document.idealWidth() + 5, fm.height())
        return QStyledItemDelegate.sizeHint(self, option, index)
    
    def createEditor(self, parent, option, index):
        """
        用于为不同类型的表格列创建不同的编辑器控件
        createEditor 方法在用户开始编辑表格单元格时被调用，用于：
            根据列类型创建适当的编辑器控件
            对编辑器进行初始配置
            返回配置好的编辑器控件
        """
        if index.column() == SCORE:
            spinbox = QSpinBox(parent)
            spinbox.setRange(0, 100)
            spinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return spinbox
        elif index.column() in (NAME, SUBJECT):
            editor = QLineEdit(parent)
            # self.connect(editor, SIGNAL("returnPressed()"), self.commitAndCloseEditor)
            return editor
        elif index.column() == DESCRIPTION:
            editor = QTextEdit()
            # self.connect(editor, SIGNAL("returnPressed()"), self.commitAndCloseEditor)
            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)
    
    def commitAndCloseEditor(self):
        """
        用于提交编辑器数据并关闭编辑器
        """
        editor = self.sender() # 获取信号发送者
        if isinstance(editor, (QTextEdit, QLineEdit)):
            # 检查编辑器类型
            self.commitData.emit(editor)
            self.closeEditor.emit(editor)

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        if index.column() == SCORE:
            try:
                value = int(float(text) + 0.5)
            except:
                value = 0
            editor.setValue(value)
        elif index.column() in (NAME, SUBJECT):
            editor.setText(text)
        elif index.column() == DESCRIPTION:
            editor.setHtml(text)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)
    
    def setModelData(self, editor, model, index):
        if index.column() == SCORE:
            model.setData(index, editor.value())
        elif index.column() in (NAME, SUBJECT):
            model.setData(index, editor.text())
        elif index.column() == DESCRIPTION:
            model.setData(index, editor.toHtml())
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

class DateColumnDelegate(QStyledItemDelegate):

    def __init__(self, minimum=QDate(),
                 maximum=QDate.currentDate(),
                 format="yyyy-MM-dd", parent=None):
        super(DateColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.format = format

    def createEditor(self, parent, option, index):
        dateedit = QDateEdit(parent)
        dateedit.setDateRange(self.minimum, self.maximum)
        dateedit.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        dateedit.setDisplayFormat(self.format)
        dateedit.setCalendarPopup(True)
        return dateedit

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        try:
            date = datetime.datetime.strptime(value, '%Y-%m-%d').date()
            editor.setDate(QDate(date.year, date.month, date.day))
        except:
            print(value, index)
            editor.setDate(QDate())

    def setModelData(self, editor, model, index):
        model.setData(index, editor.date().toString('yyyy-MM-dd'))

class IntegerColumnDelegate(QStyledItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum

    def createEditor(self, parent, option, index):
        spinbox = QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return spinbox

    def setEditorData(self, editor, index):
        value = int(index.model().data(index, Qt.DisplayRole))
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, editor.value())

class QTableViewDemo(QMainWindow):

    def __init__(self, parent=None):
        super(QTableViewDemo, self).__init__(parent)
        self.setWindowTitle("QTableDelegate案例")
        self.resize(550, 600)

        # 方式1：基于自定义模型的自定义委托
        self.tableView = QTableView()
        self.model = StudentTableModel()
        self.delegate = StudentTableDelegate()
        self.model.initData()

        self.tableView.setModel(self.model)
        self.selectModel = QItemSelectionModel()
        self.tableView.setSelectionModel(self.selectModel)
        self.tableView.setItemDelegate(self.delegate)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        # 方式2：通用模型的通用委托
        self.tableView2 = QTableView()
        self.model2 = QStandardItemModel(5, 4)
        self.init_model2()
        self.tableView2.setModel(self.model2)
        self.delegate2 = IntegerColumnDelegate()
        self.tableView2.setItemDelegateForColumn(2, self.delegate2)
        self.tableView2.setItemDelegateForColumn(3, DateColumnDelegate())

        self.buttonAddRow = QPushButton('增加行')
        self.buttonInsertRow = QPushButton('插入行')
        self.buttonDeleteRow = QPushButton('删除行')
        self.buttonAddRow.clicked.connect(self.onAdd)
        self.buttonInsertRow.clicked.connect(self.onInsert)
        self.buttonDeleteRow.clicked.connect(self.onDelete)

        self.model.setData(self.model.index(3, 1), 'Python', role=Qt.EditRole)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tableView)
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.buttonAddRow)
        layoutH.addWidget(self.buttonInsertRow)
        layoutH.addWidget(self.buttonDeleteRow)
        layout.addLayout(layoutH)
        layout.addWidget(self.tableView2)

        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(layout)

    def init_model2(self):
        for row in range(self.model2.rowCount()):
            for column in range(self.model2.columnCount()):
                if column == 2:
                    value = column + row
                elif column == 3:
                    date = datetime.datetime.strptime('2022-01-01', '%Y-%m-%d') + datetime.timedelta(days=column * row)
                    value = datetime.datetime.strftime(date, '%Y-%m-%d')
                else:
                    value = "row %s, col %s" % (row, column)
                item = QStandardItem(str(value))
                self.model2.setItem(row, column, item)

    def onAdd(self):
        rowCount = self.model.rowCount()
        self.model.insertRow(rowCount)

    def onInsert(self):
        index = self.tableView.currentIndex()
        row = index.row()
        self.model.insertRow(row)

    def onDelete(self):
        index = self.tableView.currentIndex()
        row = index.row()
        self.model.removeRow(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = QTableViewDemo()
    demo.show()
    sys.exit(app.exec())