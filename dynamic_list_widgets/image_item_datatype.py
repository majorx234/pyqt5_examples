from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QImage

class ImageItem(QObject):
    data_changed = pyqtSignal(QObject)
    def __init__(self, *args):
        super().__init__(*args)
        self.image = None
        self.thumbnail = None

    def set_image(self, image):
        self.image = image
        self.thumbnail = self.image.scaleToWidth(thumb_width, mode=Qt.SmoothTransformation)
        self.data_changed.emit(self)
        
    def set_image_from_filename(self, filename, thumb_width=128):
        self.image = QImage(filename)
        self.thumbnail = self.image.scaledToWidth(thumb_width, mode=Qt.SmoothTransformation)
        self.data_changed.emit(self)

    def get_image(self):
        return self.img

    def select(self):
        self.selected.emit(self)
