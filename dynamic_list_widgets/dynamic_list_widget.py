from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QMetaObject
from image_list_model import ImageListModel
import sys

from ui_dynamic_list_widget import Ui_dynamic_list_widget

class DynamicListWidget(QWidget, Ui_dynamic_list_widget):
    def __init__(self, parent=None):
        super(QWidget,self).__init__(parent)
        self.setupUi(parent)

        my_model = ImageListModel()
        self.listView.setModel(my_model)
        #dem lsit view sagen dass er das model hat
        #self.listView

        #später  self.listView seine delegates geben
         
    def closeEvent(self, event):
            event.accept()
                 
