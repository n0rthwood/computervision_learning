from datetime import datetime
import cv2
import numpy as np
from colorama import Fore, Style  # color coding print

from colorspace import segment
from features import basic
from morph import morph
from util import io
from util.args_setup import picture_loading_arg_process




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
    contour_rect_and_contour_and_mask_for_each_grid = [basic.for_each_mask_find_countour_rect(mask) for mask in morphed_restored_sized_masks]
    basic_feature_for_each_grid = [basic.extract_basic_feature(contour_rect_and_contour_and_mask_for_each_grid[image_index],image_list[image_index],sliced_training_size=args.training_size,padding=args.padding) for image_index in range(len(image_list))]
    #draw basic info on image
    if args.debug:
        drawn_image_list = [];
        for image_index in range(len(image_list)):
            drawn_image = basic.draw_debug_rect_on_each_object_on_whole_image(contour_rect_and_contour_and_mask_for_each_grid[image_index],image_list[image_index],basic_feature_for_each_grid[image_index],rows=4,columns=6)
            drawn_image_list.append(drawn_image)
        io.save_images_by_images_path(drawn_image_list,save_path+"/debug_img/",image_filepath_list)

    end_time = datetime.now()
    duration = end_time - start_time
    print("extract time duration: {}{}{}".format(Fore.BLUE, duration, Style.RESET_ALL))


    for image_index in range(len(image_list)):
        image_main_name = image_filepath_list[image_index].split("/")[-1]
        io.sliced_and_save_image(image_list[image_index],basic_feature_for_each_grid[image_index],save_path+"/sliced_image/",image_main_name,save_mode=args.save_mode)

    return duration.microseconds


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

    durations = []
    duration = load_and_process(remainder_images, -1, args.output)
    durations.append(duration)
    for batch_no in range(0, len(processing_images) - 1):
        duration= load_and_process(processing_images[batch_no], batch_no, args.output)
        durations.append(duration)

    total_duration = round(sum(durations)/1000)
    total_pictures = len(image_filepath_list)
    avg_duration = round(total_duration / total_pictures)
    print("avg duration per picture {}{}{}ms,total picture{}{}{} of total duration{}{}{}ms".format(
        Fore.BLUE,avg_duration, Style.RESET_ALL, Fore.BLUE, total_pictures, Style.RESET_ALL, Fore.BLUE, total_duration, Style.RESET_ALL))

