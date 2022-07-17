import cv2
from joycv.colorspace import color_threshold


def segment(image, color_cvt_code=(cv2.COLOR_RGB2HSV, cv2.COLOR_RGB2Lab, cv2.COLOR_RGB2YCrCb), genre='general', category='general'):
    masks = []
    for color_cvt_code in color_cvt_code:
            lower_color = color_threshold.get_lower_color(genre, category)
            upper_color = color_threshold.get_upper_color(genre, category)
            mask = color_threshold_mask_image(image, color_cvt_code, lower_color,upper_color)
            masks.append(mask)
    return masks


def color_threshold_mask_image(image, colorspace_transform_code, lower_color, upper_color):
    converted = cv2.cvtColor(image, colorspace_transform_code)
    mask = cv2.inRange(converted, lower_color, upper_color)
    return mask

