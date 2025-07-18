from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
import sys
import os
os.chdir(os.path.dirname(__file__))

"""
QDataWidgetMapper 主要功能：

    将模型（如 QAbstractItemModel）中的数据自动映射到界面控件
    支持双向数据绑定（模型 ↔ 控件）
    简化表单类界面的开发
    支持记录导航（前进/后退）
"""

class DataWidgetMapperDemo(QMainWindow):
    def __init__(self, parent=None):
        super(DataWidgetMapperDemo, self).__init__(parent)
        self.setWindowTitle("QDataWidgetMapper案例")
        self.resize(550, 500)
        self.initModel()
        self.createWindow()
    
    def initModel(self):
        self.model = QSqlRelationalTableModel()
        self.model.setTable("student2")
        self.sexIndex = self.model.fieldIndex("sex")
        self.subjectIndex = self.model.fieldIndex("subject")

        # QSqlRelation(关联表名,关联表明主键,显示字段)
        self.model.setRelation(self.sexIndex, QSqlRelation("sex","id","name"))
        self.model.setRelation(self.subjectIndex,QSqlRelation("subject","id","name"))
        self.model.setHeaderData(0, Qt.Horizontal, "编号")
        self.model.setHeaderData(1, Qt.Horizontal, "姓名")
        self.model.setHeaderData(2, Qt.Horizontal, "性别")
        self.model.setHeaderData(3, Qt.Horizontal, "科目")
        self.model.setHeaderData(4, Qt.Horizontal, "成绩")
        # self.model.select() 是 QSqlTableModel 和 QSqlRelationalTableModel 等 SQL 模型类中的一个关键方法，用于从数据库加载数据到模型中
        self.model.select()

    def createWindow(self):
        self.tableView = QTableView()
        # 设置 模型 以及委托
        self.tableView.setModel(self.model)
        self.delegate = QSqlRelationalDelegate(self.tableView)
        self.tableView.setItemDelegate(self.delegate)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.groupBox = QGroupBox()
        self.groupBox.setTitle('详细信息：')
        formLayout = QFormLayout(self.groupBox)

        self.idSpinBox = QSpinBox()
        self.idSpinBox.setMinimum(0)
        formLayout.addRow('编号',self.idSpinBox)

        self.nameEdite = QLineEdit()
        formLayout.addRow('姓名',self.nameEdite)
        self.sexComboBox = QComboBox()

        # 获取性别字段的关系模型
        relationModelSex = self.model.relationModel(self.sexIndex)
        self.sexComboBox.setModel(relationModelSex)
        # 设置组合框显示的列（显示name字段而不是id）
        self.sexComboBox.setModelColumn(relationModelSex.fieldIndex("name"))
        formLayout.addRow('性别',self.sexComboBox)

        self.subjectComboBox = QComboBox()
        relationModelSubject = self.model.relationModel(self.subjectIndex)
        self.subjectComboBox.setModel(relationModelSubject)
        self.subjectComboBox.setModelColumn(relationModelSubject.fieldIndex("name"))
        formLayout.addRow('科目',self.subjectComboBox)
        self.scoreSpinBox = QSpinBox()
        self.scoreSpinBox.setMinimum(0)
        formLayout.addRow('成绩',self.scoreSpinBox)

        # 设置映射  注意： 之前给特定控件设置了关系模型， 会对id 进行转换 映射到 name字段属性
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(self.delegate)
        self.mapper.addMapping(self.idSpinBox, self.model.fieldIndex('id'))
        self.mapper.addMapping(self.nameEdite, self.model.fieldIndex('name'))
        self.mapper.addMapping(self.sexComboBox, self.sexIndex)
        self.mapper.addMapping(self.subjectComboBox, self.subjectIndex)
        self.mapper.addMapping(self.scoreSpinBox, self.model.fieldIndex('score'))
        self.mapper.toFirst()

        selectModel = self.tableView.selectionModel()
        selectModel.currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        layout = QHBoxLayout()
        layout.addWidget(self.tableView)
        layout.addWidget(self.groupBox)

        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(layout)

if __name__=="__main__":
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("../db/database.db")
    if db.open() is not True:
        QMessageBox.critical(QWidget(), "警告", "数据连接失败，程序即将退出")
        exit()
    demo = DataWidgetMapperDemo()
    demo.show()
    sys.exit(app.exec())
