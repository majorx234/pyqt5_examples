import os
import sys
import signal
import cv2

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
        normalized_image = original_image
        print("{}, {}".format(image_path_to_original, image_path_to_normalized))
        cv2.imwrite(image_path_to_normalized, normalized_image)
