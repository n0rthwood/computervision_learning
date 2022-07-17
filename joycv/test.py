import cv2
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from features import double
from util import io

plt.rcParams['figure.figsize'] = (20, 10)
plt.rcParams['figure.dpi'] = 300

images = io.load_image_from_folder('../testbmp/', None, 'cc*')
start_time = datetime.now()



end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))



# mergedMask = np.zeros(image.shape[:2], dtype="uint8")
mergedMask = cv2.bitwise_or(hsvmask, labmask)
mergedMask = cv2.bitwise_or(mergedMask, ycbrcmask)

mergedMask = cv2.bitwise_not(
    mergedMask)  # invert mask to get black on white mask so we can use it to do close and openings

mmorphed_kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mmorphed_mk = cv2.morphologyEx(mergedMask, cv2.MORPH_CLOSE, mmorphed_kernal, iterations=2)

mmorphed_kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (28, 28))
mmorphed_mk = cv2.morphologyEx(mmorphed_mk, cv2.MORPH_OPEN, mmorphed_kernal, iterations=2)

final = cv2.bitwise_and(image, image.copy(), mask=mmorphed_mk)

gray_final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
ret, gray_final = cv2.threshold(gray_final, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

src1_mask = cv2.cvtColor(mmorphed_mk, cv2.COLOR_GRAY2BGR)  # change mask to a 3 channel image
mask_out = cv2.subtract(src1_mask, image)
mask_out = cv2.subtract(src1_mask, mask_out)

f, ax = plt.subplots(2, 4)

axarr = ax.flat
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

axarr[7].imshow(gray_final)
title_obj = axarr[7].set_title('final')  # get the title property handler
plt.show()

correct_color = image

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# slice image into 4*6 grid and display
h, w, c = mask_out.shape
grid = [4, 6]
f, ax = plt.subplots(4, 6)
axarr = ax.flat
grid_h = h // grid[0]
grid_w = w // grid[1]
grid_images = [];
pltindex = 0;
for i in range(grid[0]):
    for j in range(grid[1]):
        sliced_img = correct_color[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w];
        sliced_mask = mmorphed_mk[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w];
        double_check_mask = cv2.cvtColor(sliced_mask, cv2.COLOR_GRAY2RGB);

        contours, hierarchy = cv2.findContours(sliced_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(sliced_img, contours, -1, (255, 0, 0), 3)

        if len(contours) != 0:
            double_count, thresh, opening, sure_bg, dist_transform, sure_fg, unknown_area, markers = double.check_double(
                double_check_mask)
            c = max(contours, key=cv2.contourArea, default=0)
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

            h, w, ccoo = sliced_img.shape
            cv2.rectangle(sliced_img, (left[0], top[1]), (right[0], bottom[1]), (255, 0, 0), 2)
            cv2.putText(sliced_img,
                        'w:' + str(right[0] - left[0]) + ' h:' + str(bottom[1] - top[1]) + ' c[0-255]:' + str(
                            round(YCrCb_mean[0])) + ' d:' + str(double_count), (2, h - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 0), 1, cv2.LINE_AA)
        grid_images.append(sliced_img)
        axarr[pltindex].imshow(sliced_img)
        axarr[pltindex].axis('off')
        title_obj = axarr[pltindex].set_title('' + str(i) + str("-") + str(j))  # get the title property handler

        # print(pltindex)
        pltindex += 1

plt.show()

exit()
# cv2.waitKey(0)


# load image from a folder and loop through all images in the folder
