import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from MainWinMenuToolbar_ui import Ui_MainWindow
import os

class MainForm (QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm,self).__init__()
        self.setupUi(self)
        self.openCalc.triggered.connect(lambda: os.system('gnome-calculator'))
        self.fileCloseAction.triggered.connect(self.close)
        self.fileOpenAction.triggered.connect(self.openFile)

    def openFile(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开","C:/","All Files (*);;Text Files (*.txt)")
        # 在状态栏显示文件地址
        self.statusbar.showMessage(file)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec())