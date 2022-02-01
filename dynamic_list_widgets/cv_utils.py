import numpy as np
import math
from PIL import Image
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
    
def Distance(p1,p2):
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]
  return math.sqrt(dx*dx+dy*dy)

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=cv2.INTER_CUBIC):
  if (scale is None) and (center is None):
    return image.rotate(angle=angle, resample=resample)
  nx,ny = x,y = center
  sx=sy=1.0
  if new_center:
    (nx,ny) = new_center
  if scale:
    (sx,sy) = (scale, scale)
  cosine = math.cos(angle)
  sine = math.sin(angle)
  a = cosine/sx
  b = sine/sx
  c = x-nx*a-ny*b
  d = -sine/sy
  e = cosine/sy
  f = y-nx*d-ny*e
  return image.transform(image.size, cv2.AFFINE, (a,b,c,d,e,f), resample=resample)

#offset_pct=(0.3,0.3), dest_sz=(168,192)
def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (70,70)):
  # calculate offsets in original image
  offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
  offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
  # get the direction
  eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  # calc rotation angle in radians
  rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  # distance between them
  dist = Distance(eye_left, eye_right)
  # calculate the reference eye-width
  reference = dest_sz[0] - 2.0*offset_h
  # scale factor
  scale = float(dist)/float(reference)
  # rotate original around the left eye
  image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
  # crop the rotated image
  crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
  image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
  # resize it
  image = image.resize(dest_sz, cv2.ANTIALIAS)
  return image
