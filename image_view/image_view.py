from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QMetaObject
import numpy as np
import cv2, imutils
import sys
import ui_image_view
                          
class Image_View(QWidget, ui_image_view.Ui_image_view):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

        self.pushButtonApply.clicked.connect(self.update)
        self.pushButtonReset.clicked.connect(self.reset)
#        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Image properties:
        self.image_filename = None # will hold image address
        self.tmp = None # Will hold the temporary image for display

        
    def loadImage(self):
        """ This function will load the user selected image
            and set it to label using the setPhoto function
        """
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image = cv2.imread(self.filename)
        self.old_image = self.image.copy()
        self.setPhoto(self.image)

    def setPhoto(self,image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp = image
        image = imutils.resize(image, width=400)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)

        self.labelImage.setPixmap(QPixmap.fromImage(image))

    def convolutionFilter(self,img):
        x0 = int(self.textEdit_0.toPlainText())
        x1 = int(self.textEdit_1.toPlainText())
        x2 = int(self.textEdit_2.toPlainText())
        x3 = int(self.textEdit_3.toPlainText())
        x4 = int(self.textEdit_4.toPlainText())
        x5 = int(self.textEdit_5.toPlainText())
        x6 = int(self.textEdit_6.toPlainText())
        x7 = int(self.textEdit_7.toPlainText())
        x8 = int(self.textEdit_8.toPlainText())


        
        filter_kernel  = np.array([[x0,x1,x2],
                                  [x3,x4,x5],
                                  [x6,x7,x8]])

        filtered_image = cv2.filter2D(img, -1, filter_kernel)
  
        return filtered_image

    def gaussianBlurr(self, img):
        blurred_image = cv2.GaussianBlur(img, (3, 3), 0)
        return blurred_image

    def update (self):
        """ This function will update the photo according to the
            with filter Matrix
        """
        self.old_image = self.image.copy()
        img = self.image
        if(self.filterTabs.currentWidget() == self.convolutionFilterTab):
            img = self.convolutionFilter(self.image)
        elif(self.filterTabs.currentWidget() == self.gaussianFilterTab):
            img = self.gaussianBlurr(self.image)
        self.image = img.copy()    
        self.setPhoto(img)
        
    def reset(self):
        print("reset")
        self.image = self.old_image
        self.setPhoto(self.old_image)
        
    def savePhoto (self):
        """ This function will save the image

        """

        filename = QFileDialog.getSaveFileName (filter="JPG (*.jpg);;PNG (*.png);;TIFF (*.tiff);;BMP (*.bmp)")[0]
        cv2.imwrite (filename,self.tmp)
        print ('Image saved as:',self.filename)
        
class GuiMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(GuiMainWindow, self).__init__(parent)

        self.setGeometry(100, 100, 877, 712)

        self.setWindowTitle('Image View')

        self.centralWidget = Image_View(self)
        self.centralWidget.setObjectName("centralwidget")

        self.setCentralWidget(self.centralWidget)

        openAction = QAction(QIcon('open.png'),'&Open',self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.centralWidget.loadImage)
        
        saveAction = QAction(QIcon('save.png'),'&Save',self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.centralWidget.savePhoto)

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

    def closeEvent(self, event):
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = GuiMainWindow()
    main_window.show()
       
    sys.exit(app.exec_())
    
