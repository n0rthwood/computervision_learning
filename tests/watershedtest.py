import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('../colorspace/fd1.bmp')



gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)


# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)
# sure background area
sure_bg = cv.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv.connectedComponents(sure_fg)
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0

oI=img.copy()
markers = cv.watershed(img,markers)
img[markers == -1] = [255,0,0]

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
axarr[7].imshow(img)
axarr[7].set_title('img')  # get the title property handler
axarr[7].axis('off')
axarr[8].imshow(oI)
axarr[8].set_title('oI')  # get the title property handler
axarr[8].axis('off')
plt.show()