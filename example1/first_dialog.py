from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        buttonClose = QPushButton('Close', self)
        buttonClose.move(50, 25)
        buttonClose.setToolTip("close Window")
        buttonClose.clicked.connect(self.close)

        buttonDialog = QPushButton('Dialog', self)
        buttonDialog.move(150, 25)
        buttonDialog.setToolTip("open dialog")
        buttonDialog.clicked.connect(self.openDialog)

        self.setGeometry(400, 400, 300, 100)

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
    def openDialog(self, event):
        print("openDialog")
        dialog = FirstDialog(self)

        dialog.saveWindowSize.setChecked(True)
        dialog.language.setCurrentText('English')
        dialog.dbFile.setText("/")

    #    if dialog.exec_(): #Modal
    #        print('saving window: {}'.format(dialog.saveWindowSize.isChecked()))
    #    else:
    #        print('no saving')

    #not modal -> modeless
        dialog.show()


class FirstDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(100,100,250,180)
        self.setWindowTitle("Properties")

        verticalLayout = QVBoxLayout()
        self.saveWindowSize = QCheckBox('save window size on exit')
        verticalLayout.addWidget(self.saveWindowSize)

        formLayout = QFormLayout()
        formLayout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.dbFileLabel = QLabel('DB-File')
        formLayout.setWidget(0, QFormLayout.LabelRole, self.dbFileLabel)

        horizontalLayout = QHBoxLayout()
        self.dbFile = QLineEdit()
        horizontalLayout.addWidget(self.dbFile)
        self.dbFileButton = QPushButton("?")
        horizontalLayout.addWidget(self.dbFileButton)

        self.dbFileButton.clicked.connect(self.showFileDialog)
        formLayout.setLayout(0, QFormLayout.FieldRole, horizontalLayout)
        self.languageLabel = QLabel('Language')
        self.language = QComboBox()
        self.language.addItems(['English', 'Spanish', 'French'])
        formLayout.setWidget(1, QFormLayout.FieldRole, self.language)
        verticalLayout.addLayout(formLayout)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        verticalLayout.addWidget(self.buttonBox)

        self.setLayout(verticalLayout)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
    def showFileDialog(self):
#        file_name = QFileDialog.getOpenFileName(self, 'DB-file', '/', 'DB-file (*.db);;all files (*.*)') 
        fileDialog = QFileDialog(self, 'DB-file', '/', 'DB-file (*.db);;all files (*.*)')
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setViewMode(QFileDialog.Detail)
        fileDialog.exec()
        file_name = fileDialog.selectedFiles()

        if file_name[0]:
            self.dbFile.setText(file_name[0])

    def closeEvent(self, event):
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
       
    app.quit
    sys.exit(app.exec_())
    
