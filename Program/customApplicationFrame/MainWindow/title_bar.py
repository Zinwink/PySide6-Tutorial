from PySide6.QtWidgets import QWidget, QVBoxLayout,QFrame,QHBoxLayout,QLabel
from PySide6.QtGui import QCursor,Qt
from PySide6.QtCore import QSize
from title_button import TitleButton


class TitleBar(QWidget):
    def __init__(
        self,
        parent,
        bg_color = "#E2E9F7",
        btn_bg_color = "#E2E9F7",
        btn_bg_color_hover = "#EFF1F7",
        btn_bg_color_pressed = "#D3E0F7",
        icon_color = "#606F88",
        icon_color_hover = "#79A1E1",
        icon_color_pressed = "#5a86e0",
        radius = 8,
        font_family = "Segoe UI",
        title_size = 10
    ):
        super().__init__()

        self._bg_color = bg_color
        self._parent = parent
        self._btn_bg_color = btn_bg_color
        self._btn_bg_color_hover = btn_bg_color_hover
        self._btn_bg_color_pressed = btn_bg_color_pressed  
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._font_family = font_family
        self._title_size = title_size

        # self._is_maximized = parent.isMaximized()

        # SETUP UI
        self.setup_ui()

        # ADD BG COLOR
        self.bg.setStyleSheet(f"background-color: {bg_color}; border-radius: {radius}px;")


        # MOVE WINDOW / MAXIMIZE / RESTORE
        # ///////////////////////////////////////////////////////////////
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if parent.isMaximized():
                self.maximize_restore()
                # self.resize(self._old_size)
                cursor_x = parent.pos().x()
                cursor_y = parent.pos().y()
                # cursor_y = event.globalPos().y() - QCursor.pos().y()
                # cursor_y =   QCursor.pos().y() - event.globalPos().y()
                parent.move(cursor_x,cursor_y)
            if event.buttons() == Qt.LeftButton:
                parent.move(parent.pos()+event.globalPos()-self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.title_label.mouseMoveEvent = moveWindow
        self.bg.mouseMoveEvent = moveWindow
        
        self.title_label.mouseDoubleClickEvent = self.maximize_restore

        # ADD BUTTONS BUTTONS
        # ///////////////////////////////////////////////////////////////
        # Functions
        self.minimize_button.released.connect(lambda: parent.showMinimized())
        self.maximize_restore_button.released.connect(lambda: self.maximize_restore())
        self.close_button.released.connect(lambda: parent.close())
    
    def set_title(self, title):
        self.title_label.setText(title)
    
    # MAXIMIZE / RESTORE
    # maximize and restore parent window
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self, e = None):
        def change_ui():
            if self._parent.isMaximized():
                self.maximize_restore_button.set_icon(
                    "/media/mole/G/Program/PySide6-Tutorial/Program/customApplicationFrame/MainWindow/icon_restore.svg"
                )
            else:
                self.maximize_restore_button.set_icon(
                    "/media/mole/G/Program/PySide6-Tutorial/Program/customApplicationFrame/MainWindow/icon_maximize.svg"
                )
        if self._parent.isMaximized():
            # self._is_maximized=False
            self._parent.showNormal()
            # self._parent.setFixedSize(self._old_size)
            # self.resize(self._old_size)
            change_ui()
        else:
            # self._is_maximized = True
            self._old_size = QSize(self._parent.width(),self._parent.height())
            self._parent.showMaximized()
            change_ui()

    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        dragPosF = event.globalPosition()
        self.dragPos = dragPosF.toPoint()
        
    def setup_ui(self):
        self.title_bar_layout = QVBoxLayout(self)
        self.title_bar_layout.setContentsMargins(0,0,0,0)

        self.bg = QFrame()
        self.bg_layout = QHBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(10,0,5,0)
        self.bg_layout.setSpacing(0)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.title_label.setStyleSheet(f'font: {self._title_size}pt "{self._font_family}"')
        
        self.minimize_button = TitleButton(
            self._parent,
            bg_color = self._btn_bg_color,
            bg_color_hover = self._btn_bg_color_hover,
            bg_color_pressed = self._btn_bg_color_pressed,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_hover,
            icon_color_pressed = self._icon_color_pressed,
            radius = 6,
            icon_path="/media/mole/G/Program/PySide6-Tutorial/Program/customApplicationFrame/MainWindow/icon_minimize.svg"
        )

        self.maximize_restore_button = TitleButton(
            self._parent,
            bg_color = self._btn_bg_color,
            bg_color_hover = self._btn_bg_color_hover,
            bg_color_pressed = self._btn_bg_color_pressed,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_hover,
            icon_color_pressed = self._icon_color_pressed,
            radius = 6,
            icon_path="/media/mole/G/Program/PySide6-Tutorial/Program/customApplicationFrame/MainWindow/icon_maximize.svg"
        )

        self.close_button = TitleButton(
            self._parent,
            bg_color = self._btn_bg_color,
            bg_color_hover = self._btn_bg_color_hover,
            bg_color_pressed = self._btn_bg_color_pressed,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_hover,
            icon_color_pressed = self._icon_color_pressed,
            radius = 6,
            icon_path="/media/mole/G/Program/PySide6-Tutorial/Program/customApplicationFrame/MainWindow/icon_close.svg"
        )

        self.bg_layout.addWidget(self.title_label)
        self.bg_layout.addWidget(self.minimize_button)
        self.bg_layout.addWidget(self.maximize_restore_button)
        self.bg_layout.addWidget(self.close_button)
        self.title_bar_layout.addWidget(self.bg)





        

    