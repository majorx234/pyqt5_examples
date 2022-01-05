from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QMetaObject
from image_list_model import ImageListModel
from image_item_datatype import ImageItem
from image_item_delegate import ImageItemDelegate
import sys
import numpy as np
import cv2
from cv_to_qt import cv_to_qt_image
import pyqtgraph as pg

from ui_dynamic_list_widget import Ui_dynamic_list_widget

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
        self.selectedFacesListView.setItemDelegate(self.selectedFacesListDelegate)
        self.selectedFacesListView.setModel(self.selectedFacesListModel)

        self.historyListDelegate.on_clicked.connect(self.selectImageFromList)
        self.applyButton.clicked.connect(self.apply_filter)
        self.resetButton.clicked.connect(self.reset)
        self.imageLabel.mousePressEvent = self.getPos
        self.current_faces = []
        self.current_image = None
    def closeEvent(self, event):
            event.accept()

    def saveImage(self):
        """ This function will save the image

        """
        last_item = self.historyListModel.get_last_item()
        last_image = last_item.get_image()
        filename = "test.jpg"
        filename = QFileDialog.getSaveFileName (filter="JPG (*.jpg);;PNG (*.png);;TIFF (*.tiff);;BMP (*.bmp)")[0]
        cv2.imwrite(filename, last_image)
        print ('Image saved as:', filename)

            
    def setMainImage(self, cv_image):
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
        image_item = ImageItem()
        image_item.set_image_from_filename(filename)
        image = image_item.get_image()
         
        self.setMainImage(image)
        self.historyListModel.append(image_item)
        
    def reset(self):
        penultimate_item = self.historyListModel.get_penultimate_item()
        penultimate_image = penultimate_item.get_image()
        penultimate_image_copy = penultimate_image.copy()
         
        image_item = ImageItem()
        image_item.set_image(penultimate_image_copy)
        self.setMainImage(penultimate_image_copy)
        self.historyListModel.append(image_item)

    def selectImageFromList(self, index, mouse_button):
        indexed_item = self.historyListModel.get_item(index)
        indexed_image = indexed_item.get_image()
       
        image_item = ImageItem()
        image_item.set_image(indexed_image.copy())
        self.setMainImage(indexed_image)
        self.historyListModel.append(image_item)
        
    def apply_filter(self,event=None):
        last_item = self.historyListModel.get_last_item()
        last_image = last_item.get_image()
        print(type(last_image))
        filtered_image = last_image.copy()

        if(self.filterTabs.currentWidget() == self.normalizeTab):
            filtered_image = self.normalizeImage(last_image)
        if(self.filterTabs.currentWidget() == self.convolutionFilterTab):
            filtered_image = self.convolutionFilter(last_image)
        elif(self.filterTabs.currentWidget() == self.gaussianFilterTab):
            filtered_image = self.gaussianBlurr(last_image)
        elif(self.filterTabs.currentWidget() == self.greyscaleTab):
            filtered_image = self.greyscale(last_image)
        elif(self.filterTabs.currentWidget() == self.thresholdTab):
            filtered_image = self.threshold(last_image,150,255)
        elif(self.filterTabs.currentWidget() == self.erosionTab):
            filtered_image = self.erosion(last_image)
        elif(self.filterTabs.currentWidget() == self.dilationTab):
            filtered_image =  self.dilation(last_image)
        elif(self.filterTabs.currentWidget() == self.morphologicalGradientTab):
            filtered_image = self.morphologicalGradient(last_image)
        elif(self.filterTabs.currentWidget() == self.facedetectionTab):
            filtered_image = self.haarcascade_face_detection(last_image)

        image_item = ImageItem()
        image_item.set_image(filtered_image)
        self.setMainImage(filtered_image)
        self.historyListModel.append(image_item)
        
    def normalizeImage(self,cv_img):
        selected_norm = self.normCombobox.currentText()
        rows = cv_img.shape[0]
        cols = cv_img.shape[1]
        normalizedImg = np.zeros((rows, cols))
        if(selected_norm == 'MinMax'):
            normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 255, cv2.NORM_MINMAX)
            print(selected_norm)
        elif(selected_norm == 'INF'):
            print(selected_norm)
            normalizedImg2 = cv2.normalize(cv_img,  normalizedImg, 0, 1, cv2.NORM_INF, dtype=cv2.CV_32F)
            normalizedImg2 *=255
            normalizedImg = np.uint8(normalizedImg2)
        elif(selected_norm == 'L1'):
            normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 1, cv2.NORM_L1, dtype=cv2.CV_32F)
        elif(selected_norm == 'L2'):
            normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 1, cv2.NORM_L2, dtype=cv2.CV_32F)
        return normalizedImg
    
    def convolutionFilter(self, cv_img):
        x0 = float(self.textEdit_0.toPlainText())
        x1 = float(self.textEdit_1.toPlainText())
        x2 = float(self.textEdit_2.toPlainText())
        x3 = float(self.textEdit_3.toPlainText())
        x4 = float(self.textEdit_4.toPlainText())
        x5 = float(self.textEdit_5.toPlainText())
        x6 = float(self.textEdit_6.toPlainText())
        x7 = float(self.textEdit_7.toPlainText())
        x8 = float(self.textEdit_8.toPlainText())
        
        filter_kernel  = np.array([[x0,x1,x2],
                                  [x3,x4,x5],
                                  [x6,x7,x8]])

        filtered_image = cv2.filter2D(cv_img, -1, filter_kernel)
        return filtered_image    

    def gaussianBlurr(self, cv_img):
        blurred_image = cv2.GaussianBlur(cv_img, (3, 3), 0)
        return blurred_image

    def greyscale(self,cv_img):
        return cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    def threshold(self, cv_img, min, max):
        r, grey_img = cv2.threshold(cv_img, min, max, cv2.THRESH_BINARY)
        return grey_img

    def erosion(self, cv_img):
        kernel = np.ones((5,5), np.uint8)
        return cv2.erode(cv_img, kernel)

    def dilation(self, cv_img):
        kernel = np.ones((5,5), np.uint8)
        return cv2.dilate(cv_img, kernel)

    def morphologicalGradient(self, cv_img):
        kernel = np.ones((5,5), np.uint8)
        return cv2.morphologyEx(cv_img, cv2.MORPH_GRADIENT, kernel)

    def histogram(self, cv_img):
        # create greyscale image if needed:
        grey_img = cv_img
        if len(cv_img.shape) == 3:
            grey_img = self.greyscale(cv_img)
        #pixelgenau zugriff
        rows, cols = grey_img.shape
        histogram = np.zeros(256)
        for i in range(rows):
            for j in range(cols):
                k = grey_img[i,j]
                histogram[k] += 1
        return histogram

    def haarcascade_face_detection(self,cv_img):
        xml_cascade_file = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
        # detect face
        face_cascade = cv2.CascadeClassifier(xml_cascade_file)
        faces = face_cascade.detectMultiScale(cv_img)
        faces_img = cv_img.copy()
        self.current_faces = faces
        #mark faces in image
        for (x, y, w, h) in faces:
            cv2.rectangle(faces_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        self.current_image = faces_img.copy()    
        return faces_img

    def getPos(self, event):
        p_x = event.pos().x()
        p_y = event.pos().y()
        cv_img = self.current_image
        if(len(self.current_faces)>0):
            for (x, y, w, h) in self.current_faces:
                if(p_y > y) and (p_y < y +h) and (p_x > x) and (p_x < x+w):
                    face_image = cv_img[y:y+h, x:x+w]
                    image_item = ImageItem()
                    image_item.set_image(face_image)
                    self.selectedFacesListModel.append(image_item)
