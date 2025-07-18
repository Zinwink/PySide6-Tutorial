# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWinMenuToolbar.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QToolBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.openCalc = QAction(MainWindow)
        self.openCalc.setObjectName(u"openCalc")
        icon = QIcon(QIcon.fromTheme(u"accessories-calculator"))
        self.openCalc.setIcon(icon)
        self.openCalc.setMenuRole(QAction.MenuRole.NoRole)
        self.fileOpenAction = QAction(MainWindow)
        self.fileOpenAction.setObjectName(u"fileOpenAction")
        self.fileCloseAction = QAction(MainWindow)
        self.fileCloseAction.setObjectName(u"fileCloseAction")
        self.fileCloseAction.setMenuRole(QAction.MenuRole.NoRole)
        self.fileNewAction = QAction(MainWindow)
        self.fileNewAction.setObjectName(u"fileNewAction")
        self.fileNewAction.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu_F = QMenu(self.menubar)
        self.menu_F.setObjectName(u"menu_F")
        self.menu_E = QMenu(self.menubar)
        self.menu_E.setObjectName(u"menu_E")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_F.menuAction())
        self.menubar.addAction(self.menu_E.menuAction())
        self.menu_F.addAction(self.fileOpenAction)
        self.menu_F.addAction(self.fileCloseAction)
        self.menu_F.addAction(self.fileNewAction)
        self.toolBar.addAction(self.openCalc)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.openCalc.setText(QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97\u5668", None))
        self.fileOpenAction.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.fileCloseAction.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed", None))
        self.fileNewAction.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa", None))
        self.menu_F.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6(&F)", None))
        self.menu_E.setTitle(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91(&E)", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

