import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/cc_s1_sliced_image_3_5.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#use canary to find the object
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()
ax[0].imshow(image)
ax[0].set_title('thresh')
ax[1].imshow(gray, cmap=plt.cm.gray)
ax[1].set_title('thresh')
ax[2].imshow(thresh, cmap=plt.cm.gray)
ax[2].set_title('thresh')

plt.show()
