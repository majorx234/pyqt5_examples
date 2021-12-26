from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()

        button = QPushButton('Close', self)
        button.move(50, 50)
        button.setToolTip("close Window")
        button.clicked.connect(self.close)

        self.setGeometry(400, 400, 200, 200)

        self.setWindowTitle('First Window')
        self.setWindowIcon(QIcon('windowicon.png'))

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Should these window closed?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FirstWindow()
    app.quit
    sys.exit(app.exec_())
            

