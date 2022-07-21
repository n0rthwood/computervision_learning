import cv2
import numpy as np
from joycv.colorspace import color_threshold


def threshold_by_colorspace(image, color_cvt_code=(cv2.COLOR_RGB2HSV, cv2.COLOR_RGB2Lab, cv2.COLOR_RGB2YCrCb), genre='general', category='general'):
    masks = []
    for color_cvt_code in color_cvt_code:
            lower_color = color_threshold.get_lower_color(color_cvt_code,genre, category)
            upper_color = color_threshold.get_upper_color(color_cvt_code,genre, category)
            mask = __apply_in_color_in_range(image, color_cvt_code, lower_color, upper_color)
            masks.append(mask)
    return masks


def __apply_in_color_in_range(image, colorspace_transform_code, lower_color, upper_color):
    converted = cv2.cvtColor(image, colorspace_transform_code)
    mask = cv2.inRange(converted, lower_color, upper_color)
    return mask

def merge_mask_bitwise_or(masks):
    #generate a empty mask with the same size of the image
    result = masks[0]
    for i in range(1, len(masks)-1):
        result = cv2.bitwise_or(result, masks[i])
    result= cv2.bitwise_not(result)
    return result

def merge_mask_bitwise_and(masks):
    #generate a empty mask with the same size of the image
    result = np.ones(masks[0].shape, dtype=np.uint8)
    for i in range(1, len(masks)):
        result = cv2.bitwise_and(result, masks[i])
    return result