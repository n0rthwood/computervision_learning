import cv2


def color_threshold_mask_image(image, colorspace_transform_code, lower_color, upper_color):
    converted = cv2.cvtColor(image, colorspace_transform_code)
    mask = cv2.inRange(converted, lower_color, upper_color)
    return mask
