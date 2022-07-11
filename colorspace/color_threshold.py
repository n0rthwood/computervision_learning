import cv2
import matplotlib.pyplot as plt
import os
# define a function to use RGB color thresholding to generate a mask for the image

def mask_image(image, lower_color, upper_color):
    # convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # create a mask using the lower and upper bounds of the color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # return the mask
    return mask



#load image from a folder and loop through all images in the folder

path_of_the_directory = '/Volumes/Public/dateimages/deaddry/21-11-08 13-06-02/'
ext = ('.bmp')
for file in os.listdir(path_of_the_directory):
    if file.endswith(ext):
        print(file)
        image = cv2.imread(path_of_the_directory+file)
        mask = mask_image(image, (0.000, 0.000, 0.000), (1.000 * 179, 0.224 * 255, 1.000 * 255))
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        plt.figure()
        # overlay image with mask
        plt.imshow(masked_image)
        plt.show()
    else:
        continue

exit()