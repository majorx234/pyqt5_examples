import numpy as np
import cv2
import image_filter as ft

def draw_rectangle_in_image(cv_image,rectangle_list):
    if(len(rectangle_list) !=0):
        for (x, y, w, h) in rectangle_list:
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
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
    
