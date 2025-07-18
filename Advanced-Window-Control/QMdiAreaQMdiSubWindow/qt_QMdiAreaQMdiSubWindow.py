import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

"""
QMdiArea（多文档界面区域）是一个可以包含多个子窗口（QMdiSubWindow）的容器控件。它提供了平铺、层叠等排列子窗口的功能，类似于许多IDE或图像编辑软件的窗口管理方式。
"""

class MdiAreaDemo(QMainWindow):
    def __init__(self, parent=None):
        super(MdiAreaDemo, self).__init__(parent)
        self.count = 0
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("QMdiArea+QMdiSubWindow demo")

        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("ShowSubList")
        file.addSeparator()
        file.addAction("cascade")
        file.addAction("Titled")
        file.addSeparator()
        self.nextAct = QAction("Next")
        self.nextAct.setShortcuts(QKeySequence.New)
        self.nextAct.triggered.connect(self.mdi.activateNextSubWindow)
        file.addAction(self.nextAct)
        self.preAct = QAction("Pre")
        self.preAct.setShortcuts(QKeySequence(Qt.CTRL | Qt.Key_P))
        self.preAct.triggered.connect(self.mdi.activatePreviousSubWindow)
        file.addAction(self.preAct)
        file.triggered[QAction].connect(self.windowaction)
        file.addSeparator()
        order = file.addMenu("setOrder")
        order.addAction("create")
        order.addAction("stack")
        order.addAction("activateHistory")
        order.triggered[QAction].connect(self.orderAction)
        file.addSeparator()
        view = file.addMenu("setViewMode")
        view.addAction("subWindow")
        view.addAction("tabWindow")
        view.triggered[QAction].connect(self.viewAction)

        # 没有设置父对象 以及加入到其他布局等组件中 
        # 以单独的窗口形式打开
        self.text = QPlainTextEdit()
        self.text.setWindowTitle("显示信息")
        self.text.resize(400, 600)
        self.text.move(100, 200)
        self.text.show()

        # 添加QWidget窗口
        widget = QWidget()
        textEdit = QTextEdit(widget)
        layout1 = QHBoxLayout()
        layout1.addWidget(textEdit)
        widget.setLayout(layout1)
        widget.setWindowTitle("QWidget窗口")
        widget.resize(300, 400)
        self.mdi.addSubWindow(widget)

        # 添加QWidget2
        widget2 = QWidget()
        textEdit2 = QTextEdit()
        midWidget = self.mdi.addSubWindow(widget2)
        midWidget.setWidget(textEdit2)
        midWidget.setWindowTitle("QWidget窗口2")

        # 添加窗口3
        midWidget2 = self.mdi.addSubWindow(QTextEdit())
        midWidget2.setWindowTitle("QWidget窗口3")

        # 添加QMdiSubWindow窗口
        mdiSub = self.getMdiSubWindow(title="QMdiSubWindow窗口")
        self.mdi.addSubWindow(mdiSub)

        # 添加窗口-shaded
        mdiSub2 = self.getMdiSubWindow(title="shaded窗口")
        self.mdi.addSubWindow(mdiSub2)
        mdiSub2.showShaded()

        # 添加窗口-Option
        mdiSub3 = self.getMdiSubWindow(title="Option窗口")
        mdiSub3.setOption(QMdiSubWindow.RubberBandMove, on=True)
        mdiSub3.setOption(QMdiSubWindow.RubberBandResize, on=True)
        self.mdi.addSubWindow(mdiSub3)

        self.mdi.subWindowActivated.connect(lambda x: self.text.insertPlainText(f'\n触发subWindowActivated信号,title:{x.windowTitle() if x !=None else x}'))
        self.showInfo()
    
    def getMdiSubWindow(self, title=''):
        mdiSub = QMdiSubWindow()
        mdiSub.setWidget(QTextEdit())
        mdiSub.setWindowTitle(title)
        mdiSub.aboutToActivate.connect(lambda : self.text.insertPlainText(f"\n触发aboutToActive信号，title:{title}"))
        mdiSub.windowStateChanged.connect(lambda old,new:self.text.insertPlainText(f"\n触发windowStateChanged信号，title:{title},old:{self.getState(old)},new:{self.getState(new)}"))
        return mdiSub

    def getState(self,status):
        if status ==  Qt.WindowState.WindowNoState:
            return 'WindowNoState'
        elif status ==  Qt.WindowState.WindowMinimized:
            return 'WindowMinimized'
        elif status ==  Qt.WindowState.WindowMaximized:
            return 'WindowMaximized'
        elif status ==  Qt.WindowState.WindowMaximized:
            return 'WindowMaximized'
        elif status ==  Qt.WindowState.WindowActive:
            return 'WindowActive'
        else:
            return 'None'

    def windowaction(self,q):
        if q.text() == "New":
            self.count = self.count + 1
            sub = self.getMdiSubWindow(title="NewWindow" + str(self.count))
            self.mdi.addSubWindow(sub)
            sub.show()
        elif q.text() == "cascade":
            """
            cascadeSubWindows(): 层叠排列子窗口
            tileSubWindows(): 平铺排列子窗口
            arrangeIcons(): 排列最小化的子窗口图标
            """
            self.mdi.cascadeSubWindows()
        elif q.text() == "Tiled":
            self.mdi.tileSubWindows()
        elif q.text() == 'ShowSubList':
            self.showInfo()
    
    def orderAction(self, q):
        if q.text() == 'create':
            # 这意味着窗口将按照它们被创建的先后顺序激活
            self.mdi.setActivationOrder(self.mdi.CreationOrder)
        elif q.text() == 'stack':
            # 这意味着窗口将按照它们在屏幕上的 Z 顺序（前后堆叠顺序）激活
            self.mdi.setActivationOrder(self.mdi.StackingOrder)
        elif q.text() == 'activateHistory':
            # 这意味着窗口将按照它们被激活的历史记录顺序激活
            self.mdi.setActivationOrder(self.mdi.ActivationHistoryOrder)
        self.showInfo()
    
    def viewAction(self, q):
        if q.text() == 'subWindow':
            # 将 MDI 设为 ​​子窗口模式​​，子窗口可以自由移动和调整大小
            self.mdi.setViewMode(self.mdi.SubWindowView)
        elif q.text() == 'tabWindow':
            # 将 MDI 设为 ​​标签页模式​​，所有子窗口以标签页形式排列
            self.mdi.setViewMode(self.mdi.TabbedView)

    def showInfo(self):
        orderList = self.mdi.subWindowList(order=self.mdi.activationOrder())

        self.text.insertPlainText(f'\n当前排序方式：{self.mdi.activationOrder().name}，最新subWindowList:')

        count = 1
        for subWindow in orderList:
            title = subWindow.windowTitle()
            title = title.split('--')[1] if '--' in title else title
            subWindow.setWindowTitle(f'{count}--{title}')
            print(f'\nnum:{count},title:{subWindow.windowTitle()},shaded:{subWindow.isShaded()}')
            self.text.insertPlainText(f'\nnum:{count},title:{subWindow.windowTitle()},shaded:{subWindow.isShaded()}')
            count += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MdiAreaDemo()
    demo.show()
    sys.exit(app.exec())

    



        