from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QImage
import cv2, imutils

class ImageItem(QObject):
    data_changed = pyqtSignal(QObject)
    def __init__(self, *args):
        super().__init__(*args)
        self.cv_image = None
        self.cv_thumbnail = None
        self.thumb_width = 128

    def set_image(self, image):
        self.cv_image = image
        self.cv_thumbnail = imutils.resize(self.cv_image, width=self.thumb_width)
        self.data_changed.emit(self)
        
    def set_image_from_filename(self, filename):
        self.set_image(cv2.imread(filename))


    def get_image(self):
        return self.cv_image

    def select(self):
        self.selected.emit(self)

    def get_thumbnail(self):
        return self.cv_thumbnail
    
