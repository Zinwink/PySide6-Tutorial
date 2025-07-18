from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt,QRect
from PySide6.QtGui import QPainter,QBrush,QColor,QPixmap

class TitleButton(QPushButton):
    def __init__(
        self,
        parent,
        width = 30,
        height=30,
        radius=8,
        bg_color = "#343b48",
        bg_color_hover = "#3c4454",
        bg_color_pressed = "#2c313c",
        icon_color = "#c3ccdf",
        icon_color_hover = "#dce1ec",
        icon_color_pressed = "#edf0f5",
        icon_path = "no_icon.svg",
        context_color = "#568af2"
    ):
        super().__init__()

        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)
        
        # PROPERTIES
        self._bg_color = bg_color
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed        
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._context_color = context_color
        self._top_margin = self.height() + 6
        # Set Parameters
        self._set_bg_color = bg_color
        self._set_icon_path = icon_path
        self._set_icon_color = icon_color
        self._set_border_radius = radius
        # Parent
        self._parent = parent
    
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        brush = QBrush(QColor(self._set_bg_color))
        
        rect = QRect(0,0,self.width(),self.height())
        paint.setPen(Qt.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(
            rect,
            self._set_border_radius,
            self._set_border_radius
        )
        self.icon_paint(paint,self._set_icon_path,rect)

        paint.end()

    
    def set_icon(self, icon_path):
        self._set_icon_path = icon_path
        self.repaint()
    
    def enterEvent(self, event):
        self._set_bg_color = self._bg_color_hover
        self._set_icon_color = self._icon_color_hover
        self.repaint()
    
    def leaveEvent(self, event):
        self._set_bg_color = self._bg_color
        self._set_icon_color = self._icon_color
        self.repaint()
    
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._set_bg_color = self._bg_color_pressed
            self._set_icon_color = self._icon_color_pressed
            self.repaint()
            self.setFocus()
            return self.clicked.emit()
    
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()
            return self.released.emit()
    
    def icon_paint(self, qp, image, rect):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(),self._set_icon_color)
        
        qp.drawPixmap(
            (rect.width()-icon.width())/2,
            (rect.height()-icon.height())/2,
            icon
        )
        painter.end()
        

