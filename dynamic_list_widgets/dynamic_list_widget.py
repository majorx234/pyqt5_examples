from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QMetaObject
from image_list_model import ImageListModel
from image_item_datatype import ImageItem
from image_item_delegate import ImageItemDelegate
import sys

from ui_dynamic_list_widget import Ui_dynamic_list_widget

class DynamicListWidget(QWidget, Ui_dynamic_list_widget):
    def __init__(self, parent=None):
        super(QWidget,self).__init__(parent)
        self.setupUi(parent)

        self.my_model = ImageListModel()
        self.listView.setItemDelegate(ImageItemDelegate(parent = self.listView))

        self.listView.setModel(self.my_model)
        #dem lsit view sagen dass er das model hat
        #self.listView

        #später  self.listView seine delegates geben
         
    def closeEvent(self, event):
            event.accept()

    def addImage(self, filename):
        image_item = ImageItem()
        image_item.set_image_from_filename(filename)
        self.my_model.append(image_item)
