import os
import cv2
import fnmatch
from joycv.colorspace import segment


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

    return image_list, mask_list,image_names_list





def slice_by_grid(image,mask, slice_grid_row_column=[4,6]):
        sliced_images = []
        sliced_masks = []
        h, w, _ = image.shape
        grid_h = h // slice_grid_row_column[0]
        grid_w = w // slice_grid_row_column[1]
        for i in range(slice_grid_row_column[0]):
            for j in range(slice_grid_row_column[1]):
                sliced_image = image[i*grid_h:(i+1)*grid_h,j*grid_w:(j+1)*grid_w]
                sliced_mask =  mask[i*grid_h:(i+1)*grid_h,j*grid_w:(j+1)*grid_w]
                sliced_images.append(sliced_image)
                sliced_masks.append(sliced_mask)
        return sliced_images,sliced_masks


def slice_by_grid_batch(image_list,mask_list, slice_grid_row_column=[4,6]):
    image_list_sliced = []
    mask_list_sliced = []
    for im in range(0, len(image_list)):
        image = image_list[im]
        mask = mask_list[im]
        sliced_images,sliced_masks =slice_by_grid(image,mask, slice_grid_row_column)
        image_list_sliced.append(sliced_images)
        mask_list_sliced.append(sliced_masks)
    return image_list_sliced, mask_list_sliced