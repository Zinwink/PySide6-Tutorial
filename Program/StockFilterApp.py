import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow,QVBoxLayout, QHBoxLayout,QPushButton,QLineEdit,QWidget,QTableWidgetItem, QLabel, QHeaderView, QMessageBox,QTableWidget
)
from PySide6.QtCore import Qt
import pandas as pd
import pywencai
import json

class StockFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("股票筛选系统")
        self.setGeometry(100,100,1200,800)

        # 创建主窗口
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color:white")
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)

        # 创建顶部搜索区域
        search_layout = QHBoxLayout()

        # 添加搜索标签
        search_label = QLabel("输入筛选条件:")
        search_layout.addWidget(search_label)

        # 添加搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("例如: 涨停")
        search_layout.addWidget(self.search_input)

        # 添加搜索按钮
        search_button = QPushButton("搜索")
        search_button.clicked.connect(self.search_stocks)
        search_layout.addWidget(search_button)

        main_layout.addLayout(search_layout)

        # 添加状态标签
        self.status_label = QLabel("准备就绪")
        main_layout.addWidget(self.status_label)

        # 创建表格用于显示结果
        self.result_tabel = QTableWidget()
        # 设置表格为只读
        self.result_tabel.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.result_tabel)

    def search_stocks(self):
        query = self.search_input.text()
        if not query:
            QMessageBox.warning(self,"警告","请输入筛选条件")
            return
        self.status_label.setText(f"正在查询:{query}...")
        try:
            # 使用pywencai获取数据
            df = pywencai.get(query=query,loop=True)
            self.display_results(df)
            self.status_label.setText(f"查询完成:找到{len(df)}条结果")
        except Exception as e:
            self.status_label.setText(f"查询出错:{str(e)}")
            QMessageBox.critical(self,"错误",f"查询失败:{str(e)}")
    
    def display_results(self, df):
        # 清空表格
        self.result_tabel.clear()
        if df.empty:
            self.result_tabel.setRowCount(0)
            self.result_tabel.setColumnCount(0)
            self.status_label.setText("没有找到匹配的结果")
            return
        # 处理DataFrame 去除JSON格式的列
        filtered_columns = []
        for col in df.columns:
            # 检查列中的值是否为JSON格式
            is_json_column = False
            for value in df[col].dropna().head(10).astype(str):
                # 检查是否为JSON对象或JSON数组
                if (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']')):
                    try:
                        json.loads(value)
                        is_json_column = True
                        break
                    except:
                        pass
            if not is_json_column:
                filtered_columns.append(col)
        # 如果所有列都被过滤调， 保留原始DataFrame
        if not filtered_columns:
            filtered_df = df
        else:
            filtered_df = df[filtered_columns]
        
        # 设置表格列数和列标题
        self.result_tabel.setColumnCount(len(filtered_df.columns))
        self.result_tabel.setHorizontalHeaderLabels(filtered_df.columns)
        # 设置表格行数
        self.result_tabel.setRowCount(len(filtered_df))

        # 填充表格数据
        for row in range(len(filtered_df)):
            for col in range(len(filtered_df.columns)):
                value = str(filtered_df.iloc[row, col])

                # 检查单元格值是否为JSON格式 如果是则提取有用信息
                if (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']')):
                    try:
                        json_data = json.loads(value)
                        if isinstance(json_data,dict):
                            # 提取第一个非空值
                            for json_value in json_data.values():
                                if json_value:
                                    value = str(json_value)
                                    break
                        elif isinstance(json_data,list) and json_data:
                            # 如果是数组 显示数组长度或第一个元素的摘要
                            value = f"数组[{len(json_data)}项]"
                    except:
                        pass
                item = QTableWidgetItem(value)
                self.result_tabel.setItem(row, col, item)
        # 调整列宽以适应内容
        self.result_tabel.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # 设置交替行颜色
        self.result_tabel.setAlternatingRowColors(True)
        # 更新状态标签
        self.status_label.setText(f"查询完成:找到{len(filtered_df)}条结果,显示{len(filtered_df.columns)}列")
            
    


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = StockFilterApp()
    window.show()
    sys.exit(app.exec())


