import cv2
import numpy as np

def normalizeImage(cv_img, selected_norm):
    rows = cv_img.shape[0]
    cols = cv_img.shape[1]
    normalizedImg = np.zeros((rows, cols))
    if(selected_norm == 'MinMax'):
        normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 255, cv2.NORM_MINMAX)
        print(selected_norm)
    elif(selected_norm == 'INF'):
        print(selected_norm)
        normalizedImg2 = cv2.normalize(cv_img,  normalizedImg, 0, 1, cv2.NORM_INF, dtype=cv2.CV_32F)
        normalizedImg2 *=255
        normalizedImg = np.uint8(normalizedImg2)
    elif(selected_norm == 'L1'):
        normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 1, cv2.NORM_L1, dtype=cv2.CV_32F)
    elif(selected_norm == 'L2'):
        normalizedImg = cv2.normalize(cv_img,  normalizedImg, 0, 1, cv2.NORM_L2, dtype=cv2.CV_32F)
    return normalizedImg

def convolutionFilter(cv_img, filter_kernel): 
    filtered_image = cv2.filter2D(cv_img, -1, filter_kernel)
    return filtered_image    
 
def gaussianBlurr(cv_img):
    blurred_image = cv2.GaussianBlur(cv_img, (3, 3), 0)
    return blurred_image

def greyscale(cv_img):
    return cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

def threshold(cv_img, min, max):
    r, thresh_img = cv2.threshold(cv_img, min, max, cv2.THRESH_BINARY)
    return thresh_img

def erosion(cv_img):
    kernel = np.ones((5,5), np.uint8)
    return cv2.erode(cv_img, kernel)

def dilation(cv_img):
    kernel = np.ones((5,5), np.uint8)
    return cv2.dilate(cv_img, kernel)

def morphologicalGradient(cv_img):
    kernel = np.ones((5,5), np.uint8)
    return cv2.morphologyEx(cv_img, cv2.MORPH_GRADIENT, kernel)
 
