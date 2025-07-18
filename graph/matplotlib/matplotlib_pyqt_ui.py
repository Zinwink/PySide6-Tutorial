# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'matplotlib_pyqt.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

from MatplotlibWidget import MatplotlibWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 781, 541))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.DynamicGraphWidget = MatplotlibWidget(self.layoutWidget)
        self.DynamicGraphWidget.setObjectName(u"DynamicGraphWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.DynamicGraphWidget.sizePolicy().hasHeightForWidth())
        self.DynamicGraphWidget.setSizePolicy(sizePolicy1)
        self.DynamicGraphWidget.setMinimumSize(QSize(200, 80))

        self.horizontalLayout_2.addWidget(self.DynamicGraphWidget)

        self.showDynamicBtn = QPushButton(self.layoutWidget)
        self.showDynamicBtn.setObjectName(u"showDynamicBtn")

        self.horizontalLayout_2.addWidget(self.showDynamicBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.StaticGraphWidget = MatplotlibWidget(self.layoutWidget)
        self.StaticGraphWidget.setObjectName(u"StaticGraphWidget")
        sizePolicy1.setHeightForWidth(self.StaticGraphWidget.sizePolicy().hasHeightForWidth())
        self.StaticGraphWidget.setSizePolicy(sizePolicy1)
        self.StaticGraphWidget.setMinimumSize(QSize(200, 80))

        self.horizontalLayout.addWidget(self.StaticGraphWidget)

        self.showStaticBtn = QPushButton(self.layoutWidget)
        self.showStaticBtn.setObjectName(u"showStaticBtn")

        self.horizontalLayout.addWidget(self.showStaticBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.showDynamicBtn.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u52a8\u6001\u56fe", None))
        self.showStaticBtn.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u9759\u6001\u56fe", None))
    # retranslateUi

