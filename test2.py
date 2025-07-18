import json
from PySide6.QtWidgets import (QApplication, QWidget, QFormLayout, QLineEdit, 
                              QComboBox, QSpinBox, QPushButton, QTextEdit, 
                              QMessageBox)
from PySide6.QtCore import Qt

class FormApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("表单数据提交")
        self.resize(400, 300)
        
        # 创建表单布局
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        # 创建表单字段
        self.name_edit = QLineEdit()
        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 120)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["男", "女", "其他"])
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("example@example.com")
        
        # 添加字段到表单
        self.layout.addRow("姓名:", self.name_edit)
        self.layout.addRow("年龄:", self.age_spin)
        self.layout.addRow("性别:", self.gender_combo)
        self.layout.addRow("邮箱:", self.email_edit)
        
        # 添加提交按钮
        self.submit_btn = QPushButton("提交表单")
        self.submit_btn.clicked.connect(self.submit_form)
        self.layout.addRow(self.submit_btn)
        
        # 添加显示JSON结果的文本框
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("JSON数据将显示在这里...")
        self.layout.addRow(self.result_display)

    def submit_form(self):
        """收集表单数据并转换为JSON格式"""
        # 获取表单数据
        form_data = {
            "name": self.name_edit.text().strip(),
            "age": self.age_spin.value(),
            "gender": self.gender_combo.currentText(),
            "email": self.email_edit.text().strip()
        }
        
        # 验证必填字段
        if not form_data["name"]:
            QMessageBox.warning(self, "警告", "姓名不能为空!")
            return
            
        # 转换为JSON字符串
        try:
            json_data = json.dumps(form_data, ensure_ascii=False, indent=4)
            self.result_display.setPlainText(json_data)
            
            # 在实际应用中，这里可以添加发送到服务器的代码
            # 例如: requests.post(url, json=form_data)
            
            QMessageBox.information(self, "成功", "表单数据已转换为JSON格式!")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成JSON时出错: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = FormApp()
    window.show()
    app.exec()