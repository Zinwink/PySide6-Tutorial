from PySide6.QtWidgets import QWidget,QHBoxLayout,QFrame,QSpacerItem,QLabel,QSizePolicy
from PySide6.QtCore import Qt


class PyCredits(QWidget):
    def __init__(self, 
        copyright="@Wink",
        version="0.1.1",
        bg_color="#dfe8cb",
        font_family="SimHei",
        text_size = 11,
        text_description_color="#000000",
        radius = 8,
        padding = 10
    ):
        super(PyCredits, self).__init__()
        self._copyright = copyright
        self._version = version
        self._bg_color = bg_color
        self._font_family = font_family
        self._text_size = text_size
        self._text_description_color = text_description_color
        self._radius = radius
        self._padding = padding
        self.setup_ui()

    def setup_ui(self):
        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0,0,0,0)

        # BG Frame 
        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        
        self.widget_layout.addWidget(self.bg_frame)

        self.bg_layout = QHBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0,0,0,0)

        # ADD COPYRIGHT TEXT
        self.copyright_label = QLabel(self._copyright)
        self.copyright_label.setAlignment(Qt.AlignVCenter)

        # ADD VERSION TEXT
        self.version_label = QLabel(self._version)
        self.version_label.setAlignment(Qt.AlignVCenter)

        # SEPARATOR
        self.separator = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # ADD TO LAYOUT
        self.bg_layout.addWidget(self.copyright_label)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.version_label)

        style = f"""
        #bg_frame {{
            border-radius: {self._radius}px;
            background-color: {self._bg_color};
        }}
        .QLabel {{
            font: {self._text_size}pt "{self._font_family}";
            color: {self._text_description_color};
            padding-left: {self._padding}px;
            padding-right: {self._padding}px;
        }}
        """

        self.bg_frame.setStyleSheet(style)

if __name__ == "__main__":
    from PySide6.QtWidgets import QVBoxLayout,QApplication
    import sys

    class MainWindow(QWidget):
        def __init__(self, parent = None):
            super().__init__(parent)
            self.resize(600,500)
            layout = QVBoxLayout(self)
            layout.addStretch()
            credits = PyCredits(font_family="Times New Roman")
            credits.setContentsMargins(1,0,1,2)
            credits.setFixedHeight(30)
            layout.addWidget(credits)
    
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()

        



