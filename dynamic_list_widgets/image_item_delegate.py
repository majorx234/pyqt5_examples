from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QPen, QBrush, QPainter, QColor, QMouseEvent

from image_item_datatype import ImageItem

class ImageItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, *args):
        super().__init__(*args)
        self.setParent(parent)
    def sizeHint(self,style_option_view_item, model_index):
        model_index_data = model_index.data()
        midtype = type(model_index_data)
        if midtype is ImageItem:
            return QSize(model_index_data.get_thumbnail().width(),model_index_data.get_thumbnail().height())
        else:
            return super().sizeHint(style_option_view_item,model_index)

    def paint(self, qp, style_option_view_item, model_index):
        model_index_data = model_index.data()
        if type(model_index_data) == ImageItem:
            qp.save()
            qp.drawImage(style_option_view_item.rect.left() + 4, style_option_view_item.rect.top() , model_index_data.get_thumbnail())
            qp.restore()
        else:
            super().paint(qp, style_option_view_item, model_index)
