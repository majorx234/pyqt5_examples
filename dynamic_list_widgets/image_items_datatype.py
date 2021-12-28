from PyQt5.QtCore import QObject
from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSignal

class ImageItems(QObject):
    def __init__(self, *args):
        super().__init__(args)
        self.image = None
        self.thumbnail = None

    def set_image(self, image):
        self.image = image
        self.thumbnail = self.image.scaleToWidth(thumb_width, mode=Qt.SmoothTransformation)
        
    def set_image_from_filename(self, filename, thumb_width=128):
        self.image = QImage(filename)
        self.thumbnail = self.image.scaleToWidth(thumb_width, mode=Qt.SmoothTransformation)

    def get_image(self):
        return self.img

    def select(self):
        self.selected.emit(self)
