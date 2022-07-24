from datetime import datetime
import os
import cv2
import numpy as np
from colorama import Fore, Style  # color coding print

from colorspace import segment
from features import basic
from morph import morph
from util import io
from util.args_setup import picture_loading_arg_process


def for_each_mask_find_countour_rect(single_restored_sized_mask, columns=6, rows=4):
    contours = basic.find_contours(single_restored_sized_mask)
    contours_rects = [cv2.boundingRect(contour) for contour in contours]
    #extract h and w from overall_mask
    h, w = single_restored_sized_mask.shape
    grid_h = h // rows
    grid_w = w // columns
    #extract each grid rect  from single_restored_sized_mask
    grid_rects = [ (grid_w * j, grid_h * i,grid_w, grid_h)  for i in range(rows)  for j in range(columns)]

    contour_rect_for_each_grid = [];
    contour_for_each_grid = [];
    mask_for_each_grid = [];

    for grid_rect in grid_rects :
        for contour_rec_index in range (len(contours_rects)):
            if basic.overlap_region_percentage(contours_rects[contour_rec_index],grid_rect)>0.5 and contours_rects[contour_rec_index][2]*contours_rects[contour_rec_index][3]>5000 and  contours_rects[contour_rec_index][2]>70 and contours_rects[contour_rec_index][3]>70:
                contour_rect_for_each_grid.append(contours_rects[contour_rec_index])
                contour_for_each_grid.append(contours[contour_rec_index])
                mask_for_each_grid.append(single_restored_sized_mask[contours_rects[contour_rec_index][1]:contours_rects[contour_rec_index][1]+contours_rects[contour_rec_index][3],contours_rects[contour_rec_index][0]:contours_rects[contour_rec_index][0]+contours_rects[contour_rec_index][2]])
            else:
                contour_rect_for_each_grid.append(())
                contour_for_each_grid.append(())
                mask_for_each_grid.append(())


    return [contour_rect_for_each_grid,contour_for_each_grid,mask_for_each_grid]


def load_and_process(image_filepath_list, batch_no, save_path):
    if (batch_no == -1):
        print("{}batch remainder{}".format(Fore.CYAN, Style.RESET_ALL))
    print("Processing batch NO:{}{}{}".format(Fore.BLUE, batch_no + 1, Style.RESET_ALL))
    image_list = io.load_images_by_images_path(image_filepath_list, cv2.COLOR_BGR2RGB)

    start_time = datetime.now()

    resize = 1/4
    image_list_resized_shrink = [cv2.resize(image, (0, 0), fx=resize, fy=resize) for image in image_list]

    shrinked_masks = [segment.threshold_by_colorspace(image) for image in image_list_resized_shrink]
    merged_shrinked_masks = [segment.merge_mask_bitwise_or(mask3arr) for mask3arr in shrinked_masks]

    if resize == 1:
        morphed_masks = [morph.close_and_open(mask, 5, 28) for mask in merged_shrinked_masks]
    else:
        morphed_shrinked_masks = [morph.close_and_open_low_resolution(mask, (3,3), 5) for mask in merged_shrinked_masks]

    morphed_restored_sized_masks = [cv2.resize(mask, (0, 0), fx=1/resize, fy=1/resize) for mask in morphed_shrinked_masks]
    contour_rect_and_contour_and_mask_for_each_grid = [for_each_mask_find_countour_rect(mask) for mask in morphed_restored_sized_masks]
    basic_feature_for_each_grid = [basic.extract_basic_feature(contour_rect_and_contour_and_mask_for_each_grid[image_index],image_list[image_index]) for image_index in range(len(image_list))]
    #draw basic info on image
    for image_index in range(len(image_list)):
        basic.draw_debug_rect_on_each_object_on_whole_image(contour_rect_and_contour_and_mask_for_each_grid[image_index],image_list[image_index],basic_feature_for_each_grid[image_index],rows=4,columns=6)

    end_time = datetime.now()
    duration = end_time - start_time
    print("extract time duration: {}{}{}".format(Fore.BLUE, duration, Style.RESET_ALL))



    #morphed_images = [cv2.cvtColor( cv2.bitwise_and(image,image,mask =morphed_mask ),cv2.COLOR_BGR2RGB) for image,morphed_mask in zip(image_list,restored_sized_mask)]
    io.save_images_by_images_path(image_list,save_path+"/marked_img/",image_filepath_list)
    #io.save_images_by_images_path(morphed_restored_sized_masks,args.output+"/masks_rec/",image_filepath_list)
    return morphed_restored_sized_masks


args = picture_loading_arg_process(__file__)
image_filepath_list = io.load_image_names_from_folder(image_folder=args.input, filename_filter=args.filename_filter)

if len(image_filepath_list) > 0:
    # load image from immage_filepath_list in batch
    batch_size = 10
    remainder_images_count = len(image_filepath_list) % batch_size
    remainder_images = [];
    divisible_images = [];
    if(remainder_images_count>0):
        remainder_images = image_filepath_list[-remainder_images_count:]
        divisible_images = image_filepath_list[:-remainder_images_count]
    else:
        divisible_images = image_filepath_list[-remainder_images_count:]
        remainder_images = image_filepath_list[:-remainder_images_count]

    processing_images = np.array(divisible_images).reshape(-1, batch_size)

    morphed_images = load_and_process(remainder_images, -1, args.output)

    for batch_no in range(0, len(processing_images) - 1):
        load_and_process(processing_images[batch_no], batch_no, args.output)
