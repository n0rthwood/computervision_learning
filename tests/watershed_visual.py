import joycv.features.double as double
import numpy as np
from matplotlib import pyplot as plt
import skimage as skimage
import tempfile
from pathlib import Path
import cv2 as cv

# root_path='/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/fd2_sliced_mask_3_5.npy';
# image = np.load(root_path , allow_pickle=True)
image = cv.imread('/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/cc_s1_sliced_image_3_5.png')

image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# Get information regarding the shape of the image.
im_shape = np.shape(image)
x = np.arange(0, im_shape[0], 1)
y = np.arange(0, im_shape[1], 1)

# Make a grid
x, y = np.meshgrid(x, y)

# Do the 3D plot.
fig = plt.figure( figsize=(20,10) )
ax = fig.add_subplot(2, 2, 1, projection='3d')
surf = ax.plot_surface(x, y, np.transpose(image), cmap=plt.cm.gray)
plt.xlim([0, im_shape[0]])
plt.ylim([0, im_shape[1]])

# Rotate and tilt the plot so peaks and valleys are obvious
#ax.view_init(70, 360)

ax2 = fig.add_subplot(2, 2, 2)
ax2.imshow(image, cmap=plt.cm.gray)

######

# Compute the gradients of the image using a sobel filter.
im_grad = skimage.filters.sobel(image)
kernel = np.ones((1, 1), np.uint8)
im_grad = cv.morphologyEx(im_grad, cv.MORPH_CLOSE, kernel, iterations=2)
# Get information regarding the shape of the image.
im_shape = np.shape(im_grad)
x = np.arange(0, im_shape[0], 1)
y = np.arange(0, im_shape[1], 1)

#Make a grid
x, y = np.meshgrid(x, y)

# Do the 3D plot.

ax = fig.add_subplot(2, 2, 3, projection='3d')
surf = ax.plot_surface(x, y, np.transpose(im_grad), cmap=plt.cm.viridis)
plt.xlim([0, im_shape[0]])
plt.ylim([0, im_shape[1]])

# Rotate and tilt the plot so peaks and valleys are obvious
#ax.view_init(80, 360)


ax2 = fig.add_subplot(2, 2, 4)
ax2.imshow(im_grad, cmap=plt.cm.gray)

plt.show()