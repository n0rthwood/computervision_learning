import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# define a function to use RGB color thresholding to generate a mask for the image

def hsv_color_threshold_mask_image(image, lower_color, upper_color):
    # convert the image to the HSV color space
    converted = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # create a mask using the lower and upper bounds of the color
    mask = cv2.inRange(converted, lower_color, upper_color)

    # return the mask
    return mask

def lab_color_threshold_mask_image(image, lower_color, upper_color):
    # convert the image to the HSV color space
    converted = cv2.cvtColor(image, cv2.COLOR_RGB2Lab)

    # create a mask using the lower and upper bounds of the color
    mask = cv2.inRange(converted, lower_color, upper_color)

    # return the mask
    return mask


def ycbrc_color_threshold_mask_image(image, lower_color, upper_color):
    # convert the image to the HSV color space
    converted = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)

    # create a mask using the lower and upper bounds of the color
    mask = cv2.inRange(converted, lower_color, upper_color)

    # return the mask
    return mask




#load image from a folder and loop through all images in the folder

# path_of_the_directory = '../testbmp/'
# ext = ('.bmp','.png')
# for file in os.listdir(path_of_the_directory):
#     if file.endswith(ext):
#         print(file)
#         image = cv2.imread(path_of_the_directory+file)
#         hsvmask = hsv_color_threshold_mask_image(image, (0.000*179, 0.280*255, 0.000), (1.000 * 179, 0.224 * 255, 1.000 * 255))
#         labmask = lab_color_threshold_mask_image(image, (0.000*255/100, -56.877+128, -63.495+128), (84.526*255/100, -7.537+128, 61.976+128))
#         ycbrcmask = ycbrc_color_threshold_mask_image(image, (0.000, 0.000, 0.000), (255.000, 255.000, 116.000))
#         hsv_masked_image = cv2.bitwise_and(image, image, mask=hsvmask)
#         lab_masked_image = cv2.bitwise_and(image, image, mask=labmask)
#         ycbrc_masked_image = cv2.bitwise_and(image, image, mask=ycbrcmask)
#
#         plt.figure()
#         # overlay image with mask
#         plt.imshow(hsv_masked_image)
#         title_obj = plt.title('hsv_masked_image')  # get the title property handler
#         plt.getp(title_obj)  # print out the properties of title
#         plt.getp(title_obj, 'text')  # print out the 'text' property for title
#         plt.setp(title_obj, color='r')  # set the color of title to red
#         plt.show()
#
#         plt.imshow(lab_masked_image)
#         title_obj = plt.title('lab_masked_image')  # get the title property handler
#         plt.getp(title_obj)  # print out the properties of title
#         plt.getp(title_obj, 'text')  # print out the 'text' property for title
#         plt.setp(title_obj, color='r')  # set the color of title to red
#         plt.show()
#
#         plt.imshow(ycbrc_masked_image)
#         title_obj = plt.title('ycbrc_masked_image')  # get the title property handler
#         plt.getp(title_obj)  # print out the properties of title
#         plt.getp(title_obj, 'text')  # print out the 'text' property for title
#         plt.setp(title_obj, color='r')  # set the color of title to red
#         plt.show()
#     else:
#         continue


image = cv2.imread('../testbmp/fullcategory.png')
hsvmask = hsv_color_threshold_mask_image(image, (0.000*179, 0.000*255, 0.000), (1.000 * 179, 0.224 * 255, 1.000 * 255))
labmask = lab_color_threshold_mask_image(image, (0.000*255/100, -7.537+128, -63.495+128), (84.526*255/100, 45+128, 61.976+128))
ycbrcmask = ycbrc_color_threshold_mask_image(image, (0.000, 0.000, 120.000), (255.000, 255.000, 255.000))


# lab_masked_image = cv2.bitwise_and(image, image, mask=labmask)
# hsv_masked_image = cv2.bitwise_and(image, image, mask=hsvmask)
# ycbrc_masked_image = cv2.bitwise_and(image, image, mask=ycbrcmask)

plt.figure()
# overlay image with mask
plt.imshow(hsvmask)
title_obj = plt.title('hsv_masked_image')  # get the title property handler
plt.getp(title_obj)  # print out the properties of title
plt.getp(title_obj, 'text')  # print out the 'text' property for title
plt.setp(title_obj, color='r')  # set the color of title to red
plt.show()

plt.imshow(labmask)
title_obj = plt.title('lab_masked_image')  # get the title property handler
plt.getp(title_obj)  # print out the properties of title
plt.getp(title_obj, 'text')  # print out the 'text' property for title
plt.setp(title_obj, color='g')  # set the color of title to red
plt.show()

plt.imshow(ycbrcmask)
title_obj = plt.title('ycbrc_masked_image')  # get the title property handler
plt.getp(title_obj)  # print out the properties of title
plt.getp(title_obj, 'text')  # print out the 'text' property for title
plt.setp(title_obj, color='b')  # set the color of title to red
plt.show()

merged=(hsvmask+labmask+ycbrcmask)/3

plt.imshow(merged)
title_obj = plt.title('merged_masked_image')  # get the title property handler
plt.getp(title_obj)  # print out the properties of title
plt.getp(title_obj, 'text')  # print out the 'text' property for title
plt.setp(title_obj, color='b')  # set the color of title to red
plt.show()

erode_kernal=disk(1)
erodedMK=cv2.erode(merged, None, iterations=2)
plt.imshow(erodedMK)
title_obj = plt.title('eroded_masked_image')  # get the title property handler
plt.getp(title_obj)  # print out the properties of title
plt.getp(title_obj, 'text')  # print out the 'text' property for title
plt.setp(title_obj, color='b')  # set the color of title to red
plt.show()


dilate_kernal=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
dilatedMK=cv2.dilate(erodedMK, None, iterations=2)
plt.imshow(dilatedMK)
title_obj = plt.title('dialted_mk_masked_image')  # get the title property handler
plt.getp(title_obj)  # print out the properties of title
plt.getp(title_obj, 'text')  # print out the 'text' property for title
plt.setp(title_obj, color='b')  # set the color of title to red
plt.show()

mmorphed_kernal=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(22,22))
mmorphed_mk=cv2.morphologyEx(dilatedMK, cv2.MORPH_OPEN, None, iterations=2)
plt.imshow(mmorphed_mk)
title_obj = plt.title('mmorphed_mk_masked_image')  # get the title property handler
plt.getp(title_obj)  # print out the properties of title
plt.getp(title_obj, 'text')  # print out the 'text' property for title
plt.setp(title_obj, color='b')  # set the color of title to red
plt.show()