import cv2
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

plt.rcParams['figure.figsize'] = (20, 10)
plt.rcParams['figure.dpi'] = 300

GENERAL_HSV_THRESHOLD = [(0.381*180, 0.235*255, 0.235),(0.572 * 180, 1 * 255, 1.000 * 255)]
GENERAL_LAB_THRESHOLD = [(27.395*255/100, -50.539+128, -56.825+128), (98.827*255/100, -4.534+128, 5.829+128)]
GENERAL_YCrCB_THRESHOLD = [(0.000, 0.000, 117.000), (255.000, 114.000, 255.000)]
GENERAL_THRESHOLD=[GENERAL_HSV_THRESHOLD,GENERAL_LAB_THRESHOLD,GENERAL_YCrCB_THRESHOLD]


def color_threshold_mask_image(image,colorspace_transform_code, lower_color, upper_color):
    converted = cv2.cvtColor(image, colorspace_transform_code)
    mask = cv2.inRange(converted, lower_color, upper_color)
    return mask

image = cv2.imread('fd1.bmp',1)
start_time = datetime.now()
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

#hsvmask = hsv_color_threshold_mask_image(image, (0.000*180, 0.000*255, 0.000), (1.000 * 180, 0.224 * 255, 1.000 * 255))
hsvmask = color_threshold_mask_image(image,cv2.COLOR_RGB2HSV, GENERAL_THRESHOLD[0][0], GENERAL_THRESHOLD[0][1])
labmask = color_threshold_mask_image(image,cv2.COLOR_RGB2Lab, GENERAL_THRESHOLD[1][0], GENERAL_THRESHOLD[1][1])
ycbrcmask = color_threshold_mask_image(image, cv2.COLOR_RGB2YCrCb,GENERAL_THRESHOLD[2][0], GENERAL_THRESHOLD[2][1])

mergedMask = np.zeros(image.shape[:2], dtype="uint8")
mergedMask = cv2.bitwise_or(hsvmask, labmask)
mergedMask = cv2.bitwise_or(mergedMask, ycbrcmask)

mergedMask = cv2.bitwise_not(mergedMask) #invert mask to get black on white mask so we can use it to do close and openings

mmorphed_kernal=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
mmorphed_mk=cv2.morphologyEx(mergedMask, cv2.MORPH_CLOSE, mmorphed_kernal, iterations=2)

mmorphed_kernal=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(28,28))
mmorphed_mk=cv2.morphologyEx(mmorphed_mk, cv2.MORPH_OPEN, mmorphed_kernal, iterations=2)

final=cv2.bitwise_and(image, image.copy(),mask=mmorphed_mk)

gray_final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
ret,gray_final = cv2.threshold(gray_final,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

src1_mask=cv2.cvtColor(mmorphed_mk,cv2.COLOR_GRAY2BGR)#change mask to a 3 channel image
mask_out=cv2.subtract(src1_mask,image)
mask_out=cv2.subtract(src1_mask,mask_out)


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

axarr[6].imshow(image)
title_obj = axarr[6].set_title('original')  # get the title property handler

axarr[7].imshow(final)
title_obj = axarr[7].set_title('final')  # get the title property handler
plt.show()

correct_color=image

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

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
        sliced_img = correct_color[i*grid_h:(i+1)*grid_h,j*grid_w:(j+1)*grid_w];
        sliced_mask=mmorphed_mk[i*grid_h:(i+1)*grid_h,j*grid_w:(j+1)*grid_w];
        # if(i==3 and j==5):
        #     sliced_img_s=cv2.cvtColor(sliced_img,cv2.COLOR_BGR2RGB)
        #     sliced_mask_s=cv2.cvtColor(sliced_mask,cv2.COLOR_GRAY2BGR)
        #     sliced_img_masked_s=cv2.add(sliced_img_s,sliced_mask_s)
        #     cv2.imwrite('sliced_img.png',sliced_img_s)
        #     cv2.imwrite('sliced_mask.png',sliced_mask_s)
        #     cv2.imwrite('sliced_img_masked.png',sliced_img_masked_s)

        # dist = cv2.distanceTransform(sliced_mask, cv2.DIST_L2, 3)
        # ret, dist1 = cv2.threshold(dist, 0.6 * dist.max(), 255, 0)
        # markers = np.zeros(dist.shape, dtype=np.int32)
        # dist_8u = dist1.astype('uint8')
        # contours_wd, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # for ii in range(len(contours_wd)):
        #     cv2.drawContours(markers, contours_wd, ii, (ii + 1), -1)
        #
        # markers = cv2.circle(markers, (15, 15), 5, len(contours_wd) + 1, -1)
        #
        # # watershed
        #
        # waterden_marker = cv2.watershed(sliced_img, cv2.bitwise_not(markers))
        # sliced_img[waterden_marker == -1] = [255, 160, 0]

        contours, hierarchy = cv2.findContours(sliced_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(sliced_img, contours, -1, (255, 0, 0), 3)
        # markers = np.zeros(dist.shape, dtype=np.int32)
        # cv2.drawContours(markers, contours, i, (i + 1), -1)
        # for i in range(len(contours)):
        #     cv2.drawContours(markers, contours, i, (i + 1), -1)




        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea,default=0)
            left = tuple(c[c[:, :, 0].argmin()][0])
            right = tuple(c[c[:, :, 0].argmax()][0])
            top = tuple(c[c[:, :, 1].argmin()][0])
            bottom = tuple(c[c[:, :, 1].argmax()][0])

            cv2.drawContours(sliced_img, [c], -1, (36, 255, 12), 2)
            cv2.circle(sliced_img, left, 8, (0, 50, 255), -1)
            cv2.circle(sliced_img, right, 8, (0, 255, 255), -1)


            cv2.circle(sliced_img, top, 8, (255, 50, 0), -1)
            cv2.circle(sliced_img, bottom, 8, (255, 255, 0), -1)

            YCrCb_mean = cv2.mean(cv2.cvtColor(sliced_img, cv2.COLOR_RGB2YCrCb), sliced_mask)


            h,w,ccoo = sliced_img.shape
            cv2.rectangle(sliced_img, (left[0],top[1]), (right[0],bottom[1]), (255, 0, 0), 2)
            cv2.putText(sliced_img, 'w:'+str(right[0]-left[0])+' h:'+str(bottom[1]-top[1])+' c[0-255]:'+str(round(YCrCb_mean[0])), (2,h-5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 0), 1, cv2.LINE_AA)
        grid_images.append(sliced_img)
        axarr[pltindex].imshow(sliced_img)
        axarr[pltindex].axis('off')
        title_obj = axarr[pltindex].set_title(''+str(i)+str("-")+str(j))  # get the title property handler

        # print(pltindex)
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

