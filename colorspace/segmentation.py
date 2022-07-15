import cv2
import matplotlib.pyplot as plt
import numpy as np

def color_threshold_mask_image(image,colorspace_transform_code, lower_color, upper_color):
    converted = cv2.cvtColor(image, colorspace_transform_code)
    mask = cv2.inRange(converted, lower_color, upper_color)
    return mask

image = cv2.imread('ap3.bmp',1)


#hsvmask = hsv_color_threshold_mask_image(image, (0.000*180, 0.000*255, 0.000), (1.000 * 180, 0.224 * 255, 1.000 * 255))
hsvmask = color_threshold_mask_image(image,cv2.COLOR_BGR2HSV, (0.381*180, 0.235*255, 0.235), (0.572 * 180, 1 * 255, 1.000 * 255))
labmask = color_threshold_mask_image(image,cv2.COLOR_BGR2Lab, (27.395*255/100, -50.539+128, -56.825+128), (98.827*255/100, -4.534+128, 5.829+128))
ycbrcmask = color_threshold_mask_image(image, cv2.COLOR_BGR2YCrCb,(0.000, 0.000, 117.000), (255.000, 114.000, 255.000))

mergedMask = np.zeros(image.shape[:2], dtype="uint8")
mergedMask = cv2.bitwise_or(hsvmask, labmask)
mergedMask = cv2.bitwise_or(mergedMask, ycbrcmask)

mergedMask = cv2.bitwise_not(mergedMask) #invert mask to get black on white mask so we can use it to do close and openings

mmorphed_kernal=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
mmorphed_mk=cv2.morphologyEx(mergedMask, cv2.MORPH_CLOSE, mmorphed_kernal, iterations=2)

mmorphed_kernal=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(28,28))
mmorphed_mk=cv2.morphologyEx(mmorphed_mk, cv2.MORPH_OPEN, mmorphed_kernal, iterations=2)


f, ax = plt.subplots(2,4)
axarr=ax.flat
# overlay image with mask
axarr[0].imshow(hsvmask)
title_obj = axarr[0].set_title('hsv_masked_image')  # get the title property handler

axarr[1].imshow(labmask)
title_obj = axarr[1].set_title('lab_masked_image')  # get the title property handler

axarr[2].imshow(ycbrcmask)
title_obj = axarr[2].set_title('ycbrc_masked_image')  # get the title property handler

axarr[3].imshow(mergedMask)
title_obj = axarr[3].set_title('merged_masked_image')  # get the title property handler

axarr[4].imshow(mmorphed_mk)
title_obj = axarr[4].set_title('_MORPH_CLOSE_')  # get the title property handler

axarr[5].imshow(mmorphed_mk)
title_obj = axarr[5].set_title('_MORPH_OPEN')  # get the title property handler


src1_mask=cv2.cvtColor(mmorphed_mk,cv2.COLOR_GRAY2BGR)#change mask to a 3 channel image
mask_out=cv2.subtract(src1_mask,image)
mask_out=cv2.subtract(src1_mask,mask_out)

axarr[6].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
title_obj = axarr[6].set_title('original')  # get the title property handler
final=cv2.bitwise_not(image, image,mask=mmorphed_mk)

axarr[7].imshow(cv2.cvtColor(final, cv2.COLOR_BGR2RGB))
title_obj = axarr[7].set_title('final')  # get the title property handler
#plt.show()

correct_color=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#cv2.imshow('mask_out',mask_out)
#slice image into 4*6 grid and display
h,w,c = mask_out.shape
grid=[4,6]
f, ax = plt.subplots(4,6)
axarr=ax.flat
grid_h=h//grid[0]
grid_w=w//grid[1]
grid_images=[];
pltindex=0;
for i in range(grid[0]):
    for j in range(grid[1]):
        grid_images.append(correct_color[i*grid_h:(i+1)*grid_h,j*grid_w:(j+1)*grid_w])
        axarr[pltindex].imshow(grid_images[pltindex])
        title_obj = axarr[pltindex].set_title('mask_out_'+str(i)+str(j))  # get the title property handler

        print(pltindex)
        pltindex += 1

plt.show()


#cv2.waitKey(0)



#load image from a folder and loop through all images in the folder

# path_of_the_directory = '../testbmp/'
# ext = ('.bmp','.png')
# for file in os.listdir(path_of_the_directory):
#     if file.endswith(ext):
#         print(file)
#         image = cv2.imread(path_of_the_directory+file)
#
#     else:
#         continue

