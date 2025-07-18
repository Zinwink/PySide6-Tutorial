from PySide6.QtWidgets import QWidget, QFrame, QSizeGrip
from PySide6.QtCore import QRect,Qt
from PySide6.QtGui import QCursor


# 四个边角的grips用于控制窗口大小 左上角、右上角、左下角、右下角
class GripsTopLeft(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setFixedSize(15, 15)
        self.grip_container.setStyleSheet(u"background-color: #333; border: 2px solid #55FF00;")
        self.grip = QSizeGrip(self.grip_container)
        self.grip.setFixedSize(self.grip_container.size())
        # (5,5)是相对于父容器的左上角坐标位置， 父容器左上角为(0,0)
        self.setGeometry(5, 5, 15, 15)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None

class GripsTopRight(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setFixedSize(15, 15)
        self.grip_container.setStyleSheet(u"background-color: #333; border: 2px solid #55FF00;")
        self.grip = QSizeGrip(self.grip_container)
        self.grip.setFixedSize(self.grip_container.size())
        # (5,5)是相对于父容器的左上角坐标位置， 父容器左上角为(0,0)
        self.setGeometry(self.parent.width()-20, 5, 15, 15)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None
    
    def resizeEvent(self, event):
        # 当 QWidget父容器改变大小时, 包含的grip也改变
        self.grip_container.setGeometry(self.width()-15,0,15,15)

class GripsBottomLeft(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setFixedSize(15, 15)
        self.grip_container.setStyleSheet(u"background-color: #333; border: 2px solid #55FF00;")
        self.grip = QSizeGrip(self.grip_container)
        self.grip.setFixedSize(self.grip_container.size())
        # (5,5)是相对于父容器的左上角坐标位置， 父容器左上角为(0,0)
        self.setGeometry(5, self.parent.height()-20, 15, 15)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None
    
    def resizeEvent(self, event):
        # 当 QWidget父容器改变大小时, 包含的grip也改变
        self.grip_container.setGeometry(0,self.height()-15,15,15)

class GripsBottomRight(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setFixedSize(15, 15)
        self.grip_container.setStyleSheet(u"background-color: #333; border: 2px solid #55FF00;")
        self.grip = QSizeGrip(self.grip_container)
        self.grip.setFixedSize(self.grip_container.size())
        # (5,5)是相对于父容器的左上角坐标位置， 父容器左上角为(0,0)
        self.setGeometry(self.parent.width()-20, self.parent.height()-20, 15, 15)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None
    
    def resizeEvent(self, event):
        # 当 QWidget父容器改变大小时, 包含的grip也改变
        self.grip_container.setGeometry(self.width()-15,self.height()-15,15,15)

class GripsTop(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setGeometry(0,0,500,10)
        self.grip_container.setStyleSheet(u"background-color: rgb(85, 255, 255);")
        self.grip_container.setCursor(QCursor(Qt.SizeVerCursor))
        self.setGeometry(20, 0, self.parent.width()-40, 10)
        self.setMaximumHeight(10)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def mouseMoveEvent(self, event):
        # QMouseEvent.pos 返回的是（QPoint 对象） 相对于父容器的偏移 ，delta.y() 是垂直方向的偏移量
        delta = event.pos()
        height = max(self.parent.minimumHeight(),self.parent.height()-delta.y())
        geo = self.parent.geometry()
        geo.setTop(geo.bottom()-height)
        self.parent.setGeometry(geo)
        event.accept()

    def resizeEvent(self, event):
        # 当 QWidget父容器改变大小时, 包含的grip也改变
        self.grip_container.setGeometry(0,0,self.width(),10)

class GripsBottom(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setGeometry(0,0,500,10)
        self.grip_container.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.grip_container.setCursor(QCursor(Qt.SizeVerCursor))
        self.setGeometry(20, self.parent.height()-10, self.parent.width()-40, 10)
        self.setMaximumHeight(10)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def mouseMoveEvent(self, event):
        # QMouseEvent.pos 返回的是（QPoint 对象） 相对于父容器的偏移 ，delta.y() 是垂直方向的偏移量
        delta = event.pos()
        height = max(self.parent.minimumHeight(),self.parent.height()+delta.y())
        geo = self.parent.geometry()
        geo.setBottom(geo.top()+height)
        self.parent.setGeometry(geo)
        event.accept()

    def resizeEvent(self, event):
        # 当 QWidget父容器改变大小时, 包含的grip也改变
        self.grip_container.setGeometry(0,0,self.width(),10)

class GripsLeft(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setGeometry(0,0,10,480)
        self.grip_container.setStyleSheet(u"background-color: rgb(255, 121, 198);")
        self.grip_container.setCursor(QCursor(Qt.SizeHorCursor))
        self.setGeometry(0, 20, 10, self.height()-40)
        self.setMaximumWidth(10)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def mouseMoveEvent(self, event):
        # QMouseEvent.pos 返回的是（QPoint 对象） 相对于父容器的偏移 ，delta.y() 是垂直方向的偏移量
        delta = event.pos()
        width = max(self.parent.minimumWidth(),self.parent.width()-delta.x())
        geo = self.parent.geometry()
        geo.setLeft(geo.right()-width)
        self.parent.setGeometry(geo)
        event.accept()

    def resizeEvent(self, event):
        # 当 QWidget父容器改变大小时, 包含的grip也改变
        self.grip_container.setGeometry(0,0,10,self.height())
    
class GripsRight(QWidget):
    def __init__(self, parent, disable_color=False):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        
        self.grip_container = QFrame(self)
        self.grip_container.setGeometry(0,0,10,480)
        self.grip_container.setStyleSheet(u"background-color: rgb(255, 0, 127);")
        self.grip_container.setCursor(QCursor(Qt.SizeHorCursor))
        self.setGeometry(self.width()-20, 20, 10, self.height()-40)
        self.setMaximumWidth(10)

        if disable_color:
            self.grip_container.setStyleSheet("background: transparent")
    
    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def mouseMoveEvent(self, event):
        # QMouseEvent.pos 返回的是（QPoint 对象） 相对于父容器的偏移 ，delta.y() 是垂直方向的偏移量
        delta = event.pos()
        width = max(self.parent.minimumWidth(),self.parent.width()+delta.x())
        geo = self.parent.geometry()
        geo.setRight(geo.left()+width)
        self.parent.setGeometry(geo)
        event.accept()

    def resizeEvent(self, event):
        # 当 QWidget父容器改变大小时, 包含的grip也改变
        self.grip_container.setGeometry(0,0,10,self.height())