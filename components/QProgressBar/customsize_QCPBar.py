from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPainterPath, QPen, QColor, QFont
from PySide6.QtWidgets import QVBoxLayout, QSlider, QWidget, QApplication

class CPBar(QWidget):
    def __init__(self, parent=None):
        super(CPBar, self).__init__(parent)
        self.p = 0
        self.setMinimumSize(50,50)
    
    def upd(self, pp):
        if self.p == pp:
            return
        self.p = pp
        self.update()
    
    def paintEvent(self, event):
        """_summary_

        Args:
            event (_type_): _description_
        
        paintEvent 会在以下情况下被调用：
            窗口首次显示时
            窗口被其他窗口遮挡后重新显示时
            调用 update() 或 repaint() 方法时
            窗口大小改变时（取决于是否设置了 WA_OpaquePaintEvent 属性）
        """
        if self.height() > self.width():
            self.setFixedWidth(self.height())
        if self.width() > self.height():
            self.setFixedHeight(self.width())
        pd = self.p * 360
        rd = 360 - pd
        p = QPainter(self)
        # p.fillRect(self.rect(), Qt.white)
        p.translate(4, 4)
        p.setRenderHint(QPainter.Antialiasing)
        path, path2 = QPainterPath(), QPainterPath()
        circle_width = self.width() - self.width() / 10
        widht_half = circle_width/2
        # 确定path的起点
        path.moveTo(self.rect().left()+0.5*self.width(), self.rect().top()+0.5*(self.height()-circle_width))  
        circle_rect = QRectF(self.rect().left()+0.5*(self.width()-circle_width), self.rect().top()+0.5*(self.height()-circle_width), circle_width, self.height() - self.height() / 10)
        path.arcTo(circle_rect, 90, -pd)
        pen, pen2 = QPen(), QPen()
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(QColor("#30b7e0"))
        pen_width = self.width()/25
        pen.setWidth(pen_width)
        p.strokePath(path, pen)
        # 确定path的起点
        path2.moveTo(self.rect().left()+0.5*self.width(), self.rect().top()+0.5*(self.height()-circle_width))
        pen2.setWidth(pen_width)
        pen2.setColor(QColor("#d7d7d7"))
        pen2.setCapStyle(Qt.FlatCap)
        # 设置虚线样式 0.5为实线比利 1.105为虚线比例
        pen2.setDashPattern([0.5, 1.105]) # remove this line to have continue cercle line
        path2.arcTo(circle_rect, 90, rd)
        pen2.setDashOffset(2.2) # this one too
        p.strokePath(path2, pen2) # 按照QPath , QPen对照轨迹画图

        p.setPen(pen)
        font = QFont()
        percent_size = self.height() / 7
        # 带有F 用于设置浮点版本尺寸
        font.setPointSizeF(percent_size)
        p.setFont(font)
        percent_text_position = self.rect().center()
        p_in_percent = self.p * 100
        percent_text_position.setX(percent_text_position.x() - (
                percent_size + (self.width()/6 if p_in_percent >= 100 else self.width()/10 if p_in_percent >= 10 else +self.width()/40)))
        percent_text_position.setY(percent_text_position.y() + percent_size * 2 / 5)
        # drawText 默认使用​​文本基线(baseline)​​的左下角作为定位点
        p.drawText(percent_text_position, f"{round(self.p * 100, 0)}%")

class Test(QWidget):
    def __init__(self):
        super().__init__()
        l = QVBoxLayout(self)
        p = CPBar(self)
        s = QSlider(Qt.Horizontal, self)
        s.setMinimum(0)
        s.setMaximum(100)
        l.addWidget(p)
        l.addWidget(s)
        self.setLayout(l)
        s.valueChanged.connect(lambda: p.upd(s.value() / s.maximum()))
        # connect(s, &QSlider::valueChanged, [=](){ p->upd((qreal)s->value() / s->maximum());});

if __name__ == '__main__':
    app = QApplication()
    main_widget = Test()
    main_widget.show()
    app.exec()

    