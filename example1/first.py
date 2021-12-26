from PyQt5.QtWidgets import *
import sys

app = QApplication(sys.argv)
window = QWidget()
window.setGeometry(0,0,500,500)
window.setWindowTitle('First')

window.windowTitle()

window.show()

sys.exit(app.exec_())
