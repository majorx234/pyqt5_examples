from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QMetaObject, QTimer
import sys
import signal
from dynamic_list_widget import DynamicListWidget

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QApplication.quit()
    sys.exit(0)


class GuiMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(GuiMainWindow, self).__init__(parent)

        self.setGeometry(100, 100, 877, 712)

        self.setWindowTitle('Dynamic List View')

        self.centralWidget = DynamicListWidget(self)
        self.centralWidget.setObjectName("centralwidget")

        self.setCentralWidget(self.centralWidget)

        openAction = QAction(QIcon('open.png'),'&Open',self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.loadImage)
        
        saveAction = QAction(QIcon('save.png'),'&Save',self)
        saveAction.setShortcut('Ctrl+S')
        #saveAction.triggered.connect(self.centralWidget.savePhoto)

        closeAction = QAction(QIcon('close.png'),'&Close',self)
        closeAction.setShortcut('Ctrl+C')
        closeAction.triggered.connect(self.close)
        
        self.menuBar = QMenuBar(self)
        self.fileMenu = self.menuBar.addMenu('&File')
        self.fileMenu.addAction(openAction)
        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(closeAction)
        
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
                                                        
        self.show()

    def loadImage(self):
        """ This function will load the user selected image
            and set it to label using the setPhoto function
        """
        filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.centralWidget.addImage(filename)
        
    def closeEvent(self, event):
            event.accept()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    app = QApplication(sys.argv)
    main_window = GuiMainWindow()
    main_window.show()
    # timer for check signal handling
    timer = QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)   
    sys.exit(app.exec_())
