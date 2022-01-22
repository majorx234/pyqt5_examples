import numpy as np
import cv2
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QMetaObject, QEvent
from image_list_model import ImageListModel
from image_item_datatype import ImageItem
from image_item_delegate import ImageItemDelegate
from cv_to_qt import cv_to_qt_image
from ui_dynamic_list_widget import Ui_dynamic_list_widget
import image_filter as ft

class DynamicListWidget(QWidget, Ui_dynamic_list_widget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(parent)

        self.historyListModel = ImageListModel()
        self.historyListDelegate = ImageItemDelegate(parent = self.historyListView)
        self.historyListView.setItemDelegate(self.historyListDelegate)
        self.historyListView.setModel(self.historyListModel)

        self.selectedFacesListModel = ImageListModel()
        self.selectedFacesListDelegate = ImageItemDelegate(parent = self.selectedFacesListView)
        self.selectedFacesListDelegate.doubleClicked.connect(self.whoDoubleclicked)
        self.selectedFacesListView.setItemDelegate(self.selectedFacesListDelegate)
        self.selectedFacesListView.setModel(self.selectedFacesListModel)

        self.historyListDelegate.on_clicked.connect(self.selectImageFromList)
        self.applyButton.clicked.connect(self.apply_filter)
        self.resetButton.clicked.connect(self.reset)
        self.resetFacedetectionButton.clicked.connect(self.resetFacedetection)
        self.imageLabel.mousePressEvent = self.getPos
        self.current_faces = []
        self.current_image = None
        self.selectedFacesListView.installEventFilter(self)

    def whoDoubleclicked(self, index):
        print("doubleclicked {}".format(index))
        
    def closeEvent(self, event):
            event.accept()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.selectedFacesListView:
            menu = QMenu(self)
            menu.addAction("New")
            menu.addAction("Open")

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
                return True
        return super().eventFilter(source, event)
 

    def saveImage(self):
        """ This function will save the image

        """
        last_item = self.historyListModel.get_last_item()
        last_image = last_item.get_image()
        filename = "test.jpg"
        filename = QFileDialog.getSaveFileName (filter="JPG (*.jpg);;PNG (*.png);;TIFF (*.tiff);;BMP (*.bmp)")[0]
        cv2.imwrite(filename, last_image)
        print ('Image saved as:', filename)

    def selectFaceFromList(self, index, mouse_button):
        print("i do nothing yet")
        #if(mouse_button == ):
            #create contextmenu
            #saveFaceImage
            
    def saveFaceImage(self,index):
        indexed_item = self.selectedFacesListModel.get_item(index)
        indexed_image = indexed_item.get_image()
        filename = QFileDialog.getSaveFileName (filter="JPG (*.jpg);;PNG (*.png);;TIFF (*.tiff);;BMP (*.bmp)")[0]
        cv2.imwrite(filename, indexed_image)
     
    def set_main_image(self, cv_image):
        qt_image = cv_to_qt_image(cv_image)
        image_width = 400
        resized_image = qt_image.scaledToWidth(image_width, mode=Qt.SmoothTransformation)
        self.imageLabel.setPixmap(QPixmap.fromImage(resized_image))

        # histogram
        histogram_plot = pg.PlotWidget()
        y_axis = self.histogram(cv_image)
        x_axis = [x for x in range(255)]
        bargraph = pg.BarGraphItem(x = x_axis, height = y_axis, width = 1, pen ='g')
        histogram_plot.addItem(bargraph)
        self.histogramLayout.addWidget(histogram_plot,0,0)
       
    def addImage(self, filename):
        image_item = ImageItem(thumb_width=128)
        image_item.set_image_from_filename(filename)
        image = image_item.get_image()
         
        self.set_main_image(image)
        self.historyListModel.append(image_item)
        
    def reset(self):
        penultimate_item = self.historyListModel.get_penultimate_item()
        penultimate_image = penultimate_item.get_image()
        penultimate_image_copy = penultimate_image.copy()
         
        image_item = ImageItem(thumb_width=128)
        image_item.set_image(penultimate_image_copy)
        self.set_main_image(penultimate_image_copy)
        self.historyListModel.append(image_item)

    def resetFacedetection(self):
        self.set_main_image(self.current_image)
        self.current_faces = []

    def selectImageFromList(self, index, mouse_button):
        indexed_item = self.historyListModel.get_item(index)
        indexed_image = indexed_item.get_image()
       
        image_item = ImageItem(thumb_width=128)
        image_item.set_image(indexed_image.copy())
        self.set_main_image(indexed_image)
        self.historyListModel.append(image_item)
        
    def apply_filter(self,event=None):
        last_item = self.historyListModel.get_last_item()
        last_image = last_item.get_image()
        print(type(last_image))
        filtered_image = last_image.copy()

        if(self.filterTabs.currentWidget() == self.normalizeTab):
            selected_norm = self.get_selected_norm()
            filtered_image = ft.normalizeImage(last_image, selected_norm)
        if(self.filterTabs.currentWidget() == self.convolutionFilterTab):          
            filter_kernel = self.get_convolution_kernel()
            filtered_image = ft.convolutionFilter(last_image, filter_kernel)
        elif(self.filterTabs.currentWidget() == self.gaussianFilterTab):
            filtered_image = ft.gaussianBlurr(last_image)
        elif(self.filterTabs.currentWidget() == self.greyscaleTab):
            filtered_image = ft.greyscale(last_image)
        elif(self.filterTabs.currentWidget() == self.thresholdTab):
            filtered_image = ft.threshold(last_image,150,255)
        elif(self.filterTabs.currentWidget() == self.erosionTab):
            filtered_image = ft.erosion(last_image)
        elif(self.filterTabs.currentWidget() == self.dilationTab):
            filtered_image =  ft.dilation(last_image)
        elif(self.filterTabs.currentWidget() == self.morphologicalGradientTab):
            filtered_image = self.morphologicalGradient(last_image)
        elif(self.filterTabs.currentWidget() == self.facedetectionTab):
            filtered_image = last_image
            self.current_faces = self.haarcascade_face_detection(last_image)

        image_item = ImageItem(thumb_width=128)
        image_item.set_image(filtered_image)
        self.historyListModel.append(image_item)
        
        self.current_image = filtered_image
        #draw faces in label
        if(len(self.current_faces) !=0):
            faces_img = last_image.copy()
            #mark faces in image
            for (x, y, w, h) in self.current_faces:
                cv2.rectangle(faces_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            filtered_image = faces_img    
       
        self.set_main_image(filtered_image)
        
    def histogram(self, cv_img):
        # create greyscale image if needed:
        grey_img = cv_img
        if len(cv_img.shape) == 3:
            grey_img = ft.greyscale(cv_img)
        #pixelgenau zugriff
        rows, cols = grey_img.shape
        histogram = np.zeros(256)
        for i in range(rows):
            for j in range(cols):
                k = grey_img[i,j]
                histogram[k] += 1
        return histogram

    def haarcascade_face_detection(self, cv_img):
        xml_cascade_file = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
        # detect face
        face_cascade = cv2.CascadeClassifier(xml_cascade_file)
        faces = face_cascade.detectMultiScale(cv_img)
        return faces

    def getPos(self, event):
        p_x = event.pos().x()
        p_y = event.pos().y()
        cv_img = self.current_image
        if(len(self.current_faces)>0):
            for (x, y, w, h) in self.current_faces:
                if(p_y > y) and (p_y < y +h) and (p_x > x) and (p_x < x+w):
                    face_image = cv_img[y:y+h, x:x+w]
                    image_item = ImageItem(thumb_width=64)
                    image_item.set_image(face_image)
                    self.selectedFacesListModel.append(image_item)

    def get_selected_norm(self):
        return self.normCombobox.currentText()

    def get_convolution_kernel(self):
        x0 = float(self.textEdit_0.toPlainText())
        x1 = float(self.textEdit_1.toPlainText())
        x2 = float(self.textEdit_2.toPlainText())
        x3 = float(self.textEdit_3.toPlainText())
        x4 = float(self.textEdit_4.toPlainText())
        x5 = float(self.textEdit_5.toPlainText())
        x6 = float(self.textEdit_6.toPlainText())
        x7 = float(self.textEdit_7.toPlainText())
        x8 = float(self.textEdit_8.toPlainText())

        return np.array([[x0,x1,x2],
                        [x3,x4,x5],
                        [x6,x7,x8]])

    
