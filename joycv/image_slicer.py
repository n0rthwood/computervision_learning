import cv2
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from colorama import Fore, Back, Style#color coding print
from features import double
from util import io
from morph import morph
from joycv.features import basic
import config
import argparse
from util.args_setup import picture_loading_arg_process
from joycv.colorspace import segment
import sys

def load_and_process(image_filepath_list,batch_no,save_path):
    if(batch_no==-1):
        print("{}batch remainder{}".format(Fore.CYAN,Style.RESET_ALL))
    print("Processing batch NO:{}{}{}".format(Fore.BLUE,batch_no+1,Style.RESET_ALL))
    image_list = io.load_images_by_images_path(image_filepath_list,cv2.COLOR_BGR2RGB)
    #resize image_list to 1/4 size
    start_time = datetime.now()
    image_list_resized = [cv2.resize(image,(0,0),fx=0.25,fy=0.25) for image in image_list]
    masks = [segment.threshold_by_colorspace(image) for image in image_list_resized]
    merged_masks = [segment.merge_mask_bitwise_or(mask3arr) for mask3arr in masks]
    morphed_masks = [morph.close_and_open(mask,5,7) for mask in merged_masks]
    restored_sized_mask = [cv2.resize(mask,(0,0),fx=4,fy=4) for mask in morphed_masks]
    morphed_images = [cv2.cvtColor( cv2.bitwise_and(image,image,mask =morphed_mask ),cv2.COLOR_BGR2RGB) for image,morphed_mask in zip(image_list,restored_sized_mask)]
    end_time = datetime.now()
    duration = end_time - start_time
    print("extract time duration: {}{}{}".format(Fore.BLUE,duration,Style.RESET_ALL))

    io.save_images_by_images_path(morphed_images,save_path+"/resized_merged/",image_filepath_list)
    return morphed_images



args = picture_loading_arg_process()
image_filepath_list = io.load_image_names_from_folder(image_folder=args.input,filename_filter=args.filename_filter)

if len(image_filepath_list)>0 :
    #load image from immage_filepath_list in batch
    batch_size = 10
    remainder_images_count = len(image_filepath_list)%batch_size
    remainder_images = image_filepath_list[-remainder_images_count:]
    divisible_images = image_filepath_list[:-remainder_images_count]
    processing_images = np.array(divisible_images).reshape(-1,batch_size)

    morphed_images  = load_and_process(remainder_images,-1,args.output)

    for batch_no in range(0,len(processing_images)-1):
        load_and_process(processing_images[batch_no],batch_no,args.output)



    #images = io.load_images_by_images_path(image_filepath_list,cvtColor_code=cv2.COLOR_BGR2RGB)


# images,masks,image_names_list = io.load_image_from_folder(
#     image_folder=args.input,
#     process_while_loading=True,
#     extention=('.bmp', '.png'),
#     filename_filter=args.filename_filter,
#     cvtColor_code=cv2.COLOR_BGR2RGB,
#     genre=args.genre,
#     category=args.category
# )

# if(len(images)>0):
#     print('Image loading Duration: {} total image {} , {} ms per pic'.format(duration,len(images),duration/len(images)))
# else:
#     print('No image found in the folder "{}" with image filename filter {}'.format(args.input,args.filter))
#     exit()