import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('sliced_img_fd2.png')

img_mask = cv.imread('sliced_mask_fd2.png')

gray = cv.cvtColor(img_mask,cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
thresh = cv.bitwise_not(thresh)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)
# sure background area
sure_bg = cv.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
ret, sure_fg = cv.threshold(dist_transform,0.889*dist_transform.max(),255,0)
sure_fg= np.uint8(sure_fg)
unknown = cv.subtract(sure_bg,sure_fg)
# Finding unknown region



# Marker labelling
ret, markers = cv.connectedComponents(sure_fg)
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0

oI=img.copy()
markers = cv.watershed(img_mask,markers)
ws = len(np.unique(markers)) -1

img[markers == -1] = [0,0,255]


surface = np.uint8(sure_fg.copy()*255)

contours_wd, _ = cv.findContours(surface, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for ii in range(len(contours_wd)):
    cv.drawContours(surface, contours_wd, ii, (ii + 1), -1)

count = len(contours_wd)
h,w,ccoo = img.shape
cv.putText(img, 'count:'+str(count), (2,h-7), cv.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 1, cv.LINE_AA)
plt.subplotf, ax = plt.subplots(2,5,figsize=(20,10))
axarr=ax.flat
axarr[0].imshow(thresh,cmap='gray')
axarr[0].set_title('thresh')  # get the title property handler
axarr[0].axis('off')
axarr[1].imshow(opening,cmap='gray')
axarr[1].set_title('opening')  # get the title property handler
axarr[1].axis('off')
axarr[2].imshow(sure_bg,cmap='gray')
axarr[2].set_title('sure_bg')  # get the title property handler
axarr[2].axis('off')
axarr[3].imshow(dist_transform,cmap='gray')
axarr[3].set_title('dist_transform')  # get the title property handler
axarr[3].axis('off')
axarr[4].imshow(sure_fg,cmap='gray')
axarr[4].set_title('sure_fg')  # get the title property handler
axarr[4].axis('off')
axarr[5].imshow(unknown,cmap='gray')
axarr[5].set_title('unknown')  # get the title property handler
axarr[5].axis('off')
axarr[6].imshow(markers,cmap='gray')
axarr[6].set_title('markers')  # get the title property handler
axarr[6].axis('off')
axarr[7].imshow(cv.cvtColor( img,cv.COLOR_BGR2RGB))
axarr[7].set_title('img')  # get the title property handler
axarr[7].axis('off')
axarr[8].imshow(cv.cvtColor( oI, cv.COLOR_BGR2RGB))
axarr[8].set_title('original')  # get the title property handler
axarr[8].axis('off')

plt.show()