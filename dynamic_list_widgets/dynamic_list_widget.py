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
        super(QWidget,self).__init__(parent)
        self.setupUi(parent)

        self.my_model = ImageListModel()
        self.listView.setItemDelegate(ImageItemDelegate(parent = self.listView))
        self.listView.setModel(self.my_model)
        self.applyButton.clicked.connect(self.apply_filter)
         
    def closeEvent(self, event):
            event.accept()
            
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
        self.my_model.append(image_item)
        
    def reset(self):
        print("reset")
        self.image = self.old_image
        self.setPhoto(self.old_image)
    

    def apply_filter(self,event=None):
        last_item = self.my_model.get_last_item()
        last_image = last_item.get_image()
        # todo: filter geshizzle
        
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

        image_item = ImageItem()
        image_item.set_image(filtered_image)
        self.setMainImage(filtered_image)
        self.my_model.append(image_item)
        
    def normalizeImage(self,cv_img):
        rows = cv_img.shape[0]
        cols = cv_img.shape[1]
        normalizedImg = np.zeros((rows, cols))
        normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 255, cv2.NORM_MINMAX)
        #normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 255, cv2.NORM_INF)
        #normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 255, cv2.NORM_L1)
        #normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 255, cv2.NORM_L2)
 
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
        
