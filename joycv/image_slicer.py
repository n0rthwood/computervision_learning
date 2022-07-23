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


def for_each_mask_find_basic_feature(overall_mask):
    contours = basic.find_contours(overall_mask)
    contrours_rects = [cv2.boundingRect(contour) for contour in contours]
    columns = args.column
    rows = args.row
    #extract h and w from overall_mask
    h, w = overall_mask.shape
    grid_h = h // rows
    grid_w = w // columns
    #extract each grid rect  from overall_mask
    grid_rects = [ (grid_w * j, grid_h * i,grid_w, grid_h)  for i in range(rows)  for j in range(columns)]
    contour_for_each_grid=[ [contour_rec for contour_rec in contrours_rects if basic.overlap_region_percentage(contour_rec,grid_rect)>0.5] for grid_rect in grid_rects]
    #draw contour_for_each_grid on overall_mask
    for i in range(rows):
        for j in range(columns):
            contour_rects = contour_for_each_grid[i*columns+j]
            for contour_rect in contour_rects:
                x, y, w, h = contour_rect
                area =  w*h;
                if(area>5000):
                    cv2.rectangle(overall_mask, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    #put label on top of the rectangle of column and row
                    cv2.putText(overall_mask, "r:"+str(i) + ",c:" + str(j)+"area:"+str(w*h), (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return contour_for_each_grid


def load_and_process(image_filepath_list, batch_no, save_path):
    if (batch_no == -1):
        print("{}batch remainder{}".format(Fore.CYAN, Style.RESET_ALL))
    print("Processing batch NO:{}{}{}".format(Fore.BLUE, batch_no + 1, Style.RESET_ALL))
    image_list = io.load_images_by_images_path(image_filepath_list, cv2.COLOR_BGR2RGB)
    # resize image_list to 1/4 size
    start_time = datetime.now()
    image_list_resized = [cv2.resize(image, (0, 0), fx=0.25, fy=0.25) for image in image_list]

    masks = [segment.threshold_by_colorspace(image) for image in image_list_resized]
    merged_masks = [segment.merge_mask_bitwise_or(mask3arr) for mask3arr in masks]
    morphed_masks = [morph.close_and_open_low_resolution(mask, (3,3), 5) for mask in merged_masks]
    #io.save_images_by_images_path(merged_masks,args.output+"/resized_merged_mask_rec/",image_filepath_list)
    # restore the mask size to 1:1
    restored_sized_masks = [cv2.resize(mask, (0, 0), fx=4, fy=4) for mask in morphed_masks]


    contour_for_each_grid = [for_each_mask_find_basic_feature(mask) for mask in restored_sized_masks]


    end_time = datetime.now()
    duration = end_time - start_time
    print("extract time duration: {}{}{}".format(Fore.BLUE, duration, Style.RESET_ALL))
    #morphed_images = [cv2.cvtColor( cv2.bitwise_and(image,image,mask =morphed_mask ),cv2.COLOR_BGR2RGB) for image,morphed_mask in zip(image_list,restored_sized_mask)]
    io.save_images_by_images_path(morphed_masks,save_path+"/resized_merged/",image_filepath_list)
    io.save_images_by_images_path(restored_sized_masks,args.output+"/masks_rec/",image_filepath_list)
    return restored_sized_masks


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
