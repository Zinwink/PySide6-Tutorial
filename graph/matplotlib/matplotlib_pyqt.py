
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QApplication

from matplotlib_pyqt_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.StaticGraphWidget.setVisible(False)
        self.DynamicGraphWidget.setVisible(False)


    @Slot()
    def on_showStaticBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.StaticGraphWidget.setVisible(True)
        self.StaticGraphWidget.mpl.start_dynamic_plot()
    
    @Slot()
    def on_showDynamicBtn_clicked(self):
        self.DynamicGraphWidget.setVisible(True)
        self.DynamicGraphWidget.mpl.start_dynamic_plot()
    
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())