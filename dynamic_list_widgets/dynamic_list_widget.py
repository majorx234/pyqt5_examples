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
        self.applyButton.clicked.connect(self.apply_filter)
         
    def closeEvent(self, event):
            event.accept()

    def addImage(self, filename):
        image_item = ImageItem()
        image_item.set_image_from_filename(filename)
        image = image_item.get_image()
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.my_model.append(image_item)

    def apply_filter(self,event=None):
        last_item = self.my_model.get_last_item()
        last_image = last_item.get_image()
        # todo: filter geshizzle
        filtered_image = QImage(last_image)
        image_item = ImageItem()
        image_item.set_image(filtered_image)

        self.imageLabel.setPixmap(QPixmap.fromImage(filtered_image))
        self.my_model.append(image_item)

