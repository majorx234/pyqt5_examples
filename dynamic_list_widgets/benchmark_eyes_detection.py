#!/bin/python
import sys,os
import image_filter as ft
import cv2

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: create_csv <base_path>")
        sys.exit(1)
        
    BASE_PATH=sys.argv[1]
    imagecount = 0
    failcount = 0
    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                image = cv2.imread(abs_path)
                
                eyes = ft.haarcascade_eyes_detection(image, 1.2, 3, 0,(22,22),(50,50))
                length = len(eyes)
                if(length != 2):
                    print("{} detected in {}".format(length, abs_path))
                    failcount += 1
                imagecount += 1
    print("all: {} fail: {}".format(imagecount,failcount))                

