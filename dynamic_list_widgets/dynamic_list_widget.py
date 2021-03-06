import numpy as np
import cv2
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QEvent
from image_list_model import ImageListModel
from image_item_datatype import ImageItem
from image_item_delegate import ImageItemDelegate
from cv_to_qt import cv_to_qt_image
from ui_dynamic_list_widget import Ui_dynamic_list_widget
import image_filter as ft
import cv_utils as cu
from os.path import expanduser

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
        self.resetFacedetectionButton.clicked.connect(self.resetFacedetection)
        self.imageLabel.mousePressEvent = self.getFaceAtPos
        self.current_faces = []
        self.current_eyes  = []
        self.current_image = None
        self.selectedFacesListView.installEventFilter(self)

        self.imageOriginalWidth = 0
        self.imageOriginalHeight = 0
        self.scaleFactorWidth = 1.0
        self.scaleFactorHeight = 1.0
        self.labelWidth = 400
        self.labelHeight = 400
        
    def closeEvent(self, event):
            event.accept()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.selectedFacesListView:
            menu = QMenu(self)
            save_img = menu.addAction("Save")
            delete_img = menu.addAction("Delete")
            save_all_img = menu.addAction("SaveAll")
            menu_click = menu.exec(event.globalPos())
            model_index = 0
            try:
                model_index = self.selectedFacesListView.indexAt(event.pos())
            except Exception as e:
                print(f"No item selected {e}")

            if menu_click == save_img:
                print("Save")
                #model_index = self.selectedFacesListView.indexAt(event.pos())
                filename = QFileDialog.getSaveFileName (filter="JPG (*.jpg);;PNG (*.png);;TIFF (*.tiff);;BMP (*.bmp)")[0]
                cv2.imwrite(filename, model_index.data().get_image())
            elif menu_click == delete_img:
                print("Delete")
            elif menu_click == save_all_img:
                print("SaveAll")
                filepath = QFileDialog.getExistingDirectory(self, "Open Directory",
                                             expanduser("~"),
                                             QFileDialog.ShowDirsOnly)
                i = 0
                for item in self.selectedFacesListModel:
                    filename = filepath + "/" + str(i) + ".jpg"
                    image = item.get_image();
                    cv2.imwrite(filename,image)
                    i += 1
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
            
    def saveFaceImage(self,index):
        """This function will save a face image as file"""
        indexed_item = self.selectedFacesListModel.get_item(index)
        indexed_image = indexed_item.get_image()
        filename = QFileDialog.getSaveFileName (filter="JPG (*.jpg);;PNG (*.png);;TIFF (*.tiff);;BMP (*.bmp)")[0]
        cv2.imwrite(filename, indexed_image)
     
    def set_main_image(self, cv_image):
        (resized_cv_image, self.scaledFactorWidth, self.scaleFactorHeight) = cu.scaledImageToConstrains(cv_image, self.labelWidth, self.labelHeight)
        qt_image = cv_to_qt_image(resized_cv_image)
        self.imageLabel.setPixmap(QPixmap.fromImage(qt_image))
        (height, width,_) = cv_image.shape
        self.xValueLabel.setNum(width)
        self.yValueLabel.setNum(height)
        
        # histogram
        histogram_plot = pg.PlotWidget()
        y_axis = cu.histogram(cv_image)
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
            filtered_image = ft.morphologicalGradient(last_image)
        elif(self.filterTabs.currentWidget() == self.facedetectionTab):
            filtered_image = last_image
            (face_scale_factor, face_min_neighbors, face_min_size_x, face_min_size_y, face_max_size_x, face_max_size_y) = self.get_facedetect_params()
            self.current_faces = ft.haarcascade_face_detection(last_image,
                                                               face_scale_factor,
                                                               face_min_neighbors,
                                                               flags = 0,
                                                               min_size =(face_min_size_x, face_min_size_y),
                                                               max_size = (face_max_size_x, face_max_size_y))

            (eyes_scale_factor, eyes_min_neighbors, eyes_min_size_x, eyes_min_size_y, eyes_max_size_x, eyes_max_size_y) = self.get_eyesdetect_params()
            self.current_eyes = ft.haarcascade_eyes_detection(last_image,
                                                              eyes_scale_factor,
                                                              eyes_min_neighbors,
                                                              flags = 0,
                                                              min_size = (eyes_min_size_x, eyes_min_size_y),
                                                              max_size = (eyes_max_size_x, eyes_max_size_y))
            print(self.current_faces)
            print(self.current_eyes)

        image_item = ImageItem(thumb_width=128)
        image_item.set_image(filtered_image)
        self.historyListModel.append(image_item)
        
        self.current_image = filtered_image
        #draw faces in label
        face_color = (0, 0, 255)
        face_image = cu.draw_rectangle_in_image(filtered_image.copy(), self.current_faces, face_color)
        eyes_color = (255, 0, 0)
        self.set_main_image(cu.draw_rectangle_in_image(face_image, self.current_eyes, eyes_color))
        
    def getFaceAtPos(self, event):
        #doofer Name, splitten in Pos Methode und in Methode die wenn in Gesicht geklickt in Liste tun  
        label_x = event.pos().x()
        label_y = event.pos().y()

        p_x = label_x / self.scaledFactorWidth
        p_y = label_y / self.scaleFactorHeight

        cv_img = self.current_image

        image_item = ImageItem(thumb_width=64)
        face_image = cu.cut_selecteced_rectangle_from_image(p_x, p_y, cv_img, self.current_faces)
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

    def get_facedetect_params(self):
        scale_factor  = float(self.scaleFactorTextEdit.toPlainText())
        min_neighbors = int(self.minNeighborsTextEdit.toPlainText())
        min_size_x    = int(self.minSizeXTextEdit.toPlainText())
        min_size_y    = int(self.minSizeYTextEdit.toPlainText())
        max_size_x    = int(self.maxSizeXTextEdit.toPlainText())
        max_size_y    = int(self.maxSizeYTextEdit.toPlainText())

        return (scale_factor, min_neighbors,
                min_size_x, min_size_y,
                max_size_x, max_size_y)

    def get_eyesdetect_params(self):
        scale_factor  = float(self.scaleFactorTextEdit_2.toPlainText())
        min_neighbors = int(self.minNeighborsTextEdit_2.toPlainText())
        min_size_x    = int(self.minSizeXTextEdit_2.toPlainText())
        min_size_y    = int(self.minSizeYTextEdit_2.toPlainText())
        max_size_x    = int(self.maxSizeXTextEdit_2.toPlainText())
        max_size_y    = int(self.maxSizeYTextEdit_2.toPlainText())

        return (scale_factor, min_neighbors,
                min_size_x, min_size_y,
                max_size_x, max_size_y)
