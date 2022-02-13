#!/usr/bin/env python3

import sys
import os.path
import shutil

def foo(folderpath_one, folderpath_two):
    print("folder 1: {} folder 2: {}".format(folderpath_one, folderpath_two))
    max_num = 0
    for filename in os.listdir(folderpath_one):
        split_name = filename.split(".")
        num_file = int(split_name[0])
        if num_file > max_num:
            max_num = num_file

    for filename_old in os.listdir(folderpath_two):
        max_num += 1
        filename_path_old = "{}/{}".format(folderpath_two, filename_old)
        filename_path_new = "{}/{}.jpg".format(folderpath_one, max_num)
        print("cp {} {}".format(filename_path_old, filename_path_new))
        shutil.move(filename_path_old, filename_path_new)
    os.rmdir(folderpath_two)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: tell me folderpath <folder_path>")
        sys.exit(1)

    FOLDER_PATH_ONE=sys.argv[1]
    FOLDER_PATH_TWO=sys.argv[2]

    foo(FOLDER_PATH_ONE, FOLDER_PATH_TWO)




