import os
import cv2
import fnmatch

def load_image_from_folder(image_folder='./', process_func=None,filename_filter="*",extention= ('.bmp', '.png'),cvtColor_code=cv2.COLOR_BGR2RGB):
    files = os.listdir(image_folder)
    image_list = []
    files = fnmatch.filter(files, filename_filter)
    for file in files:
        if file.endswith(extention):
            image = cv2.imread(image_folder + file)
            image = cv2.cvtColor(image, cvtColor_code)
            image_list.append(image)
            if process_func is not None:
                process_func(image)
        else:
            continue

    return image_list

