import sys
from PySide6.QtCore import QDate, QFile, Qt, QTextStream
from PySide6.QtGui import QAction, QFont, QIcon, QKeySequence, QTextCharFormat,QTextCursor, QTextTableFormat
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import QApplication, QDialog, QDockWidget,QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit

import os 
os.chdir(os.path.dirname(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self._text_edit = QTextEdit()
        self.setCentralWidget(self._text_edit)

        self.create_actions()
        self.create_menus()
        self.create_tool_bars()
        self.create_status_bar()
        self.create_dock_windows()

        self.setWindowTitle("Dock Widgets")

        self.new_letter()

    def new_letter(self):
        self._text_edit.clear()

        cursor = self._text_edit.textCursor()
        # 移动到文档开始
        cursor.movePosition(QTextCursor.Start)
        """
        QTextFrame 是 QTextDocument 中的一个容器元素，可以包含其他文档元素（文本块、表格、图片等）。它类似于 HTML 中的 <div> 元素，用于组织文档结构。
        """
        top_frame = cursor.currentFrame()
        top_frame_format = top_frame.frameFormat()
        top_frame_format.setPadding(16)
        top_frame.setFrameFormat(top_frame_format)

        text_format = QTextCharFormat()
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)

        """
        QTextTableFormat 是 PySide6 中用于定义表格样式和布局的类，继承自 QTextFrameFormat。它提供了控制表格外观和行为的各种属性设置。
        """
        table_format = QTextTableFormat()
        table_format.setBorder(1)
        table_format.setCellPadding(16)
        table_format.setAlignment(Qt.AlignRight)
        cursor.insertTable(1, 1, table_format)
        cursor.insertText("The Firm", bold_format)
        cursor.insertBlock()
        cursor.insertText("321 City Street", text_format)
        cursor.insertBlock()
        cursor.insertText("Industry Park")
        cursor.insertBlock()
        cursor.insertText("Some Country")
        cursor.setPosition(top_frame.lastPosition())
        cursor.insertText(QDate.currentDate().toString("d MMMM yyyy"),
                          text_format)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Dear ", text_format)
        cursor.insertText("NAME", italic_format)
        cursor.insertText(",", text_format)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("Yours sincerely,", text_format)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("The Boss", text_format)
        cursor.insertBlock()
        cursor.insertText("ADDRESS", italic_format)


    def print_(self):
        document = self._text_edit.document()
        printer = QPrinter()

        dlg = QPrintDialog(printer, self)
        if dlg.exec() != QDialog.Accepted:
            return

        document.print_(printer)

        self.statusBar().showMessage("Ready", 2000)
    
    def save(self):
        dialog = QFileDialog(self, "Choose a file name")
        # 设置文件过滤器
        # dialog.setNameFilter("HTML 文件 (*.html *.htm)")
        dialog.setMimeTypeFilters(["text/html"])
        # QFileDialog.AcceptOpen: 打开文件模式 默认
        # QFileDialog.AcceptSave : 保存文件模式 （去任按钮显示“保存”而不是“打开”）
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("html")
        if dialog.exec() != QDialog.Accepted:
            return
        # 选择的文件路径名
        filename = dialog.selectedFiles()[0]
        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            reason = file.errorString()
            QMessageBox.warning(self,"Dock Widgets","Cannot write file {filename}:\n{reason}")
            return
        out = QTextStream(file)
        # 覆盖光标， 重新设置光标样式为 等待状态
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self._text_edit.toHtml()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage(f"Saved '{filename}'",2000)
    
    def undo(self):
        document = self._text_edit.document()
        document.undo()

    def insert_customer(self,customer):
        if not customer:
            return
        customer_list = customer.split(", ")
        document = self._text_edit.document()
        cursor = document.find("NAME")
        if not cursor.isNull():
            """
            beginEditBlock() 和 endEditBlock() 则是用来将多个编辑操作组合成一个原子操作的重要方法
            beginEditBlock() 开始一个编辑块（edit block），标记一系列编辑操作的开始
            endEditBlock() 结束当前编辑块，标记一系列编辑操作的结束
            insertText(text) 在光标位置插入文本
            insertBlock() 插入一个新的文本块（类似于段落）
            """
            cursor.beginEditBlock()
            cursor.insertText(customer_list[0])
            oldcursor = cursor
            cursor = document.find("ADDRESS")
            if not cursor.isNull():
                for i in customer_list[1:]:
                    cursor.insertBlock()
                    cursor.insertText(i)
                cursor.endEditBlock()
            else:
                oldcursor.endEditBlock()
    
    def add_paragraph(self, paragraph):
        if not paragraph:
            return
        document = self._text_edit.document()
        cursor = document.find("Yours sincerely,")
        if cursor.isNull():
            return
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor,2) # 将光标向上移动两个文本块
        cursor.insertBlock()
        cursor.insertText(paragraph)
        cursor.insertBlock()
        cursor.endEditBlock()
    
    def about(self):
        QMessageBox.about(self, "About Dock Widgets",
                          "The <b>Dock Widgets</b> example demonstrates how to use "
                          "Qt's dock widgets. You can enter your own text, click a "
                          "customer to add a customer name and address, and click "
                          "standard paragraphs to add them.")

    def create_actions(self):
        # fromTheme从系统主题图标中获取图标， 未找到则使用备用的fallback
        icon = QIcon.fromTheme('document-new',QIcon('./new.png'))
        self._new_letter_act = QAction(icon, "&New Letter",self,
                                       shortcut=QKeySequence.New,statusTip="Create a new form letter",triggered=self.new_letter)
        
        icon = QIcon.fromTheme("document-save",QIcon("./save.png"))
        self._save_act = QAction(icon,"&Save...",self,
                                 shortcut=QKeySequence.Save,
                                 statusTip="Save the current form letter",triggered=self.save)
        
        icon = QIcon.fromTheme("document-print",QIcon("./printer.png"))
        self._print_act = QAction(icon, "&Print...",self,
                                  shortcut=QKeySequence.Print,
                                  statusTip="Print the current form letter",
                                  triggered=self.print_)
        icon = QIcon.fromTheme("edit-undo",QIcon("./undo.png"))
        self._undo_act = QAction(icon,"&Undo",self,
                                 shortcut=QKeySequence.Undo,
                                 statusTip="Undo the last editing action",
                                 triggered=self.undo)
        
        self._quit_act = QAction("&Quit",self,shortcut="Ctrl+Q",
                                 statusTip="Quit the application",triggered=self.close)
        
        self._about_act = QAction("&About",self,statusTip="Show the application's about box",triggered=self.about)

        self._about_qt_act = QAction("About &Qt",self,statusTip="Show the Qt library's About box",triggered=QApplication.instance().aboutQt)
    
    def create_menus(self):
        self._file_menu = self.menuBar().addMenu("&File")
        self._file_menu.addAction(self._new_letter_act)
        self._file_menu.addAction(self._save_act)
        self._file_menu.addAction(self._print_act)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self._quit_act)

        self._edit_menu = self.menuBar().addMenu("&Edit")
        self._edit_menu.addAction(self._undo_act)

        self._view_menu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self._help_menu = self.menuBar().addMenu("&Help")
        self._help_menu.addAction(self._about_act)
        self._help_menu.addAction(self._about_qt_act)

    def create_tool_bars(self):
        self._file_tool_bar = self.addToolBar("File")
        self._file_tool_bar.addAction(self._new_letter_act)
        self._file_tool_bar.addAction(self._save_act)
        self._file_tool_bar.addAction(self._print_act)

        self._edit_tool_bar = self.addToolBar("Edit")
        self._edit_tool_bar.addAction(self._undo_act)
    
    def create_status_bar(self):
        self.statusBar().showMessage("Ready")
    
    def create_dock_windows(self):
        dock = QDockWidget("Customers", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._customer_list = QListWidget(dock)
        self._customer_list.addItems(
            (
            "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton",
            "Jane Doe, Memorabilia, 23 Watersedge, Beaton",
            "Tammy Shea, Tiblanka, 38 Sea Views, Carlton",
            "Tim Sheen, Caraba Gifts, 48 Ocean Way, Deal",
            "Sol Harvey, Chicos Coffee, 53 New Springs, Eccleston",
            "Sally Hobart, Tiroli Tea, 67 Long River, Fedula"
            )
        )
        dock.setWidget(self._customer_list)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self._view_menu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Paragraphs", self)
        self._paragraphs_list = QListWidget(dock)
        self._paragraphs_list.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
            "28 days.",
            "We have dispatched those items that were in stock. The rest of "
            "your order will be dispatched once all the remaining items "
            "have arrived at our warehouse. No additional shipping "
            "charges will be made.",
            "You made a small overpayment (less than $5) which we will keep "
            "on account for you, or return at your request.",
            "You made a small underpayment (less than $1), but we have sent "
            "your order anyway. We'll add this underpayment to your next "
            "bill.",
            "Unfortunately you did not send enough money. Please remit an "
            "additional $. Your order will be dispatched as soon as the "
            "complete amount has been received.",
            "You made an overpayment (more than $5). Do you wish to buy more "
            "items, or should we return the excess to you?"))
        dock.setWidget(self._paragraphs_list)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self._view_menu.addAction(dock.toggleViewAction())

        self._customer_list.currentTextChanged.connect(self.insert_customer)
        self._paragraphs_list.currentTextChanged.connect(self.add_paragraph)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())