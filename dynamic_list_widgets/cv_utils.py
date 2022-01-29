import numpy as np
import cv2
import image_filter as ft

def scaledImageToConstrains(cv_image : np.ndarray, label_width, label_height ) -> (np.ndarray, float, float):
    image_height, image_width  = cv_image.shape[:2]
    ratio = image_width / image_height
    scaledFactorWidth = 1.0
    scaledFactorHeight = 1.0
    if ratio == 1 :
        dim = (label_width,label_width)
        resized_image = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)
        scaledFactorWidth = label_width/image_width
        scaledFactorHeight = label_height/image_height
    elif ratio < 1 :
        r = image_height / float(label_height)
        dim = (int(image_width/r),label_height)
        resized_image = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)
        scaledFactorHeight = label_height/image_height
        scaledFactorWidth = scaledFactorHeight
    else : #ratio > 1:
        r = image_width / float(label_width)
        dim = (label_width,int(image_height/r))
        resized_image = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)
        scaledFactorWidth = label_width/image_width
        scaledFactorHeight = scaledFactorWidth
    return resized_image, scaledFactorWidth, scaledFactorHeight

def draw_rectangle_in_image(cv_image,rectangle_list, color):
    if(len(rectangle_list) !=0):
        for (x, y, w, h) in rectangle_list:
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), color, 2)
    return cv_image

def histogram(cv_img):
        # create greyscale image if needed:
        grey_img = cv_img
        if len(cv_img.shape) == 3:
            grey_img = ft.greyscale(cv_img)
        #pixelgenau zugriff
        rows, cols = grey_img.shape
        histogram = np.zeros(256)
        for i in range(rows):
            for j in range(cols):
                k = grey_img[i,j]
                histogram[k] += 1
        return histogram

def cut_selecteced_rectangle_from_image(p_x, p_y, cv_image, rectangle_list):
    if(len(rectangle_list)>0):
            for (x, y, w, h) in rectangle_list:
                if(p_y > y) and (p_y < y +h) and (p_x > x) and (p_x < x+w):
                    return cv_image[y:y+h, x:x+w]
    
