from PyQt5.QtGui import QImage
import cv2
import numpy as np

def cv_to_qt_image(cv_img):
    #check if monocrm or RGB
    frame = None
    qt_img = QImage()
    if(cv_img.dtype == np.uint8):
        if len(cv_img.shape) == 2:
            qt_img = QImage(cv_img.data , cv_img.shape[1], cv_img.shape[0],cv_img.strides[0],QImage.Format_Grayscale8)
        else:
            frame = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            qt_img = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
    return qt_img

