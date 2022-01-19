from PyQt5.QtCore import Qt, QSize, QEvent, pyqtSignal, QTimer
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QPen, QBrush, QPainter, QColor, QMouseEvent

from image_item_datatype import ImageItem
from cv_to_qt import cv_to_qt_image

class ImageItemDelegate(QStyledItemDelegate):
    on_clicked = pyqtSignal(int, Qt.MouseButton)
    doubleClicked = pyqtSignal(int)
    def __init__(self, parent=None, *args):
        super().__init__(*args)
        self.setParent(parent)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        #self.timer.timeout.connect(self.on_clicked.emit)
        self.on_clicked.connect(self.checkDoubleClick)

    def checkDoubleClick(self, index, mouse_button):
        if self.timer.isActive():
            print("second")
            #if (self.timer<250):
            #    self.doubleClicked.emit(index)
            #    self.timer.stop()
            #else:
            #    self.timer.start()
        else:
            print("first")
            self.timer.start(250)
        
    def sizeHint(self,style_option_view_item, model_index):
        model_index_data = model_index.data()
        midtype = type(model_index_data)
        if midtype is ImageItem:
            cv_thumbnail = model_index_data.get_thumbnail()
            qt_thumbnail = cv_to_qt_image(cv_thumbnail)
            return QSize(qt_thumbnail.width(),qt_thumbnail.height())
        else:
            return super().sizeHint(style_option_view_item,model_index)

    def paint(self, qp, style_option_view_item, model_index):
        model_index_data = model_index.data()
        if type(model_index_data) == ImageItem:
            qp.save()
            cv_thumbnail = model_index_data.get_thumbnail()
            qt_thumbnail = cv_to_qt_image(cv_thumbnail)
            qp.drawImage(style_option_view_item.rect.left() + 4, style_option_view_item.rect.top() , qt_thumbnail )
            qp.restore()
        else:
            super().paint(qp, style_option_view_item, model_index)

    def editorEvent (self, event, model, option, model_index):
        if event.type() == QEvent.MouseButtonPress:
            mouse_button =  event.button()
            item_index = model_index.row()
            self.on_clicked.emit(item_index, mouse_button)
        return True     
