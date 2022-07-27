import fnmatch
import glob
import ntpath
import os
from datetime import datetime
from pathlib import Path

import cv2
from colorama import Fore, Style

from colorspace import segment


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def load_image_names_from_folder(image_folder="./", filename_filter="*"):
    image_filepath_list = glob.glob(image_folder + "/" + filename_filter + '*')
    print(("{}{}{} files found from{}{}{} wtih filter {}'{}'{}").format(Fore.GREEN, len(image_filepath_list),
                                                                        Style.RESET_ALL,
                                                                        Fore.GREEN, image_folder, Style.RESET_ALL,
                                                                        Fore.GREEN, filename_filter, Style.RESET_ALL))
    return image_filepath_list


def load_images_by_images_path(images_path, cvtColor_code=cv2.COLOR_BGR2RGB):
    images = []
    start_time = datetime.now()
    for image_path in images_path:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cvtColor_code)
        images.append(image)
    end_time = datetime.now()
    duration = end_time - start_time
    print("Loading images count {}{}{} duration: {}{}{}".format(Fore.GREEN, len(images), Style.RESET_ALL,
                                                                Fore.GREEN, duration, Style.RESET_ALL))
    return images


def load_image_from_folder(image_folder='./', process_while_loading=True, filename_filter="*",
                           extention=('.bmp', '.png'), cvtColor_code=cv2.COLOR_BGR2RGB):
    files = os.listdir(image_folder)
    image_names_list = [];
    image_list = []
    mask_list = []
    files = fnmatch.filter(files, filename_filter)
    for file in files:
        if file.endswith(extention):
            image = cv2.imread(image_folder + file)
            image = cv2.cvtColor(image, cvtColor_code)
            image_list.append(image)
            if process_while_loading:
                masks = segment.threshold_by_colorspace(image)
                mask_list.append(segment.merge_mask_bitwise_or(masks))
                image_names_list.append(file)
        else:
            continue

    return image_list, mask_list, image_names_list


def extract_mask_from_image(image):
    masks = segment.threshold_by_colorspace(image)
    return segment.merge_mask_bitwise_or(masks)


def slice_by_grid(image, mask, slice_grid_row_column=[4, 6]):
    sliced_images = []
    sliced_masks = []
    h, w, _ = image.shape
    grid_h = h // slice_grid_row_column[0]
    grid_w = w // slice_grid_row_column[1]
    for i in range(slice_grid_row_column[0]):
        for j in range(slice_grid_row_column[1]):
            sliced_image = image[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w]
            sliced_mask = mask[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w]
            sliced_images.append(sliced_image)
            sliced_masks.append(sliced_mask)
    return sliced_images, sliced_masks


def slice_by_grid_batch(image_list, mask_list, slice_grid_row_column=[4, 6]):
    image_list_sliced = []
    mask_list_sliced = []
    for im in range(0, len(image_list)):
        image = image_list[im]
        mask = mask_list[im]
        sliced_images, sliced_masks = slice_by_grid(image, mask, slice_grid_row_column)
        image_list_sliced.append(sliced_images)
        mask_list_sliced.append(sliced_masks)
    return image_list_sliced, mask_list_sliced
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
def sliced_and_save_image(image,basic_info,save_path,main_image_name,save_mode=4,training_size=244):

    save_path=save_path+"/"+"sm"+str(save_mode)+"/"
    Path(save_path).mkdir(parents=True, exist_ok=True);
    main_image_name=main_image_name.split(".")[0]
    for i in range(len(basic_info)):
        if len(basic_info[i])>0:
            save_rect=basic_info[i][save_mode]
            e=basic_info[i][0]
            d=basic_info[i][1]
            c=basic_info[i][2]
            w=basic_info[i][3][2]
            h=basic_info[i][3][3]
            save_path_image = save_path + "/" + main_image_name +\
                              "_i" + str(i)  + \
                              "_e" + str(e)  + \
                              "_d" + str(d)  + \
                              "_c" + str(c)  + \
                              "_w" + str(w)  + \
                              "_h" + str(h)  + \
                              "_s" + str(save_mode)  + \
                              ".png"



            sliced_image = image[save_rect[1]:save_rect[1]+save_rect[3], save_rect[0]:save_rect[0]+save_rect[2]]
            if save_mode  == 3 or save_mode == 5:
                import numpy as np
                backimg = np.zeros([training_size,training_size,3],dtype=np.uint8)
                backimg.fill(255) # or img[:] = 255
                #if sliced_image size is bigger than backimg, resize it to fit backimg size proportionally
                if sliced_image.shape[0]>backimg.shape[0] :
                    sliced_image = image_resize(sliced_image,height=training_size)
                if sliced_image.shape[1]>backimg.shape[1] :
                    sliced_image= image_resize(sliced_image,width=training_size)


                #centre the sliced_image on the backimg
                x_offset = int((training_size - sliced_image.shape[1]) / 2)
                y_offset = int((training_size - sliced_image.shape[0]) / 2)
                backimg[y_offset:y_offset + sliced_image.shape[0], x_offset:x_offset + sliced_image.shape[1]] = sliced_image
                sliced_image = backimg

            cv2.imwrite(save_path_image, cv2.cvtColor(sliced_image,cv2.COLOR_BGR2RGB) )
            #print("saved to {}".format(save_path_image))

def save_images_by_images_path(to_be_saved_images, save_path, image_name_list,cvtColor=True):
    Path(save_path).mkdir(parents=True, exist_ok=True);
    for i in range(len(to_be_saved_images)):
        tail = path_leaf(image_name_list[i])
        save_path_image = save_path + "/" + tail
        if cvtColor:
            whole_image=cv2.cvtColor(to_be_saved_images[i],cv2.COLOR_BGR2RGB)
        else:
            whole_image=to_be_saved_images[i]

        cv2.imwrite(save_path_image, whole_image)
        #print("saved to {}".format(save_path_image))
    return None
