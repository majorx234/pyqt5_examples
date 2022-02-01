import os
import sys
import signal
import cv2
import cv_utils as cu
import image_filter as ft

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)

    if len(sys.argv) != 3:
        print("usage: create_faces_catalog.py <base_path>")
        sys.exit(1)

    BASE_PATH=sys.argv[1]
    DST_PATH=sys.argv[2]
    SEPARATOR=";"

    label = 0
    pathlist = []
    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            #create subdirpath in dst_path
            dst_subdir_path = os.path.join(DST_PATH,subdirname)
            if not os.path.exists(dst_subdir_path):
                os.makedirs(dst_subdir_path) 
            print(dst_subdir_path)
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path_original = "{}/{}".format(subject_path, filename)
                abs_path_normalized = "{}/{}".format(dst_subdir_path, filename)
                path_to_original_file = "{}".format(abs_path_original) #SEPARATOR)
                path_to_normalized_file = "{}".format(abs_path_normalized) #, SEPARATOR)
                pathlist.append((path_to_original_file, path_to_normalized_file,label))
            label = label + 1

    # ab hier haben wir liste von Bildern +label
    # wir wollen aber liste von normaliierten bildern +label in csv

    # kleine schleife
    # path1,label -> path2,label
    # path1 is normalbild
    # path2 normalisiert gedreht an augen ausgerichtet
    for image_path_to_original,image_path_to_normalized,label in pathlist:
        original_image = cv2.imread(image_path_to_original)
        #do some stuff with orginal image

        # greyscale
        grey_scale_image = ft.greyscale(original_image)

        # normalize
        normalized_image = ft.normalizeImage(grey_scale_image,'MinMax')
        
        # 2x cv2.Rect <- eye detection
        # (x,y,w,h) -> mittelpunkt? (x+(w/2), y+(h/2)) (richtiger links und recht)
        # p1(x1,y1) , p2(x2,y2) x1<x2 damit p1 links und p2 rechts

        eyes = ft.haarcascade_eyes_detection(normalized_image)
        print(eyes)
        how_much_eyes = len(eyes)
        print(how_much_eyes)
    #    assert(how_much_eyes == 2)
        # ausgabe zu viele oder zuwenig Augen
        left_eye = eyes[0]
        right_eye = eyes[1]
        if(eyes[0][0] > eyes[1][0]):
            left_eye = eyes[1]
            right_eye = eyes[0]

        (lx, ly, lw, lh) = left_eye
        (rx, ry, rw, rh) = right_eye

        lmx = lx+lw/2.0
        lmy = ly+lw/2.0
        rmx = rx+rw/2.0
        rmy = ry+rh/2.0

        croped_image = cu.CropFace(normalized_image, eye_left=(lmx,lmy), eye_right=(rmx,rmy), offset_pct=(0.3,0.3), dest_sz = (200,200))

        print("{}, {}".format(image_path_to_original, image_path_to_normalized))
        cv2.imwrite(image_path_to_normalized, croped_image)
